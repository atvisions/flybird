import requests
import json
import logging
from django.conf import settings
import time
import re

logger = logging.getLogger('users')

class ErnieService:
    """文心一言服务"""
    
    def __init__(self):
        self.api_key = settings.ERNIE_API_KEY
        self.secret_key = settings.ERNIE_SECRET_KEY
        self.access_token = self._get_access_token()
        self.api_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
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
        max_retries = 2  # 减少重试次数
        timeout = (10, 20)  # 连接超时10秒，读取超时20秒
        retry_count = 0
        retry_delay = 1  # 初始重试延迟1秒
        
        while retry_count < max_retries:
            try:
                logger.info(f"开始调用文心一言API (尝试 {retry_count + 1}/{max_retries})")
                
                url = f"{self.api_url}?access_token={self.access_token}"
                
                payload = {
                    "messages": messages,
                    "temperature": 0.1,  # 降低随机性，提高响应速度
                    "top_p": 0.95,
                    "penalty_score": 1.0,
                    "system": "你是一个简历解析助手。你的任务是将简历文本解析为结构化的JSON数据。请确保返回的是纯JSON格式，不要包含任何注释、换行或特殊字符。所有日期必须是YYYY-MM-DD格式。"
                }
                
                with requests.Session() as session:
                    response = session.post(
                        url, 
                        headers=self.headers,
                        json=payload,
                        timeout=timeout,
                        verify=True
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    if "result" in result:
                        content = result["result"]
                        logger.info("API返回原始响应: %s", content)
                        
                        if isinstance(content, str):
                            content = content.replace('```json', '').replace('```', '').strip()
                            try:
                                return json.loads(content)
                            except json.JSONDecodeError as e:
                                logger.error(f"JSON解析错误: {str(e)}")
                                logger.error(f"待解析内容: {content}")
                                raise
                        elif isinstance(content, dict):
                            return content
                        else:
                            raise Exception(f"意外的返回类型: {type(content)}")
                    else:
                        error_msg = result.get("error_msg", "未知错误")
                        logger.error(f"API返回错误: {result}")
                        
                        if "token" in error_msg.lower() or "auth" in error_msg.lower():
                            self.access_token = self._get_access_token()
                            retry_count += 1
                            time.sleep(retry_delay)
                            continue
                        
                        raise Exception(error_msg)
                    
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"请求超时，等待 {retry_delay} 秒后进行第 {retry_count + 1} 次重试")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("请求超时，已达到最大重试次数")
                    raise Exception("请求超时，请稍后重试")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"请求异常，等待 {retry_delay} 秒后进行第 {retry_count + 1} 次重试")
                    time.sleep(retry_delay)
                    continue
                raise Exception(f"请求失败: {str(e)}")
                
            except Exception as e:
                logger.error(f"文心一言API调用失败: {str(e)}")
                logger.error(f"错误详情: {type(e).__name__}")
                raise
    
    def parse_resume(self, text):
        """解析简历文本"""
        messages = [{
            "role": "user",
            "content": f"""请解析以下简历文本，并返回JSON格式的结果：

{text}

请按照以下格式返回数据：
{{
    "basic_info": {{
        "name": "姓名",
        "gender": "性别",
        "birth_date": "出生日期（YYYY-MM-DD格式）",
        "phone": "电话",
        "email": "邮箱",
        "location": "所在地",
        "personal_summary": "个人总结"
    }},
    "work_experiences": [
        {{
            "company": "公司名称",
            "position": "职位",
            "department": "部门",
            "start_date": "开始日期（YYYY-MM-DD格式）",
            "end_date": "结束日期（YYYY-MM-DD格式）",
            "is_current": false,
            "description": "工作描述",
            "achievements": "工作成就",
            "technologies": "使用的技术"
        }}
    ],
    "educations": [
        {{
            "school": "学校名称",
            "major": "专业",
            "degree": "学位",
            "start_date": "开始日期（YYYY-MM-DD格式）",
            "end_date": "结束日期（YYYY-MM-DD格式）",
            "is_current": false,
            "description": "教育描述",
            "achievements": "教育成就"
        }}
    ],
    "projects": [
        {{
            "name": "项目名称",
            "role": "担任角色",
            "start_date": "开始日期（YYYY-MM-DD格式）",
            "end_date": "结束日期（YYYY-MM-DD格式）",
            "is_current": false,
            "description": "项目描述",
            "achievement": "项目成就"
        }}
    ],
    "skills": [
        {{
            "name": "技能名称",
            "level": "技能等级",
            "description": "技能描述",
            "projects": "相关项目"
        }}
    ],
    "languages": [
        {{
            "name": "语言名称",
            "proficiency": "熟练程度",
            "certification": "语言证书",
            "score": "分数"
        }}
    ],
    "social_links": [
        {{
            "platform": "平台名称",
            "url": "链接地址",
            "description": "描述"
        }}
    ]
}}

注意：
1. 如果某个字段没有对应的信息，请返回空字符串""
2. 日期必须是YYYY-MM-DD格式，如果无法确定具体日期，请返回空字符串""
3. 请确保返回的是标准的JSON格式，不要包含任何注释或特殊字符
4. 如果某个数组没有数据，请返回空数组[]
"""
        }]
        
        return self.generate_response(messages) 