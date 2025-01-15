import requests
import logging
from django.conf import settings
from PIL import Image
import pytesseract
import pdf2image
import io

logger = logging.getLogger('users')

class OCRService:
    """OCR服务"""
    
    def __init__(self):
        self.api_key = settings.BAIDU_OCR_API_KEY
        self.secret_key = settings.BAIDU_OCR_SECRET_KEY
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
    
    def extract_text(self, file_path):
        """提取文本"""
        try:
            # 如果是PDF，先转换为图片
            if file_path.lower().endswith('.pdf'):
                images = pdf2image.convert_from_path(file_path)
                text = ""
                for image in images:
                    # 使用pytesseract进行本地OCR
                    text += pytesseract.image_to_string(image, lang='chi_sim') + "\n"
                return text
            
            # 如果是图片，直接OCR
            elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                # 使用百度OCR API
                url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={self.access_token}"
                
                with open(file_path, 'rb') as f:
                    img = f.read()
                
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {'image': base64.b64encode(img).decode()}
                
                response = requests.post(url, headers=headers, data=data)
                result = response.json()
                
                if 'words_result' in result:
                    return '\n'.join([item['words'] for item in result['words_result']])
                else:
                    raise Exception(f"OCR识别失败: {result.get('error_msg', '未知错误')}")
            
            else:
                raise Exception("不支持的文件格式")
                
        except Exception as e:
            logger.error(f"文本提取失败: {str(e)}")
            raise 