import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger('users')

class ErnieService:
    """文心一言服务"""
    
    def __init__(self):
        self.api_key = settings.ERNIE_API_KEY
        self.secret_key = settings.ERNIE_SECRET_KEY
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        """获取access_token"""
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        try:
            response = requests.post(url, params=params)
            result = response.json()
            return result.get('access_token')
        except Exception as e:
            logger.error(f"获取access_token失败: {str(e)}")
            raise
    
    def generate_response(self, messages):
        """生成回复"""
        try:
            logger.info("开始调用文心一言API")
            logger.info(f"发送消息: {messages}")
            
            url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={self.access_token}"
            
            # 转换消息格式
            payload = {
                "messages": [
                    {
                        "role": msg["role"],
                        "content": msg["content"]
                    } for msg in messages
                ]
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                url, 
                headers=headers,
                data=json.dumps(payload)
            )
            
            result = response.json()
            logger.info("API 调用成功")
            
            if "result" in result:
                return result["result"]
            else:
                logger.error(f"API返回错误: {result}")
                raise Exception(result.get("error_msg", "未知错误"))
                
        except Exception as e:
            logger.error(f"文心一言API调用失败: {str(e)}")
            logger.error(f"错误详情: {type(e).__name__}")
            raise 