from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import transaction
import os
import json
import logging
from datetime import datetime, date
import requests
from ..models import BasicInfo, WorkExperience, Education, Project, Skill, Language, SocialLink
import uuid
from ...services.ernie import ErnieService
from ...services.resume import ResumeService

# 获取日志记录器
logger = logging.getLogger(__name__)

class ResumeImportView(APIView):
    """简历导入视图"""
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def _parse_date(self, date_str):
        """解析日期字符串"""
        if not date_str:
            return None
        
        # 如果已经是日期对象，直接返回
        if isinstance(date_str, (datetime, date)):
            return date_str if isinstance(date_str, date) else date_str.date()
        
        # 清理日期字符串
        date_str = str(date_str).strip()
        
        # 常见日期格式列表
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y.%m.%d',
            '%Y年%m月%d日',
            '%Y-%m',
            '%Y/%m',
            '%Y.%m',
            '%Y年%m月',
            '%Y'
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                # 如果只有年份，设置为该年的1月1日
                if fmt == '%Y':
                    return date(int(date_str), 1, 1)
                # 如果只有年月，设置为该月的1日
                if fmt in ['%Y-%m', '%Y/%m', '%Y.%m', '%Y年%m月']:
                    return parsed_date.replace(day=1)
                return parsed_date
            except ValueError:
                continue
            
        # 如果所有格式都失败了，尝试提取年份
        try:
            # 匹配4位数字作为年份
            import re
            year_match = re.search(r'\d{4}', date_str)
            if year_match:
                year = int(year_match.group())
                if 1900 <= year <= 2100:  # 合理的年份范围
                    return date(year, 1, 1)
        except:
            pass
        
        # 如果实在无法解析，返回当前日期
        return date.today()

    def _clean_user_data(self, user):
        """清理用户现有数据"""
        logger.info(f"清理用户 {user.id} 的现有数据")
        with transaction.atomic():
            BasicInfo.objects.filter(user=user).delete()
            WorkExperience.objects.filter(user=user).delete()
            Education.objects.filter(user=user).delete()
            Project.objects.filter(user=user).delete()
            Skill.objects.filter(user=user).delete()
            Language.objects.filter(user=user).delete()
            SocialLink.objects.filter(user=user).delete()

    def _import_basic_info(self, user, data):
        """导入基本信息"""
        if not data:
            return
        
        try:
            BasicInfo.objects.create(
                user=user,
                name=data.get('name', ''),
                gender=data.get('gender', ''),
                birth_date=self._parse_date(data.get('birth_date')),
                phone=data.get('phone', ''),
                email=data.get('email', ''),
                location=data.get('location', ''),
                personal_summary=data.get('personal_summary', '')
            )
            logger.info(f"成功导入用户 {user.id} 的基本信息")
        except Exception as e:
            logger.error(f"导入基本信息失败: {str(e)}")
            raise

    def _import_work_experiences(self, user, data_list):
        """导入工作经历"""
        if not data_list:
            return
        
        try:
            for data in data_list:
                WorkExperience.objects.create(
                    user=user,
                    company=data.get('company', ''),
                    position=data.get('position', ''),
                    department=data.get('department', ''),
                    start_date=self._parse_date(data.get('start_date')),
                    end_date=self._parse_date(data.get('end_date')),
                    is_current=data.get('is_current', False),
                    description=data.get('description', ''),
                    achievements=data.get('achievements', ''),
                    technologies=data.get('technologies', '')
                )
            logger.info(f"成功导入用户 {user.id} 的工作经历")
        except Exception as e:
            logger.error(f"导入工作经历失败: {str(e)}")
            raise

    def _import_educations(self, user, data_list):
        """导入教育经历"""
        if not data_list:
            return
        
        try:
            for data in data_list:
                Education.objects.create(
                    user=user,
                    school=data.get('school', ''),
                    major=data.get('major', ''),
                    degree=data.get('degree', 'other'),
                    start_date=self._parse_date(data.get('start_date')),
                    end_date=self._parse_date(data.get('end_date')),
                    is_current=data.get('is_current', False),
                    description=data.get('description', ''),
                    achievements=data.get('achievements', '')
                )
            logger.info(f"成功导入用户 {user.id} 的教育经历")
        except Exception as e:
            logger.error(f"导入教育经历失败: {str(e)}")
            raise

    def _import_projects(self, user, data_list):
        """导入项目经历"""
        if not data_list:
            return
        
        try:
            for data in data_list:
                # 记录原始数据
                logger.info(f"项目数据: {data}")
                
                # 处理日期
                start_date = self._parse_date(data.get('start_date'))
                end_date = self._parse_date(data.get('end_date'))
                
                # 如果没有开始日期，使用结束日期，或者默认使用当前日期
                if not start_date:
                    if end_date:
                        start_date = end_date
                    else:
                        start_date = date.today()
                        end_date = date.today()
                
                # 如果有开始日期但没有结束日期，且不是当前项目
                if start_date and not end_date and not data.get('is_current'):
                    end_date = date.today()
                
                logger.info(f"处理后的日期 - 开始: {start_date}, 结束: {end_date}")
                
                Project.objects.create(
                    user=user,
                    name=data.get('name', ''),
                    role=data.get('role', ''),
                    start_date=start_date,
                    end_date=end_date,
                    is_current=data.get('is_current', False),
                    description=data.get('description', ''),
                    achievement=data.get('achievement', '')
                )
            logger.info(f"成功导入用户 {user.id} 的项目经历")
        except Exception as e:
            logger.error(f"导入项目经历失败: {str(e)}")
            raise

    def _import_skills(self, user, data_list):
        """导入技能特长"""
        if not data_list:
            return
        
        try:
            for data in data_list:
                Skill.objects.create(
                    user=user,
                    name=data.get('name', ''),
                    level=data.get('level', ''),
                    description=data.get('description', ''),
                    projects=data.get('projects', '')
                )
            logger.info(f"成功导入用户 {user.id} 的技能特长")
        except Exception as e:
            logger.error(f"导入技能特长失败: {str(e)}")
            raise

    def _import_languages(self, user, data_list):
        """导入语言能力"""
        if not data_list:
            return
        
        try:
            # 如果是字符串，转换为列表
            if isinstance(data_list, str):
                # 尝试解析 JSON 字符串
                try:
                    data_list = json.loads(data_list)
                except json.JSONDecodeError:
                    # 如果不是 JSON，按逗号分割
                    data_list = [{'name': lang.strip()} for lang in data_list.split(',') if lang.strip()]
            
            # 确保 data_list 是列表
            if not isinstance(data_list, list):
                data_list = [data_list]
            
            for data in data_list:
                # 如果是字符串，转换为字典
                if isinstance(data, str):
                    data = {'name': data.strip()}
                
                logger.info(f"处理语言数据: {data}")
                
                Language.objects.create(
                    user=user,
                    name=data.get('name', ''),
                    proficiency=data.get('proficiency', '熟练'),
                    certification=data.get('certification', ''),
                    score=data.get('score', '')
                )
            logger.info(f"成功导入用户 {user.id} 的语言能力")
        except Exception as e:
            logger.error(f"导入语言能力失败: {str(e)}")
            raise

    def _import_social_links(self, user, data_list):
        """导入社交主页"""
        if not data_list:
            return
        
        try:
            for data in data_list:
                SocialLink.objects.create(
                    user=user,
                    platform=data.get('platform', ''),
                    url=data.get('url', ''),
                    description=data.get('description', '')
                )
            logger.info(f"成功导入用户 {user.id} 的社交主页")
        except Exception as e:
            logger.error(f"导入社交主页失败: {str(e)}")
            raise

    def _parse_resume(self, file_path):
        """调用简历解析服务"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                raise Exception("上传的文件不存在")

            # 检查文件大小
            file_size = os.path.getsize(file_path)
            logger.info(f"文件大小: {file_size} bytes")
            
            # 使用简历解析服务
            resume_service = ResumeService()
            parsed_data = resume_service.parse_resume(file_path)
            
            # 检查头像数据
            logger.info("检查解析结果中的头像数据:")
            if parsed_data:
                # 检查 basic_info 中的头像
                if 'basic_info' in parsed_data:
                    avatar = parsed_data.get('basic_info', {}).get('avatar')
                    logger.info(f"basic_info.avatar: {bool(avatar)}")
                    if avatar:
                        logger.info(f"头像数据类型: {type(avatar)}")
                        if isinstance(avatar, str):
                            logger.info(f"头像数据长度: {len(avatar)}")
                            logger.info(f"头像数据前缀: {avatar[:100] if len(avatar) > 100 else avatar}")
                
                # 检查 result 中的头像
                if 'result' in parsed_data:
                    avatar_data = parsed_data.get('result', {}).get('avatar_data')
                    avatar_url = parsed_data.get('result', {}).get('avatar_url')
                    logger.info(f"result.avatar_data: {bool(avatar_data)}")
                    logger.info(f"result.avatar_url: {bool(avatar_url)}")
                    if avatar_data:
                        logger.info(f"avatar_data类型: {type(avatar_data)}")
                    if avatar_url:
                        logger.info(f"avatar_url: {avatar_url}")
            
            logger.info("简历解析成功")
            return parsed_data

        except Exception as e:
            logger.error(f"简历解析失败: {str(e)}")
            raise Exception(f"简历解析失败: {str(e)}")
        finally:
            try:
                # 清理临时文件
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"临时文件已清理: {file_path}")
            except Exception as e:
                logger.warning(f"清理临时文件失败: {str(e)}")

    def _generate_filename(self, original_filename):
        """生成唯一的文件名"""
        # 获取文件扩展名
        ext = os.path.splitext(original_filename)[1].lower()
        # 生成唯一的文件名
        unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
        return unique_filename

    def post(self, request, *args, **kwargs):
        """解析简历文件"""
        try:
            # 检查文件是否存在
            logger.info(f"接收到文件上传请求，FILES: {request.FILES}")
            if not request.FILES:
                return Response({
                    'code': 400,
                    'message': '请上传文件'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取上传的文件
            file = None
            for field_name, file_obj in request.FILES.items():
                logger.info(f"处理上传文件: {field_name}, {file_obj.name}")
                file = file_obj
                break

            if not file:
                return Response({
                    'code': 400,
                    'message': '请上传文件'
                }, status=status.HTTP_400_BAD_REQUEST)

            file_ext = os.path.splitext(file.name)[1].lower()
            logger.info(f"文件扩展名: {file_ext}")
            logger.info(f"文件类型: {file.content_type}")

            # 检查文件类型
            allowed_types = settings.RESUME_UPLOAD_SETTINGS['ALLOWED_TYPES']
            allowed_extensions = {
                'application/pdf': '.pdf',
                'application/msword': '.doc',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
                'image/jpeg': ['.jpg', '.jpeg'],
                'image/png': '.png'
            }

            # 检查文件类型和扩展名是否匹配
            is_valid = False
            if file.content_type in allowed_types:
                valid_extensions = allowed_extensions[file.content_type]
                if isinstance(valid_extensions, list):
                    is_valid = file_ext in valid_extensions
                else:
                    is_valid = file_ext == valid_extensions
            
            # 特殊处理 PDF 文件
            if file_ext == '.pdf' and (file.content_type == 'application/pdf' or file.content_type == ''):
                is_valid = True

            if not is_valid:
                return Response({
                    'code': 400,
                    'message': '不支持的文件格式'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 检查文件大小
            if file.size > settings.RESUME_UPLOAD_SETTINGS['MAX_SIZE']:
                return Response({
                    'code': 400,
                    'message': f'文件大小超过限制 ({settings.RESUME_UPLOAD_SETTINGS["MAX_SIZE"] / 1024 / 1024}MB)'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 确保目录存在
                upload_dir = f'{settings.RESUME_UPLOAD_SETTINGS["UPLOAD_DIR"]}/{request.user.id}'
                os.makedirs(os.path.join(settings.MEDIA_ROOT, upload_dir), exist_ok=True)
                
                # 生成唯一的文件名
                unique_filename = self._generate_filename(file.name)
                
                # 保存文件
                file_path = default_storage.save(
                    f'{upload_dir}/{unique_filename}',
                    file
                )
                full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
                logger.info(f"文件已保存到: {full_file_path}")

                # 调用简历解析服务
                parsed_data = self._parse_resume(full_file_path)

                # 清理临时文件
                try:
                    default_storage.delete(file_path)
                    logger.info("临时文件已清理")
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")

                return Response({
                    'code': 200,
                    'message': '解析成功',
                    'data': parsed_data
                })

            except Exception as e:
                logger.error(f"处理文件失败: {str(e)}")
                return Response({
                    'code': 500,
                    'message': f'处理文件失败: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"解析简历失败: {str(e)}")
            return Response({
                'code': 500,
                'message': f'解析简历失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        """导入简历数据"""
        try:
            data = request.data
            if not data:
                return Response({
                    'code': 400,
                    'message': '请提供要导入的数据'
                }, status=status.HTTP_400_BAD_REQUEST)

            logger.info("开始导入数据")
            with transaction.atomic():
                # 清理现有数据
                self._clean_user_data(request.user)
                
                # 导入各类数据
                self._import_basic_info(request.user, data.get('basic_info'))
                self._import_work_experiences(request.user, data.get('work_experiences'))
                self._import_educations(request.user, data.get('educations'))
                self._import_projects(request.user, data.get('projects'))
                self._import_skills(request.user, data.get('skills'))
                self._import_languages(request.user, data.get('languages'))
                self._import_social_links(request.user, data.get('social_links'))

            logger.info("数据导入完成")
            return Response({
                'code': 200,
                'message': '导入成功'
            })

        except Exception as e:
            logger.error(f"导入数据失败: {str(e)}")
            return Response({
                'code': 500,
                'message': f'导入数据失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 