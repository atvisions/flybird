from users.services.ernie import ErnieService
import json
import logging
from django.db import transaction
from django.core.cache import cache
import uuid
from django.utils import timezone

logger = logging.getLogger('users')

class ContentQualityService:
    """内容质量服务"""
    
    def __init__(self, user):
        self.user = user
        self.ai = ErnieService()
    
    def analyze_content(self):
        """分析内容质量"""
        try:
            # 获取用户档案数据
            basic_info = self.user.basic_info
            work_experiences = self.user.work_experiences.all()
            
            # 构建提示内容
            content = f"""请以JSON格式分析以下简历内容并提供改进建议。

简历内容：
个人简介：{basic_info.personal_summary}

工作经历：
{self._format_work_experiences(work_experiences)}

请按照以下JSON格式返回分析结果：
{{
    "analysis": {{
        "basic_info": {{
            "score": 80,
            "strengths": ["优点1", "优点2"],
            "weaknesses": ["不足1", "不足2"],
            "suggestions": [
                {{
                    "field": "personal_summary",
                    "current": "当前内容",
                    "suggestion": "改进建议",
                    "example": "示例"
                }}
            ]
        }},
        "work_experience": {{
            "score": 75,
            "strengths": ["优点1", "优点2"],
            "weaknesses": ["不足1", "不足2"],
            "suggestions": [
                {{
                    "field": "responsibilities",
                    "current": "当前描述",
                    "suggestion": "改进建议",
                    "example": "示例"
                }}
            ]
        }}
    }},
    "overall_score": 85,
    "improvement_priority": ["优先改进项1", "优先改进项2"]
}}"""

            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": content
                }
            ]
            
            # 调用 AI
            response = self.ai.generate_response(messages)
            logger.info(f"AI 响应: {response}")  # 添加日志
            
            try:
                analysis = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析失败: {str(e)}")
                logger.error(f"原始响应: {response}")
                # 尝试清理响应文本
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                analysis = json.loads(cleaned_response)
            
            return {
                'code': 200,
                'message': '获取成功',
                'data': {
                    'analysis': analysis,
                    'optimization_available': True
                }
            }
            
        except Exception as e:
            logger.error(f"分析内容失败: {str(e)}")
            return {
                'code': 500,
                'message': str(e),
                'data': None
            }
    
    def optimize_content(self):
        """一键优化内容"""
        try:
            # 获取用户档案数据
            basic_info = self.user.basic_info
            work_experiences = self.user.work_experiences.all()
            
            # 构建提示内容
            content = f"""请优化以下简历内容，并按照指定的JSON格式返回结果。

当前简历内容：
个人简介：{basic_info.personal_summary}

工作经历：
{self._format_work_experiences(work_experiences)}

优化要求：
1. 使用STAR法则描述工作经历
2. 突出关键成就和量化指标
3. 使用专业的行业术语
4. 保持事实准确性

请按照以下JSON格式返回优化结果：
{{
    "optimized_content": {{
        "personal_summary": {{
            "before": "原始内容",
            "after": "优化后的内容",
            "improvements": [
                "改进点1",
                "改进点2"
            ]
        }},
        "work_experiences": [
            {{
                "company": "公司名称",
                "position": "职位",
                "responsibilities": {{
                    "before": "原始描述",
                    "after": "优化后的描述",
                    "improvements": [
                        "改进点1",
                        "改进点2"
                    ]
                }},
                "achievements": {{
                    "before": "原始描述",
                    "after": "优化后的描述",
                    "improvements": [
                        "改进点1",
                        "改进点2"
                    ]
                }}
            }}
        ]
    }},
    "optimization_summary": {{
        "major_improvements": [
            "主要改进1",
            "主要改进2"
        ],
        "professional_score": {{
            "before": 75,
            "after": 90
        }}
    }}
}}"""

            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": content
                }
            ]
            
            # 调用 AI
            response = self.ai.generate_response(messages)
            logger.info(f"优化响应: {response}")  # 添加日志
            
            try:
                optimized = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析失败: {str(e)}")
                logger.error(f"原始响应: {response}")
                # 尝试清理响应文本
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                optimized = json.loads(cleaned_response)
            
            # 更新数据库（可选）
            if 'auto_update' in self.user.profile_layout.layout.get('preferences', {}):
                try:
                    self._update_profile(optimized['optimized_content'])
                    logger.info("自动更新成功")
                except Exception as e:
                    logger.error(f"自动更新失败: {str(e)}")
            
            return {
                'code': 200,
                'message': '优化成功',
                'data': {
                    'optimized_content': optimized['optimized_content'],
                    'optimization_summary': optimized['optimization_summary'],
                    'auto_updated': 'auto_update' in self.user.profile_layout.layout.get('preferences', {})
                }
            }
            
        except Exception as e:
            logger.error(f"优化内容失败: {str(e)}")
            return {
                'code': 500,
                'message': str(e),
                'data': None
            }
    
    def _format_work_experiences(self, work_experiences):
        """格式化工作经历"""
        return "\n".join([
            f"公司：{exp.company}\n"
            f"职位：{exp.position}\n"
            f"部门：{exp.department}\n"
            f"时间：{exp.start_date} - {exp.end_date if not exp.is_current else '至今'}\n"
            f"公司描述：{exp.company_description}\n"
            f"工作职责：{exp.responsibilities}\n"
            f"工作成果：{exp.achievements}\n"
            f"技术栈：{exp.technologies}\n"
            for exp in work_experiences
        ])
    
    def _format_educations(self, educations):
        """格式化教育经历"""
        return "\n".join([
            f"学校：{edu.school}\n"
            f"专业：{edu.major}\n"
            f"学位：{edu.degree}\n"
            f"时间：{edu.start_date} - {edu.end_date if not edu.is_current else '至今'}\n"
            f"描述：{edu.description}\n"
            for edu in educations
        ])
    
    def _format_skills(self, skills):
        """格式化技能特长"""
        return "\n".join([
            f"技能：{skill.name}\n"
            f"等级：{skill.level}\n"
            f"描述：{skill.description}\n"
            f"相关项目：{skill.projects}\n"
            for skill in skills
        ])
    
    def _format_certificates(self, certificates):
        """格式化证书资质"""
        return "\n".join([
            f"证书：{cert.name}\n"
            f"发证机构：{cert.issuing_authority}\n"
            f"获得时间：{cert.issue_date}\n"
            f"描述：{cert.description}\n"
            for cert in certificates
        ])
    
    def _format_languages(self, languages):
        """格式化语言能力"""
        return "\n".join([
            f"语言：{lang.name}\n"
            f"等级：{lang.level}\n"
            f"描述：{lang.description}\n"
            for lang in languages
        ])
    
    def _format_portfolios(self, portfolios):
        """格式化作品展示"""
        return "\n".join([
            f"标题：{port.title}\n"
            f"链接：{port.url}\n"
            f"描述：{port.description}\n"
            f"亮点：{port.highlights}\n"
            for port in portfolios
        ])
    
    def _format_before_after(self, original_exps, optimized_exps):
        """格式化优化前后的对比"""
        result = []
        for orig, opt in zip(original_exps, optimized_exps):
            result.append({
                'company': orig.company,
                'position': orig.position,
                'before': {
                    'responsibilities': orig.responsibilities,
                    'achievements': orig.achievements
                },
                'after': {
                    'responsibilities': opt['responsibilities'],
                    'achievements': opt['achievements']
                }
            })
        return result
    
    def _update_profile(self, optimized_content):
        """更新档案数据"""
        with transaction.atomic():
            # 更新个人简介
            basic_info = self.user.basic_info
            basic_info.personal_summary = optimized_content['personal_summary']['after']
            basic_info.save()
            
            # 更新工作经历
            for exp_data in optimized_content['work_experiences']:
                try:
                    exp = self.user.work_experiences.get(
                        company=exp_data['company'],
                        position=exp_data['position']
                    )
                    exp.responsibilities = exp_data['responsibilities']['after']
                    exp.achievements = exp_data['achievements']['after']
                    exp.save()
                    logger.info(f"更新工作经历: {exp.company}")
                except Exception as e:
                    logger.error(f"更新工作经历失败: {str(e)}") 
    
    def _update_basic_info(self, basic_info_data):
        """更新基本信息"""
        try:
            basic_info = self.user.basic_info
            
            # 更新个人简介
            if 'personal_summary' in basic_info_data:
                basic_info.personal_summary = basic_info_data['personal_summary']['after']
                logger.info(f"更新个人简介: {basic_info.personal_summary[:50]}...")
            
            # 更新其他基本信息字段
            if 'education' in basic_info_data:
                basic_info.education = basic_info_data['education']['after']
                logger.info("更新教育背景")
                
            if 'skills' in basic_info_data:
                basic_info.skills = basic_info_data['skills']['after']
                logger.info("更新技能特长")
            
            basic_info.save()
            logger.info("基本信息更新成功")
            
        except Exception as e:
            logger.error(f"更新基本信息失败: {str(e)}")
            raise
    
    def _update_work_experiences(self, work_experiences_data):
        """更新工作经历"""
        try:
            for exp_data in work_experiences_data:
                try:
                    # 尝试精确匹配
                    exp = self.user.work_experiences.get(
                        company=exp_data['company'],
                        position=exp_data['position']
                    )
                except self.user.work_experiences.model.DoesNotExist:
                    # 如果找不到，尝试模糊匹配
                    logger.info(f"尝试模糊匹配工作经历: {exp_data['company']}")
                    exps = self.user.work_experiences.filter(
                        company__icontains=exp_data['company'].replace('（请填写实际公司名称）', '')
                    )
                    if exps.exists():
                        exp = exps.first()
                        logger.info(f"找到模糊匹配: {exp.company} - {exp.position}")
                    else:
                        # 如果还是找不到，创建新记录
                        logger.info(f"创建新的工作经历记录: {exp_data['company']}")
                        exp = self.user.work_experiences.create(
                            company=exp_data['company'].replace('（请填写实际公司名称）', ''),
                            position=exp_data['position'],
                            start_date=exp_data.get('start_date') or timezone.now().date(),
                            is_current=True
                        )
                
                # 更新各个字段
                if 'responsibilities' in exp_data:
                    exp.responsibilities = exp_data['responsibilities']['after']
                
                if 'achievements' in exp_data:
                    exp.achievements = exp_data['achievements']['after']
                
                if 'company_description' in exp_data:
                    exp.company_description = exp_data['company_description']['after']
                
                if 'technologies' in exp_data:
                    exp.technologies = exp_data['technologies']['after']
                
                if 'department' in exp_data:
                    exp.department = exp_data['department']
                
                exp.save()
                logger.info(f"更新工作经历成功: {exp.company} - {exp.position}")
                
        except Exception as e:
            logger.error(f"更新工作经历失败: {str(e)}")
            raise
    
    def _update_education(self, educations_data):
        """更新教育经历"""
        try:
            for edu_data in educations_data:
                try:
                    # 尝试精确匹配
                    edu = self.user.educations.get(
                        school=edu_data['school'],
                        major=edu_data['major']
                    )
                except self.user.educations.model.DoesNotExist:
                    # 如果找不到，尝试模糊匹配
                    logger.info(f"尝试模糊匹配教育经历: {edu_data['school']} - {edu_data['major']}")
                    edus = self.user.educations.filter(
                        school__icontains=edu_data['school']
                    )
                    if edus.exists():
                        edu = edus.first()
                        logger.info(f"找到模糊匹配: {edu.school} - {edu.major}")
                    else:
                        # 如果还是找不到，创建新记录
                        logger.info(f"创建新的教育经历记录: {edu_data['school']}")
                        edu = self.user.educations.create(
                            school=edu_data['school'],
                            major=edu_data['major'],
                            degree=edu_data.get('degree', '本科'),
                            start_date=timezone.now().date() - timezone.timedelta(days=365*4),  # 默认4年前开始
                            end_date=timezone.now().date(),
                            is_current=False
                        )

                # 更新描述
                if 'description' in edu_data:
                    edu.description = edu_data['description']['after']

                # 更新其他字段
                if 'degree' in edu_data:
                    edu.degree = edu_data['degree']

                edu.save()
                logger.info(f"更新教育经历成功: {edu.school} - {edu.major}")

        except Exception as e:
            logger.error(f"更新教育经历失败: {str(e)}")
            logger.error(f"教育经历数据: {educations_data}")
            raise
    
    def _update_skills(self, skills_data):
        """更新技能特长"""
        try:
            for skill_data in skills_data:
                try:
                    # 尝试精确匹配
                    skill = self.user.skills.get(name=skill_data['name'])
                except self.user.skills.model.DoesNotExist:
                    # 如果找不到，创建新记录
                    logger.info(f"创建新的技能记录: {skill_data['name']}")
                    skill = self.user.skills.create(
                        name=skill_data['name'],
                        level=skill_data.get('level', '熟练')
                    )

                # 更新描述
                if 'description' in skill_data:
                    skill.description = skill_data['description']['after']

                # 更新相关项目
                if 'projects' in skill_data:
                    skill.projects = skill_data['projects']['after']

                # 更新等级
                if 'level' in skill_data:
                    skill.level = skill_data['level']

                skill.save()
                logger.info(f"更新技能成功: {skill.name}")

        except Exception as e:
            logger.error(f"更新技能失败: {str(e)}")
            logger.error(f"技能数据: {skills_data}")
            raise

    def _update_certificates(self, certificates_data):
        """更新证书资质"""
        try:
            for cert_data in certificates_data:
                try:
                    # 尝试精确匹配
                    cert = self.user.certificates.get(name=cert_data['name'])
                except self.user.certificates.model.DoesNotExist:
                    # 如果找不到，创建新记录
                    logger.info(f"创建新的证书记录: {cert_data['name']}")
                    cert = self.user.certificates.create(
                        name=cert_data['name'],
                        issuing_authority=cert_data.get('issuing_authority', ''),
                        issue_date=timezone.now().date()
                    )

                # 更新描述
                if 'description' in cert_data:
                    cert.description = cert_data['description']['after']

                # 更新发证机构
                if 'issuing_authority' in cert_data:
                    cert.issuing_authority = cert_data['issuing_authority']

                cert.save()
                logger.info(f"更新证书成功: {cert.name}")

        except Exception as e:
            logger.error(f"更新证书失败: {str(e)}")
            logger.error(f"证书数据: {certificates_data}")
            raise

    def _update_languages(self, languages_data):
        """更新语言能力"""
        try:
            for lang_data in languages_data:
                try:
                    # 尝试精确匹配
                    lang = self.user.languages.get(name=lang_data['name'])
                except self.user.languages.model.DoesNotExist:
                    # 如果找不到，创建新记录
                    logger.info(f"创建新的语言记录: {lang_data['name']}")
                    lang = self.user.languages.create(
                        name=lang_data['name'],
                        level=lang_data.get('level', '')
                    )

                # 更新描述
                if 'description' in lang_data:
                    lang.description = lang_data['description']['after']

                # 更新等级
                if 'level' in lang_data:
                    lang.level = lang_data['level']

                lang.save()
                logger.info(f"更新语言能力成功: {lang.name}")

        except Exception as e:
            logger.error(f"更新语言能力失败: {str(e)}")
            logger.error(f"语言数据: {languages_data}")
            raise

    def _update_portfolios(self, portfolios_data):
        """更新作品展示"""
        try:
            for port_data in portfolios_data:
                try:
                    # 尝试精确匹配
                    port = self.user.portfolios.get(title=port_data['title'])
                except self.user.portfolios.model.DoesNotExist:
                    # 如果找不到，创建新记录
                    logger.info(f"创建新的作品记录: {port_data['title']}")
                    port = self.user.portfolios.create(
                        title=port_data['title'],
                        url=port_data.get('url', '')
                    )

                # 更新描述
                if 'description' in port_data:
                    port.description = port_data['description']['after']

                # 更新亮点
                if 'highlights' in port_data:
                    port.highlights = port_data['highlights']['after']

                port.save()
                logger.info(f"更新作品成功: {port.title}")

        except Exception as e:
            logger.error(f"更新作品失败: {str(e)}")
            logger.error(f"作品数据: {portfolios_data}")
            raise
    
    def preview_optimization(self):
        """预览优化结果"""
        try:
            # 获取所有档案数据
            basic_info = self.user.basic_info
            work_experiences = self.user.work_experiences.all()
            educations = self.user.educations.all()
            skills = self.user.skills.all()
            certificates = self.user.certificates.all()
            languages = self.user.languages.all()
            portfolios = self.user.portfolios.all()
            
            # 计算年龄
            age = None
            if basic_info.birth_date:
                today = timezone.now().date()
                age = today.year - basic_info.birth_date.year - ((today.month, today.day) < (basic_info.birth_date.month, basic_info.birth_date.day))
            
            # 构建当前简历内容
            current_content = f"""基本信息：
姓名：{basic_info.name or '未填写'}
性别：{basic_info.get_gender_display() if basic_info.gender else '未填写'}
年龄：{f"{age}岁" if age else '未填写'}
所在地：{basic_info.location or '未填写'}
邮箱：{basic_info.email or '未填写'}
电话：{basic_info.phone or '未填写'}

个人简介：
{basic_info.personal_summary or '未填写'}

工作经历：
{self._format_work_experiences(work_experiences)}

教育经历：
{self._format_educations(educations)}

技能特长：
{self._format_skills(skills)}

证书资质：
{self._format_certificates(certificates)}

语言能力：
{self._format_languages(languages)}

作品展示：
{self._format_portfolios(portfolios)}"""

            # 构建提示内容
            prompt = f"""作为一位专业的简历优化专家，请对以下简历内容进行全面优化。
严格按照JSON格式返回优化建议，必须包含所有字段。

当前简历内容：
{current_content}

请返回以下格式的JSON：
{{
    "preview": {{
        "basic_info": {{
            "personal_summary": {{
                "before": "当前内容",
                "after": "优化后的内容",
                "changes": ["改进点1", "改进点2"]
            }}
        }},
        "work_experiences": [
            {{
                "company": "公司名称",
                "position": "职位名称",
                "responsibilities": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }},
                "achievements": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ],
        "educations": [
            {{
                "school": "学校名称",
                "major": "专业名称",
                "degree": "学位",
                "description": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ],
        "skills": [
            {{
                "name": "技能名称",
                "level": "掌握程度",
                "description": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ],
        "certificates": [
            {{
                "name": "证书名称",
                "description": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ],
        "languages": [
            {{
                "name": "语言名称",
                "level": "掌握程度",
                "description": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ],
        "portfolios": [
            {{
                "title": "作品标题",
                "description": {{
                    "before": "当前描述",
                    "after": "优化后的描述",
                    "changes": ["改进点1", "改进点2"]
                }}
            }}
        ]
    }},
    "summary": {{
        "key_improvements": ["核心改进点1", "核心改进点2"],
        "expected_benefits": ["预期收益1", "预期收益2"]
    }}
}}"""

            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # 调用 AI
            try:
                response = self.ai.generate_response(messages)
                logger.info(f"AI 响应: {response}")
                
                # 清理响应文本
                cleaned_response = response.strip()
                
                # 处理可能的 markdown 代码块
                if "```" in cleaned_response:
                    # 提取 ``` 之间的内容
                    start = cleaned_response.find("```") + 3
                    end = cleaned_response.rfind("```")
                    if start < end:
                        # 如果有语言标识符（如 ```json），跳过它
                        if cleaned_response[start:].startswith("json\n"):
                            start += 5
                        cleaned_response = cleaned_response[start:end].strip()
                
                # 移除所有前导和尾随空白
                cleaned_response = cleaned_response.strip()
                
                try:
                    # 尝试解析 JSON
                    result = json.loads(cleaned_response)
                    logger.info("JSON 解析成功")
                    
                    # 生成优化ID并保存到缓存
                    optimization_id = str(uuid.uuid4())
                    cache.set(
                        f"profile_optimization_{optimization_id}",
                        result,
                        timeout=3600  # 1小时过期
                    )
                    
                    # 在返回数据中添加优化ID
                    result['optimization_id'] = optimization_id
                    
                    return {
                        'code': 200,
                        'message': '获取优化预览成功',
                        'data': result
                    }
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON 解析失败: {str(e)}")
                    logger.error(f"原始响应: {response}")
                    logger.error(f"清理后响应: {cleaned_response}")
                    # 尝试修复常见的 JSON 格式问题
                    try:
                        # 替换单引号为双引号
                        cleaned_response = cleaned_response.replace("'", '"')
                        # 确保布尔值是小写的
                        cleaned_response = cleaned_response.replace("True", "true").replace("False", "false")
                        result = json.loads(cleaned_response)
                        logger.info("JSON 修复并解析成功")
                        
                        # 生成优化ID并保存到缓存
                        optimization_id = str(uuid.uuid4())
                        cache.set(
                            f"profile_optimization_{optimization_id}",
                            result,
                            timeout=3600
                        )
                        
                        result['optimization_id'] = optimization_id
                        return {
                            'code': 200,
                            'message': '获取优化预览成功',
                            'data': result
                        }
                    except:
                        return {
                            'code': 500,
                            'message': f'AI 返回格式错误: {str(e)}',
                            'data': None
                        }
                
            except Exception as e:
                logger.error(f"调用 AI 失败: {str(e)}")
                return {
                    'code': 500,
                    'message': f'AI 服务异常: {str(e)}',
                    'data': None
                }
                
        except Exception as e:
            logger.error(f"获取优化预览失败: {str(e)}")
            return {
                'code': 500,
                'message': str(e),
                'data': None
            }
    
    def apply_optimization(self, optimization_id):
        """应用优化结果"""
        try:
            logger.info(f"尝试应用优化ID: {optimization_id}")
            
            # 从缓存获取优化数据
            optimized = cache.get(f"profile_optimization_{optimization_id}")
            logger.info(f"从缓存获取的数据: {optimized}")
            
            if not optimized:
                logger.error(f"缓存中找不到优化ID: {optimization_id}")
                raise Exception("优化结果已过期，请重新获取")
            
            with transaction.atomic():
                # 更新基本信息
                if 'basic_info' in optimized['preview']:
                    self._update_basic_info(optimized['preview']['basic_info'])
                
                # 更新工作经历
                if 'work_experiences' in optimized['preview']:
                    self._update_work_experiences(optimized['preview']['work_experiences'])
                
                # 更新教育经历
                if 'educations' in optimized['preview']:
                    self._update_education(optimized['preview']['educations'])
                
                # 更新技能特长
                if 'skills' in optimized['preview']:
                    self._update_skills(optimized['preview']['skills'])
                
                # 更新证书资质
                if 'certificates' in optimized['preview']:
                    self._update_certificates(optimized['preview']['certificates'])
                
                # 更新语言能力
                if 'languages' in optimized['preview']:
                    self._update_languages(optimized['preview']['languages'])
                
                # 更新作品展示
                if 'portfolios' in optimized['preview']:
                    self._update_portfolios(optimized['preview']['portfolios'])
                
                return {
                    'code': 200,
                    'message': '应用优化成功',
                    'data': {
                        'updated_fields': {
                            'basic_info': {
                                'personal_summary': True if 'basic_info' in optimized['preview'] else False,
                                'education': False,
                                'skills': False
                            },
                            'work_experiences': {
                                'company': True if 'work_experiences' in optimized['preview'] else False,
                                'position': True if 'work_experiences' in optimized['preview'] else False,
                                'department': True if 'work_experiences' in optimized['preview'] else False,
                                'company_description': True if 'work_experiences' in optimized['preview'] else False,
                                'responsibilities': True if 'work_experiences' in optimized['preview'] else False,
                                'achievements': True if 'work_experiences' in optimized['preview'] else False,
                                'technologies': True if 'work_experiences' in optimized['preview'] else False
                            },
                            'educations': {
                                'school': True if 'educations' in optimized['preview'] else False,
                                'major': True if 'educations' in optimized['preview'] else False,
                                'degree': True if 'educations' in optimized['preview'] else False,
                                'description': True if 'educations' in optimized['preview'] else False
                            },
                            'skills': {
                                'name': True if 'skills' in optimized['preview'] else False,
                                'level': True if 'skills' in optimized['preview'] else False,
                                'description': True if 'skills' in optimized['preview'] else False,
                                'projects': True if 'skills' in optimized['preview'] else False
                            },
                            'certificates': {
                                'name': True if 'certificates' in optimized['preview'] else False,
                                'description': True if 'certificates' in optimized['preview'] else False,
                                'issuing_authority': True if 'certificates' in optimized['preview'] else False
                            },
                            'languages': {
                                'name': True if 'languages' in optimized['preview'] else False,
                                'level': True if 'languages' in optimized['preview'] else False,
                                'description': True if 'languages' in optimized['preview'] else False
                            },
                            'portfolios': {
                                'title': True if 'portfolios' in optimized['preview'] else False,
                                'description': True if 'portfolios' in optimized['preview'] else False,
                                'highlights': True if 'portfolios' in optimized['preview'] else False
                            }
                        }
                    }
                }
                
        except Exception as e:
            logger.error(f"应用优化失败: {str(e)}")
            logger.error(f"优化数据: {optimized}")
            raise 