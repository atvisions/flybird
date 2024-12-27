from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import logging
import random
from django.core.cache import cache
import traceback
import os

logger = logging.getLogger('users')

def generate_code():
    """生成6位验证码"""
    return ''.join(random.choices('0123456789', k=6))

def send_sms(phone, code, scene):
    """发送短信"""
    # 记录发送信息
    logger.info(f"环境变量 VIRTUAL_SMS: {os.getenv('VIRTUAL_SMS')}")
    logger.info(f"发送短信 - 手机号: {phone}, 验证码: {code}, 场景: {scene}")
    logger.info(f"虚拟短信: {'是' if settings.SMS_CONFIG['VIRTUAL_SMS'] else '否'}")
    logger.info(f"阿里云配置:")
    logger.info(f"ACCESS_KEY_ID: {settings.ALIYUN['ACCESS_KEY_ID']}")
    logger.info(f"SIGN_NAME: {settings.ALIYUN['SMS_SIGN_NAME']}")
    logger.info(f"模板ID: {settings.ALIYUN['SMS_TEMPLATES'][scene]}")
    
    # 根据配置决定是否使用虚拟短信
    if settings.SMS_CONFIG['VIRTUAL_SMS']:
        logger.info(f"使用虚拟短信 - 验证码: {code}")
        return True
    
    # 发送真实短信
    try:
        # 初始化客户端
        client = AcsClient(
            settings.ALIYUN['ACCESS_KEY_ID'],
            settings.ALIYUN['ACCESS_KEY_SECRET'],
            'cn-hangzhou'
        )
        
        # 组装请求对象
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('http')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        
        # 记录请求参数
        params = {
            'PhoneNumbers': phone,
            'SignName': settings.ALIYUN['SMS_SIGN_NAME'],
            'TemplateCode': settings.ALIYUN['SMS_TEMPLATES'][scene],
            'TemplateParam': json.dumps({'code': code}, separators=(',', ':'))
        }
        logger.info(f"请求参数: {params}")
        
        # 设置发送参数
        for key, value in params.items():
            request.add_query_param(key, value)
        
        # 发送请求
        logger.info("开始发送请求...")
        logger.info(f"请求方法: {request.get_method()}")
        logger.info(f"请求域名: {request.get_domain()}")
        logger.info(f"请求协议: {request.get_protocol_type()}")
        logger.info(f"请求版本: {request.get_version()}")
        logger.info(f"请求动作: {request.get_action_name()}")
        
        response = client.do_action_with_exception(request)
        result = json.loads(response)
        
        logger.info(f"短信发送结果: {result}")
        
        if result.get('Code') != 'OK':
            logger.error(f"阿里云返回错误: {result}")
            raise Exception(f"短信发送失败: {result.get('Message')}")
            
        return True
        
    except Exception as e:
        logger.error(f"短信发送异常: {str(e)}")
        logger.error(f"异常详情: {traceback.format_exc()}")
        raise

def verify_code(phone, code, scene):
    """验证短信验证码"""
    cached_code = cache.get(f'sms_code_{scene}_{phone}')
    return cached_code and code == cached_code