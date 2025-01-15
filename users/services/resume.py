import logging
from .aliyun_resume import AliyunResumeService
import os

logger = logging.getLogger('users')

class ResumeService:
    """简历解析服务"""
    
    def __init__(self):
        self.aliyun_service = AliyunResumeService()
    
    def parse_resume(self, file_path):
        """解析简历"""
        try:
            # 直接使用阿里云解析服务
            result = self.aliyun_service.parse_resume(file_path)
            if result:
                logger.info("简历解析成功")
                return result
            else:
                raise Exception("简历解析失败")
            
        except Exception as e:
            logger.error(f"简历解析失败: {str(e)}")
            raise
        finally:
            # 清理临时文件
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"临时文件已清理: {file_path}")
            except Exception as e:
                logger.error(f"清理临时文件失败: {str(e)}") 