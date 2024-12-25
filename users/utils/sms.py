from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import logging

logger = logging.getLogger(__name__)

class AliyunSMS:
    def __init__(self):
        self.access_key_id = settings.ALIYUN['ACCESS_KEY_ID']
        self.access_key_secret = settings.ALIYUN['ACCESS_KEY_SECRET']
        self.sign_name = settings.ALIYUN['SMS_SIGN_NAME']
        self.region = "cn-hangzhou"
        self.client = AcsClient(self.access_key_id, self.access_key_secret, self.region)

    def send_code(self, phone, code, template_code):
        """
        发送验证码
        :param phone: 手机号
        :param code: 验证码
        :param template_code: 短信模板CODE
        :return: (bool, str) - (是否成功, 错误信息)
        """
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', self.sign_name)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', json.dumps({'code': code}))

        try:
            response = self.client.do_action_with_exception(request)
            response = json.loads(response)
            logger.info(f"Aliyun SMS response: {response}")
            
            if response.get('Code') == 'OK':
                return True, None
            return False, response.get('Message', '发送失败')
            
        except Exception as e:
            logger.error(f"Send SMS error: {str(e)}")
            return False, str(e)

def send_sms(phone, code, scene):
    """
    发送短信验证码的统一接口
    :param phone: 手机号
    :param code: 验证码
    :param scene: 场景类型(register/login/reset_password/change_phone)
    :return: (bool, str) - (是否成功, 错误信息)
    """
    sms = AliyunSMS()
    template_code = settings.ALIYUN['SMS_TEMPLATES'].get(scene)
    if not template_code:
        logger.error(f"Invalid SMS scene type: {scene}")
        return False, '无效的验证码类型'
    
    logger.info(f"Sending SMS code to {phone}, scene: {scene}")
    success, error_msg = sms.send_code(phone, code, template_code)
    
    if success:
        logger.info(f"Successfully sent SMS code to {phone}")
    else:
        logger.error(f"Failed to send SMS code to {phone}: {error_msg}")
    
    return success, error_msg