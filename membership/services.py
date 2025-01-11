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
import textwrap

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
    logger = logging.getLogger('membership')  # 添加类级别的 logger
    
    def __init__(self):
        self.alipay = self._init_alipay()
    
    def _init_alipay(self):
        """初始化支付宝客户端"""
        try:
            try:
                with open(settings.ALIPAY_CONFIG['PRIVATE_KEY_PATH']) as f:
                    key_content = f.read()
                    # 处理私钥格式
                    lines = key_content.strip().split('\n')
                    if len(lines) <= 2:  # 如果只有一行内容
                        app_private_key_string = (
                            "-----BEGIN RSA PRIVATE KEY-----\n" +
                            '\n'.join(textwrap.wrap(lines[0], 64)) +
                            "\n-----END RSA PRIVATE KEY-----"
                        )
                    else:
                        app_private_key_string = key_content
                logger.info("成功读取应用私钥")
            except Exception as e:
                logger.error(f"读取应用私钥失败: {str(e)}")
                raise
            
            # 读取公钥
            try:
                with open(settings.ALIPAY_CONFIG['PUBLIC_KEY_PATH']) as f:
                    key_content = f.read()
                    # 处理公钥格式
                    lines = key_content.strip().split('\n')
                    if len(lines) <= 2:  # 如果只有一行内容
                        alipay_public_key_string = (
                            "-----BEGIN PUBLIC KEY-----\n" +
                            '\n'.join(textwrap.wrap(lines[0], 64)) +
                            "\n-----END PUBLIC KEY-----"
                        )
                    else:
                        alipay_public_key_string = key_content
                logger.info("成功读取支付宝公钥")
            except Exception as e:
                logger.error(f"读取支付宝公钥失败: {str(e)}")
                raise
            
            logger.info("成功读取支付宝密钥文件")
            
            # 打印处理后的密钥格式（仅打印头尾）
            logger.info("私钥格式:")
            logger.info(app_private_key_string.split('\n')[0])
            logger.info('...')
            logger.info(app_private_key_string.split('\n')[-1])
            
            logger.info("公钥格式:")
            logger.info(alipay_public_key_string.split('\n')[0])
            logger.info('...')
            logger.info(alipay_public_key_string.split('\n')[-1])
            
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
            logger.error("完整错误信息:", exc_info=True)
            raise
    
    def create_payment(self, order):
        """创建支付链接"""
        try:
            subject = f'飞鸟简历 - {order.tier.name}'
            body = f'{order.days}天会员服务'
            
            logger.info(f"创建支付订单 - 订单号:{order.order_no}, 金额:{order.amount}")
            
            # 检查支付宝客户端是否正确初始化
            if not self.alipay:
                logger.error("支付宝客户端未初始化")
                raise ValueError("支付宝客户端未初始化")
            
            # 构建支付参数
            params = {
                'out_trade_no': order.order_no,
                'total_amount': float(order.amount),
                'subject': subject,
                'body': body,
                'return_url': settings.ALIPAY_CONFIG['RETURN_URL'],
                'notify_url': settings.ALIPAY_CONFIG['NOTIFY_URL'],
                'timeout_express': '15m',
                'product_code': 'FAST_INSTANT_TRADE_PAY'
            }
            
            logger.info(f"支付参数: {params}")
            
            try:
                order_string = self.alipay.api_alipay_trade_page_pay(**params)
                logger.info("支付宝订单字符串生成成功")
            except Exception as e:
                logger.error(f"生成支付宝订单字符串失败: {str(e)}", exc_info=True)
                raise
            
            # 使用正确的沙箱网关
            gateway = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
            payment_url = f"{gateway}?{order_string}"
            
            logger.info(f"生成支付链接: {payment_url}")
            return payment_url
                
        except Exception as e:
            logger.error(f"创建支付链接失败: {str(e)}")
            logger.error("完整错误信息:", exc_info=True)
            raise

    @classmethod
    def create_order(cls, user, tier_id, duration, payment_method='alipay'):
        """创建订单"""
        try:
            logger.info(f"开始创建订单 - user:{user.id}, tier_id:{tier_id}, duration:{duration}")
            
            # 获取会员等级
            try:
                tier = MembershipTier.objects.get(id=tier_id)
            except MembershipTier.DoesNotExist:
                logger.error(f"会员等级不存在: tier_id={tier_id}")
                raise ValueError('会员等级不存在')

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
                logger.error(f"无效的时长: duration={duration}")
                raise ValueError('Invalid duration')

            logger.info(f"订单金额计算 - amount:{amount}, days:{days}")

            # 创建订单记录
            try:
                order = MembershipOrder.objects.create(
                    user=user,
                    tier=tier,
                    amount=amount,
                    days=days,
                    payment_method=payment_method,
                    status='pending'
                )
                logger.info(f"订单创建成功 - order_no:{order.order_no}")
            except Exception as e:
                logger.error(f"订单记录创建失败: {str(e)}")
                raise

            return {
                'order_no': order.order_no,
                'amount': float(amount)
            }

        except Exception as e:
            logger.error(f"订单创建失败: {str(e)}")
            logger.error(f"完整错误信息:", exc_info=True)
            logger.error(f"请求参数 - user:{user.id}, tier_id:{tier_id}, duration:{duration}")
            raise

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
            cls.logger.info(f"开始处理订单: {order.order_no}")
            
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
            cls.logger.info(f"签名类型: {data.get('sign_type')}")
            
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

    def verify_alipay_params(self, params):
        """验证支付宝回调参数"""
        try:
            # 移除sign和sign_type
            sign = params.pop('sign', None)
            params.pop('sign_type', None)
            
            # 验证签名
            verify_result = self.alipay.verify(params, sign)
            
            # 恢复参数
            params['sign'] = sign
            params['sign_type'] = 'RSA2'
            
            return verify_result
            
        except Exception as e:
            logger.error(f"验证支付宝参数失败: {str(e)}", exc_info=True)
            return False

    def query_payment(self, order_no):
        """查询支付状态"""
        try:
            response = self.alipay.api_alipay_trade_query(out_trade_no=order_no)
            if response.get('code') == '10000':  # 接口调用成功
                return response.get('trade_status')
            return None
        except Exception as e:
            self.logger.error(f"查询支付状态失败: {str(e)}", exc_info=True)
            raise

class PointService:
    """积分服务"""
    
    @staticmethod
    def add_points(user, points, event_type, description=None):
        """
        添加积分
        :param user: 用户对象
        :param points: 积分数量
        :param event_type: 事件类型
        :param description: 描述
        :return: PointRecord 对象
        """
        with transaction.atomic():
            # 获取或创建用户积分账户
            user_point, _ = UserPoint.objects.get_or_create(user=user)
            
            # 更新积分余额
            user_point.balance += points
            user_point.total_earned += points if points > 0 else 0
            user_point.save()
            
            # 创建积分记录
            record = PointRecord.objects.create(
                user=user,
                points=points,
                event_type=event_type,
                description=description,
                balance=user_point.balance
            )
            
            return record
    
    @staticmethod
    def check_daily_sign_in(user):
        """
        检查用户今日是否已签到
        :param user: 用户对象
        :return: bool
        """
        today = timezone.now().date()
        return PointRecord.objects.filter(
            user=user,
            event_type='daily_check_in',
            created_at__date=today
        ).exists()
    
    @staticmethod
    def get_sign_in_days(user):
        """
        获取用户连续签到天数
        :param user: 用户对象
        :return: int
        """
        records = PointRecord.objects.filter(
            user=user,
            event_type='daily_check_in'
        ).order_by('-created_at')
        
        if not records:
            return 0
            
        days = 1
        last_date = records[0].created_at.date()
        
        for record in records[1:]:
            current_date = record.created_at.date()
            if (last_date - current_date).days == 1:
                days += 1
                last_date = current_date
            else:
                break
                
        return days

class MembershipCacheService:
    """会员信息缓存服务"""
    
    @staticmethod
    def get_user_membership_info(user):
        """获取用户会员信息"""
        cache_key = f'user_membership_{user.id}'
        info = cache.get(cache_key)
        
        if info is None:
            membership = getattr(user, 'membership', None)
            info = {
                'is_vip': membership.is_active if membership else False,
                'vip_type': membership.tier.key if membership and membership.is_active and membership.tier else 'none',
                'vip_expire_time': membership.expire_time if membership else None,
                'vip_status': membership.tier.name if membership and membership.is_active and membership.tier else '普通用户'
            }
            cache.set(cache_key, info, timeout=3600)  # 缓存1小时
            
        return info

    @staticmethod
    def clear_user_membership_cache(user):
        """清除用户会员信息缓存"""
        cache_key = f'user_membership_{user.id}'
        cache.delete(cache_key) 