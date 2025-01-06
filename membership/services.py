from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.db import transaction
import time
import random
import logging
import traceback
from alipay import AliPay
from .models import MembershipTier, MembershipOrder, UserMembership, PointRule, UserPoint, PointRecord

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',
)
logger = logging.getLogger('')

class MembershipService:
    """会员服务"""
    @classmethod
    def get_user_privileges(cls, user):
        """获取用户权益"""
        if not user.is_authenticated:
            return cls.get_default_privileges()

        membership = getattr(user, 'membership', None)
        if not membership or not membership.tier:
            return cls.get_default_privileges()

        # 检查会员是否过期
        if membership.expire_time and membership.expire_time < timezone.now():
            return cls.get_default_privileges()

        # 获取会员权益
        privileges = {}
        for tier_privilege in membership.tier.privileges.select_related('privilege').all():
            privileges[tier_privilege.privilege.key] = tier_privilege.value

        return privileges

    @classmethod
    def get_default_privileges(cls):
        """获取默认权益"""
        default_tier = MembershipTier.objects.filter(is_default=True).first()
        if not default_tier:
            return {}

        privileges = {}
        for tier_privilege in default_tier.privileges.select_related('privilege').all():
            privileges[tier_privilege.privilege.key] = tier_privilege.value

        return privileges

    @classmethod
    def check_privilege(cls, user, privilege_key):
        """检查用户是否拥有某项权益"""
        privileges = cls.get_user_privileges(user)
        return privileges.get(privilege_key, False)

class PaymentService:
    """支付服务"""
    
    def __init__(self):
        self.alipay = self._init_alipay()
    
    def _init_alipay(self):
        """初始化支付宝客户端"""
        try:
            # 读取密钥文件
            with open(settings.ALIPAY_CONFIG['PRIVATE_KEY_PATH']) as f:
                app_private_key_string = f.read()
            
            with open(settings.ALIPAY_CONFIG['PUBLIC_KEY_PATH']) as f:
                alipay_public_key_string = f.read()
            
            logger.info("成功读取支付宝密钥文件")
            
            # 创建支付宝客户端
            alipay = AliPay(
                appid=settings.ALIPAY_CONFIG['APP_ID'],
                app_notify_url=settings.ALIPAY_CONFIG['NOTIFY_URL'],
                app_private_key_string=app_private_key_string,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",
                debug=settings.ALIPAY_CONFIG['DEBUG']
            )
            
            logger.info("成功创建支付宝客户端")
            return alipay
            
        except Exception as e:
            logger.error(f"初始化支付宝客户端失败: {str(e)}")
            logger.error(f"错误详情: {e.__class__.__name__}")
            raise
    
    def create_payment(self, order):
        """创建支付链接"""
        try:
            logger.info(f"开始创建支付链接: 订单号={order.order_no}")
            logger.info(f"支付金额: {float(order.amount)}")
            
            # 构建商品信息
            subject = f'飞鸟简历 - {order.tier.name}'
            body = f'{order.days}天会员服务'
            
            # 生成支付参数
            order_string = self.alipay.api_alipay_trade_page_pay(
                out_trade_no=order.order_no,
                total_amount=float(order.amount),
                subject=subject,
                body=body,
                return_url=settings.ALIPAY_CONFIG['RETURN_URL'],
                notify_url=settings.ALIPAY_CONFIG['NOTIFY_URL'],
                # 添加额外参数
                timeout_express='15m',  # 订单有效期15分钟
                product_code='FAST_INSTANT_TRADE_PAY'  # 固定值
            )
            
            # 生成完整支付URL
            payment_url = f"{settings.ALIPAY_CONFIG['SANDBOX_URL']}?{order_string}"
            
            logger.info(f"生成支付链接成功: {payment_url}")
            return payment_url
                
        except Exception as e:
            logger.error(f"创建支付链接失败: {str(e)}")
            logger.error(f"错误详情: {e.__class__.__name__}")
            raise

    @classmethod
    def create_order(cls, user, tier, duration, payment_method='alipay'):
        """创建订单"""
        try:
            # 计算订单金额
            if duration == 'monthly':
                amount = tier.price_monthly
                days = 30
            elif duration == 'quarterly':
                amount = tier.price_quarterly
                days = 90
            elif duration == 'yearly':
                amount = tier.price_yearly
                days = 365
            else:
                raise ValueError('Invalid duration')

            # 创建订单记录
            order = MembershipOrder.objects.create(
                user=user,
                tier=tier,
                amount=amount,
                days=days,
                payment_method=payment_method,
                status='pending'
            )

            # 根据支付方式创建支付
            if payment_method == 'alipay':
                payment_url = cls.create_alipay_payment(order)
            else:
                raise ValueError('Unsupported payment method')

            return {
                'order_no': order.order_no,
                'amount': float(order.amount),
                'payment_url': payment_url
            }

        except Exception as e:
            logger.error(f"订单创建失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise ValueError(f'Order creation failed: {str(e)}')

    @classmethod
    def create_alipay_payment(cls, order):
        """创建支付宝支付"""
        try:
            client = cls.create_alipay_client()
            
            # 创建支付订单
            order_string = client.api_alipay_trade_page_pay(
                out_trade_no=order.order_no,
                total_amount=float(order.amount),
                subject=f'会员订阅-{order.tier.name}',
                return_url=settings.PAYMENT_CONFIG['alipay']['return_url'],
                notify_url=settings.PAYMENT_CONFIG['alipay']['notify_url']
            )
            
            # 生成支付链接
            if settings.PAYMENT_CONFIG['alipay']['debug']:
                pay_url = f"{settings.PAYMENT_CONFIG['alipay']['server_url']}?{order_string}"
            else:
                pay_url = f"https://openapi.alipay.com/gateway.do?{order_string}"
                
            return pay_url
            
        except Exception as e:
            cls.logger.error(f"创建支付宝支付失败: {str(e)}")
            cls.logger.error(traceback.format_exc())
            raise ValueError('Payment creation failed')

    @classmethod
    def complete_order(cls, order):
        """完成订单"""
        try:
            # 检查订单状态
            cls.logger.info(f"开始处理订单: {order.order_no}")
            cls.logger.info(f"当前状态: {order.status}")
            
            if order.status != 'pending':
                cls.logger.info(f"订单状态不是待支付，跳过处理")
                return False

            with transaction.atomic():
                # 更新订单状态
                order.status = 'paid'
                order.paid_time = timezone.now()
                order.save()
                
                cls.logger.info(f"订单状态已更新为已支付")

                # 更新会员信息
                membership, created = UserMembership.objects.get_or_create(
                    user=order.user,
                    defaults={'tier': order.tier}
                )
                
                # 更新会员等级和到期时间
                membership.tier = order.tier
                membership.extend_membership(order.days)
                membership.save()
                
                cls.logger.info(f"会员信息更新成功")
                cls.logger.info(f"用户: {order.user.phone}")
                cls.logger.info(f"会员等级: {membership.tier.name}")
                cls.logger.info(f"到期时间: {membership.expire_time}")

            return True

        except Exception as e:
            cls.logger.error(f"完成订单失败: {str(e)}")
            cls.logger.error(traceback.format_exc())
            return False

    @classmethod
    def verify_alipay_payment(cls, data):
        """验证支付宝支付结果"""
        try:
            cls.logger.info("\n" + "="*50)
            cls.logger.info("开始验证支付宝签名")
            cls.logger.info(f"验证数据: \n{data}")
            
            # 记录关键参数
            cls.logger.info("关键参数:")
            cls.logger.info(f"订单: {data.get('out_trade_no')}")
            cls.logger.info(f"交易号: {data.get('trade_no')}")
            cls.logger.info(f"交易状态: {data.get('trade_status')}")
            cls.logger.info(f"签名: {data.get('sign')}")
            cls.logger.info(f"签��类型: {data.get('sign_type')}")
            
            client = cls.create_alipay_client()
            
            # 验证签名
            sign = data.pop('sign', None)
            sign_type = data.pop('sign_type', None)
            
            if sign and sign_type:
                success = client.verify(data, sign)
                if success:
                    cls.logger.info("签名验证成功")
                    # 恢复签名数据
                    data['sign'] = sign
                    data['sign_type'] = sign_type
                    return data
                else:
                    cls.logger.error("签名验证失败")
                    cls.logger.error("验证参数:")
                    cls.logger.error(f"使用的公钥文件: {settings.PAYMENT_CONFIG['alipay']['public_key_path']}")
                    cls.logger.error(f"支付宝应用ID: {settings.PAYMENT_CONFIG['alipay']['app_id']}")
            else:
                cls.logger.error("缺少签名数据")
                cls.logger.error(f"sign: {sign}")
                cls.logger.error(f"sign_type: {sign_type}")
                
            return None
                
        except Exception as e:
            cls.logger.error(f"验证过程异常: {str(e)}")
            cls.logger.error(f"异常详情: \n{traceback.format_exc()}")
            return None

class PointService:
    """积分服务"""
    @classmethod
    def add_points(cls, user, event_type, description=None):
        """添加积分"""
        rule = PointRule.objects.filter(
            event_type=event_type,
            is_active=True
        ).first()
        
        if not rule:
            return None
            
        with transaction.atomic():
            user_point, _ = UserPoint.objects.get_or_create(user=user)
            
            # 更新用户积分
            user_point.balance += rule.points
            user_point.total_earned += rule.points
            user_point.save()
            
            # 创建积分记录
            record = PointRecord.objects.create(
                user=user,
                rule=rule,
                points=rule.points,
                balance=user_point.balance,
                event_type=event_type,
                description=description or rule.description
            )
            
            return record
            
    @classmethod
    def deduct_points(cls, user, points, event_type, description):
        """扣除积分"""
        with transaction.atomic():
            user_point = UserPoint.objects.select_for_update().get(user=user)
            
            # 检查积分是否足够
            if user_point.balance < points:
                raise ValueError('积分不足')
                
            # 更新用户积分
            user_point.balance -= points
            user_point.total_spent += points
            user_point.save()
            
            # 创建积分记录
            record = PointRecord.objects.create(
                user=user,
                points=-points,
                balance=user_point.balance,
                event_type=event_type,
                description=description
            )
            
            return record 