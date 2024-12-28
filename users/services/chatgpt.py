from openai import OpenAI
import logging
from django.conf import settings
import os

logger = logging.getLogger('users')

class ChatGPTService:
    """ChatGPT 服务"""
    
    def __init__(self):
        # 设置环境变量代理
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url="https://api.openai.com/v1",  # 添加基础 URL
            timeout=30.0  # 设置超时时间
        )
        self.model = settings.OPENAI_MODEL
    
    def generate_response(self, messages):
        """生成回复"""
        try:
            logger.info("开始调用 ChatGPT API")
            logger.info(f"使用模型: {self.model}")
            logger.info(f"发送消息: {messages}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            logger.info("API 调用成功")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"ChatGPT API 调用失败: {str(e)}")
            logger.error(f"错误详情: {type(e).__name__}")
            raise 