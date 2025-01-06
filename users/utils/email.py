from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import redis
import logging
import traceback
import base64

def generate_email_code():
    """生成6位数字验证码"""
    return ''.join(random.choices('0123456789', k=6))

def get_logo_base64():
    """获取 logo 的 base64 编码"""
    logo_path = settings.BASE_DIR / 'static/images/logo.png'
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    return base64.b64encode(logo_data).decode()

def send_verification_email(email, code):
    """发送验证码邮件"""
    logger = logging.getLogger('users')
    try:
        # 获取 logo 的 base64 编码
        logo_base64 = get_logo_base64()
        
        # 渲染HTML模板
        html_message = render_to_string('email/verification_code.html', {
            'code': code,
            'logo_base64': logo_base64
        })
        # 获取纯文本内容
        plain_message = strip_tags(html_message)
        
        # 邮件内容配置
        email_data = {
            'subject': '【飞鸟简历】邮箱验证码',
            'message': plain_message,
            'html_message': html_message,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [email],
            'fail_silently': False,
        }
        
        # 记录所有邮件配置
        logger.info("邮件配置信息:")
        logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        logger.info(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # 保存验证码到Redis
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        redis_client.setex(f'email_code:{email}', 300, code)
        
        logger.info(f"开始发送邮件到 {email}")
        logger.info(f"发件人: {email_data['from_email']}")
        logger.info(f"邮件服务器: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        
        # 发送邮件
        send_mail(**email_data)
        logger.info("邮件发送成功")
        
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def verify_email_code(email, code):
    """验证邮箱验证码"""
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    
    stored_code = redis_client.get(f'email_code:{email}')
    if not stored_code:
        return False
        
    return stored_code.decode() == code 