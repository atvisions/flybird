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
    """
    发送阿里云短信验证码
    """
    try:
        # 初始化阿里云客户端
        client = AcsClient(
            settings.ALIYUN['ACCESS_KEY_ID'],
            settings.ALIYUN['ACCESS_KEY_SECRET'],
            'cn-hangzhou'
        )
        
        # 组装请求
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        
        # 获取场景对应的模板代码
        template_code = settings.ALIYUN['SMS_TEMPLATES'].get(scene)
        if not template_code:
            raise ValueError(f'无效的短信场景: {scene}')
        
        # 设置请求参数
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', settings.ALIYUN['SMS_SIGN_NAME'])
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', json.dumps({'code': code}))
        
        # 发送请求
        logger.info(f"发送短信 - 手机号: {phone}, 场景: {scene}, 模板: {template_code}")
        response = client.do_action_with_exception(request)
        response_data = json.loads(response.decode())
        
        # 检查响应
        if response_data.get('Code') != 'OK':
            logger.error(f"短信发送失败: {response_data}")
            raise Exception(response_data.get('Message', '短信发送失败'))
            
        logger.info(f"短信发送成功 - RequestId: {response_data.get('RequestId')}")
        return True
        
    except Exception as e:
        logger.error(f"短信发送异常: {str(e)}", exc_info=True)
        raise Exception(f"短信发送失败: {str(e)}")

def verify_code(phone, code, scene):
    """验证短信验证码"""
    cached_code = cache.get(f'sms_code_{scene}_{phone}')
    return cached_code and code == cached_code