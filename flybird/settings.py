# SMS 配置
SMS_CONFIG = {
    'USE_VIRTUAL_SMS': True if DEBUG else False,  # 开发环境使用虚拟验证码
    'VIRTUAL_SMS_CODE': '123456',  # 虚拟验证码
    'SMS_EXPIRE_SECONDS': 300,  # 验证码有效期（秒）
    'SMS_COOLDOWN_SECONDS': 60,  # 发送冷却时间（秒）
} 