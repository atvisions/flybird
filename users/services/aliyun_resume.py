import os
import json
import logging
import base64
import urllib3
import ssl

logger = logging.getLogger(__name__)

class AliyunResumeService:
    def __init__(self):
        self.app_code = os.getenv('ALIYUN_APP_CODE')
        self.host = "https://aliprofile.market.alicloudapi.com"
        self.path = "/ResumeProfiler"
        
        self.http = urllib3.PoolManager(
            cert_reqs=ssl.CERT_NONE,
            retries=urllib3.Retry(3, backoff_factor=0.5)
        )
    
    def parse_resume(self, file_path):
        """
        解析简历文件
        :param file_path: 简历文件路径
        :return: 解析后的JSON数据
        """
        try:
            # 读取文件内容并转换为base64
            with open(file_path, 'rb') as f:
                file_content = f.read()
                file_content_base64 = base64.b64encode(file_content).decode('utf-8')
            
            # 准备请求参数
            payload = {
                'file_name': os.path.basename(file_path),
                'file_cont': file_content_base64,
                'need_avatar': 0
            }
            
            logger.info(f"Sending request to {self.host}{self.path}")
            
            # 发送请求
            response = self.http.request(
                'POST',
                self.host + self.path,
                body=json.dumps(payload).encode('utf-8'),
                headers={
                    'Authorization': f'APPCODE {self.app_code}',
                    'Content-Type': 'application/json; charset=UTF-8'
                },
                timeout=30.0
            )
            
            # 解析响应
            result = json.loads(response.data.decode('utf-8'))
            logger.info(f"API Response: {result}")
            
            if result.get('status', {}).get('code') == 200:
                return self._format_response(result.get('result', {}))
            else:
                error_msg = f"Resume parsing failed: {result.get('status', {}).get('message')} (Code: {result.get('status', {}).get('code')})"
                logger.error(error_msg)
                return None
                
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            return None
            
    def _format_response(self, data):
        """
        格式化阿里云返回的数据为统一格式
        """
        try:
            # 基本信息
            basic_info = {
                'name': data.get('name', ''),
                'gender': data.get('gender', ''),
                'birth_date': '',  # 阿里云API没有直接返回出生日期
                'phone': data.get('phone', ''),
                'email': data.get('email', ''),
                'location': data.get('expect_jlocation', ''),
                'summary': data.get('cont_my_desc', '')
            }
            
            # 工作经历
            work_experiences = []
            for job in data.get('job_exp_objs', []):
                work_experiences.append({
                    'company': job.get('job_cpy', ''),
                    'position': job.get('job_position', ''),
                    'start_date': job.get('start_date', ''),
                    'end_date': job.get('end_date', ''),
                    'description': job.get('job_content', ''),
                    'achievements': []  # 阿里云API没有单独的成就字段
                })
            
            # 教育经历
            education = []
            for edu in data.get('education_objs', []):
                education.append({
                    'school': edu.get('edu_college', ''),
                    'major': edu.get('edu_major', ''),
                    'degree': edu.get('edu_degree', ''),
                    'start_date': edu.get('start_date', ''),
                    'end_date': edu.get('end_date', '')
                })
            
            # 项目经历
            projects = []
            for proj in data.get('proj_exp_objs', []):
                projects.append({
                    'name': proj.get('proj_name', ''),
                    'role': proj.get('proj_position', ''),
                    'start_date': proj.get('start_date', ''),
                    'end_date': proj.get('end_date', ''),
                    'description': proj.get('proj_content', ''),
                    'achievements': []
                })
            
            # 技能
            skills = [skill.get('skills_name', '') for skill in data.get('skills_objs', [])]
            
            # 语言能力
            languages = [lang.get('lang_name', '') for lang in data.get('lang_objs', [])]
            
            # 社交链接 - 从工作经历和项目经历中提取URL
            social_links = []
            
            return {
                'basic_info': basic_info,
                'work_experiences': work_experiences,
                'education': education,
                'projects': projects,
                'skills': skills,
                'languages': languages,
                'social_links': social_links
            }
            
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            return None 