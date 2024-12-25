from django.core.management.base import BaseCommand
from users.models import User
from users.utils.profile_score import calculate_profile_score

class Command(BaseCommand):
    help = '查看用户档案评分'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='用户手机号')

    def handle(self, *args, **options):
        phone = options['phone']

        try:
            # 直接从数据库获取用户信息
            user = User.objects.get(phone=phone)
            
            # 直接调用评分接口
            score_data = calculate_profile_score(user)
            
            # 打印评分结果
            self.stdout.write('\n档案评分结果:')
            self.stdout.write(f'总分: {score_data["total_score"]}')
            self.stdout.write('\n维度得分:')
            self.stdout.write(f'- 基础维度: {score_data["basic_dimension"]["score"]} (权重: {score_data["basic_dimension"]["weight"]})')
            self.stdout.write(f'- 经验维度: {score_data["experience_dimension"]["score"]} (权重: {score_data["experience_dimension"]["weight"]})')
            self.stdout.write(f'- 能力维度: {score_data["capability_dimension"]["score"]} (权重: {score_data["capability_dimension"]["weight"]})')
            self.stdout.write(f'- 成就维度: {score_data["achievement_dimension"]["score"]} (权重: {score_data["achievement_dimension"]["weight"]})')
            
            if score_data["improvement_suggestions"]:
                self.stdout.write('\n改进建议:')
                for suggestion in score_data["improvement_suggestions"]:
                    self.stdout.write(f'- {suggestion["field"]}: {suggestion["message"]} (影响分数: {suggestion["score_impact"]})')

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'用户不存在: {phone}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'发生错误: {str(e)}')) 