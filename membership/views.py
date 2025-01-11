from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    MembershipTier, UserMembership, MembershipOrder,
    UserPoint, PointRecord
)
from .serializers import (
    MembershipTierSerializer, UserMembershipSerializer,
    MembershipOrderSerializer, UserPointSerializer,
    PointRecordSerializer
)
from .services import PaymentService, MembershipCacheService, PointService
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .tasks import process_payment_callback
from django.conf import settings
import logging
import traceback
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

# 配置日志记录器
logger = logging.getLogger('membership')

class MembershipTierViewSet(viewsets.ReadOnlyModelViewSet):
    """会员等级视图集"""
    queryset = MembershipTier.objects.filter(status=True)  # 只显示启用的等级
    serializer_class = MembershipTierSerializer
    permission_classes = [permissions.AllowAny]  # 允许任何人访问
    
    def list(self, request):
        """获取会员等级列表"""
        queryset = self.get_queryset().order_by('sort_order')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

class UserMembershipViewSet(viewsets.GenericViewSet):
    """用户会员视图集"""
    serializer_class = UserMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserMembership.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()

    @action(detail=False, methods=['get'])
    def info(self, request):
        """获取会员信息"""
        membership = getattr(request.user, 'membership', None)
        if not membership:
            return Response({
                'code': 404,
                'message': '未找到会员信息',
                'data': None
            })
            
        # 检查是否需要恢复会员状态
        if membership.expire_time < timezone.now():
            restored = membership.check_and_restore()
            if restored:
                membership.refresh_from_db()
        
        serializer = self.get_serializer(membership)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        """购买会员"""
        try:
            # 记录当前配置
            logger.info("创建订单使用的配置:")
            logger.info(f"NGROK_URL: {settings.NGROK_URL}")
            logger.info(f"notify_url: {settings.PAYMENT_CONFIG['alipay']['notify_url']}")
            logger.info(f"return_url: {settings.PAYMENT_CONFIG['alipay']['return_url']}")
            
            # 获取参数
            tier_id = request.data.get('tier_id')
            duration = request.data.get('duration')  # monthly, quarterly, yearly
            payment_method = request.data.get('payment_method', 'alipay')
            
            # 参数验证
            if not tier_id or not duration:
                return Response({
                    'detail': '缺少必要参数'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取会员等级
            try:
                tier = MembershipTier.objects.get(id=tier_id)
            except MembershipTier.DoesNotExist:
                return Response({
                    'detail': '无效的会员等级'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 创建订单
            try:
                result = PaymentService.create_order(
                    user=request.user,
                    tier=tier,
                    duration=duration,
                    payment_method=payment_method
                )
                return Response(result)
            except ValueError as e:
                return Response({
                    'detail': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"购买会员失败: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                'detail': '购买失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PointViewSet(viewsets.GenericViewSet):
    """积分视图集"""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def balance(self, request):
        """获取积分余额"""
        point, _ = UserPoint.objects.get_or_create(user=request.user)
        serializer = UserPointSerializer(point)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def records(self, request):
        """获取积分记录"""
        records = PointRecord.objects.filter(user=request.user)
        page = self.paginate_queryset(records)
        serializer = PointRecordSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

@csrf_exempt
def alipay_notify(request):
    """支付宝异步通知"""
    logger.info("\n" + "="*50)
    logger.info("支付宝异步通知开始处理")
    
    try:
        # 记录请求信息
        logger.info(f"请求方法: {request.method}")
        logger.info(f"请求头: \n{dict(request.headers)}")
        logger.info(f"请求IP: {request.META.get('REMOTE_ADDR')}")
        
        if request.method == 'POST':
            data = request.POST.dict()
            logger.info(f"收到的数据: \n{data}")
            
            # 验证签名
            verified_data = PaymentService.verify_alipay_payment(data)
            if verified_data:
                order_no = verified_data.get('out_trade_no')
                trade_status = verified_data.get('trade_status')
                
                logger.info(f"签名验证: 成功")
                logger.info(f"订单号: {order_no}")
                logger.info(f"交易状态: {trade_status}")
                
                if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
                    try:
                        order = MembershipOrder.objects.get(order_no=order_no)
                        logger.info(f"订单状态: {order.status}")
                        
                        if PaymentService.complete_order(order):
                            logger.info("订单处理成功")
                            logger.info("="*50 + "\n")
                            return HttpResponse('success')
                        else:
                            logger.error("订单处理失败")
                    except MembershipOrder.DoesNotExist:
                        logger.error(f"未找到订单: {order_no}")
                else:
                    logger.warning(f"无效的交易状态: {trade_status}")
            else:
                logger.error("签名验证失败")
        else:
            logger.warning(f"不支持的请求方法: {request.method}")
            
    except Exception as e:
        logger.error(f"处理异常: {str(e)}")
        logger.error(f"异常详情: \n{traceback.format_exc()}")
    
    logger.info("处理完成，返回 fail")
    logger.info("="*50 + "\n")
    return HttpResponse('fail')

def alipay_return(request):
    """支付宝同步通知（支付完成后的跳转页面）"""
    try:
        # 获取参数
        data = request.GET.dict()
        logger.info("\n" + "="*50)
        logger.info("支付宝同步跳转开始处理")
        logger.info(f"收到的数据: \n{data}")
        
        # 验证签名
        verified_data = PaymentService.verify_alipay_payment(data)
        if verified_data:
            order_no = verified_data.get('out_trade_no')
            trade_status = verified_data.get('trade_status')
            trade_no = verified_data.get('trade_no')
            total_amount = verified_data.get('total_amount')
            
            logger.info(f"签名验证: 成功")
            logger.info(f"订单号: {order_no}")
            logger.info(f"支付宝交易号: {trade_no}")
            logger.info(f"交易状态: {trade_status}")
            
            try:
                # 查询订单状态
                order = MembershipOrder.objects.get(order_no=order_no)
                logger.info(f"订单当前状态: {order.status}")
                
                if order.status == 'pending':
                    # 尝试完成订单
                    if PaymentService.complete_order(order):
                        logger.info("订单处理成功")
                        return redirect(
                            f"{settings.ALIPAY_CONFIG['RETURN_URL']}"
                            f"?out_trade_no={order_no}"
                            f"&trade_no={trade_no}"
                            f"&total_amount={total_amount}"
                        )
                    else:
                        logger.error("订单处理失败")
                        return redirect(f"{settings.ALIPAY_CONFIG['FAIL_URL']}?reason=process_failed")
                elif order.status == 'paid':
                    logger.info("订单已经是支付成功状态")
                    return redirect(
                        f"{settings.ALIPAY_CONFIG['RETURN_URL']}"
                        f"?out_trade_no={order_no}"
                        f"&trade_no={trade_no}"
                        f"&total_amount={total_amount}"
                    )
                else:
                    logger.warning(f"订单状态异常: {order.status}")
                    return redirect(f"{settings.ALIPAY_CONFIG['FAIL_URL']}?reason=invalid_status")
                    
            except MembershipOrder.DoesNotExist:
                logger.error(f"未找到订单: {order_no}")
                return redirect(f"{settings.ALIPAY_CONFIG['FAIL_URL']}?reason=order_not_found")
        else:
            logger.error("签名验证失败")
            return redirect(f"{settings.ALIPAY_CONFIG['FAIL_URL']}?reason=verify_failed")
            
    except Exception as e:
        logger.error(f"处理支付跳转异常: {str(e)}")
        logger.error(traceback.format_exc())
        return redirect(f"{settings.ALIPAY_CONFIG['FAIL_URL']}?reason=system_error")
    finally:
        logger.info("="*50 + "\n")

@csrf_exempt
def wechat_notify(request):
    """微信支付回调"""
    if request.method == 'POST':
        try:
            data = PaymentService.verify_wechat_payment(request.body)
            if data and data['return_code'] == 'SUCCESS':
                order_no = data['out_trade_no']
                try:
                    order = MembershipOrder.objects.get(order_no=order_no, status='pending')
                    # 异步处理支付结果
                    process_payment_callback.delay(order.id, data)
                    return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>')
                except MembershipOrder.DoesNotExist:
                    pass
        except Exception:
            pass
    return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code></xml>') 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    """每日签到"""
    try:
        # 检查今日是否已签到
        if PointService.check_daily_sign_in(request.user):
            return Response({
                'code': 400,
                'message': '今日已签到',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取连续签到天数
        sign_in_days = PointService.get_sign_in_days(request.user)
        
        # 计算签到奖励积分
        points = 3  # 基础积分
        
        # 连续签到额外奖励
        if sign_in_days % 7 == 6:  # 连续签到7天
            points += 10
        if sign_in_days % 30 == 29:  # 连续签到30天
            points += 50
            
        # 添加积分
        record = PointService.add_points(
            user=request.user,
            points=points,
            event_type='daily_check_in',
            description=f'第{sign_in_days + 1}天签到奖励'
        )
        
        return Response({
            'code': 200,
            'message': '签到成功',
            'data': {
                'points': points,
                'balance': record.balance,
                'sign_in_days': sign_in_days + 1,
                'next_reward': {
                    'days': 7 - ((sign_in_days + 1) % 7),
                    'points': 10
                } if (sign_in_days + 1) % 7 != 0 else {
                    'days': 30 - ((sign_in_days + 1) % 30),
                    'points': 50
                }
            }
        })
        
    except Exception as e:
        logger.error(f"签到失败: {str(e)}")
        return Response({
            'code': 500,
            'message': '签到失败，请稍后重试',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class MembershipPurchaseView(APIView):
    """会员购买"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # 获取参数
            tier_id = request.data.get('tier_id')
            duration = request.data.get('duration', 'monthly')
            payment_method = request.data.get('payment_method', 'alipay')
            
            logger.info(f"用户 {request.user.phone} 尝试购买会员")
            logger.info(f"参数: tier_id={tier_id}, duration={duration}, payment_method={payment_method}")
            
            # 检查当前会员状态
            current_membership = getattr(request.user, 'membership', None)
            if current_membership and current_membership.expire_time > timezone.now():
                logger.info(f"用户当前会员状态: 等级={current_membership.tier.name}, 到期时间={current_membership.expire_time}")
            else:
                logger.info("用户当前不是会员或会员已过期")
            
            # 验证会员等级
            try:
                tier = MembershipTier.objects.get(id=tier_id)
                logger.info(f"目标会员等级: {tier.name}")
                
                # 检查是否降级
                if current_membership and current_membership.tier.sort_order > tier.sort_order:
                    return Response({
                        'code': 400,
                        'message': '不能购买低于当前等级的会员',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except MembershipTier.DoesNotExist:
                logger.error(f"会员等级不存在: {tier_id}")
                return Response({
                    'code': 404,
                    'message': '会员等级不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 验证购买时长
            if duration not in ['monthly', 'quarterly', 'yearly']:
                logger.error(f"无效的购买时长: {duration}")
                return Response({
                    'code': 400,
                    'message': '无效的购买时长',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取价格和天数
            price_field = f'price_{duration}'
            amount = getattr(tier, price_field)
            days = {
                'monthly': 30,
                'quarterly': 90,
                'yearly': 365
            }[duration]
            
            logger.info(f"计算价格: {amount}, 天数: {days}")
            
            # 创建订单
            try:
                order = MembershipOrder.objects.create(
                    user=request.user,
                    tier=tier,
                    amount=amount,
                    days=days,
                    payment_method=payment_method,
                    status='pending'
                )
                logger.info(f"创建订单成功: {order.id}")
                
                # 调用支付服务
                payment_service = PaymentService()
                payment_url = payment_service.create_payment(order)
                logger.info(f"生成支付链接成功: {payment_url}")
                
                return Response({
                    'code': 200,
                    'message': '创建订单成功',
                    'data': {
                        'order_id': order.id,
                        'payment_url': payment_url,
                        'amount': float(amount),
                        'days': days
                    }
                })
                
            except Exception as e:
                logger.error(f"创建订单失败: {str(e)}")
                return Response({
                    'code': 500,
                    'message': '创建订单失败',
                    'data': None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            logger.error(f"购买会员失败: {str(e)}")
            logger.error(f"错误详情: {e.__class__.__name__}")
            logger.error(f"请求数据: {request.data}")
            return Response({
                'code': 500,
                'message': '系统错误，请稍后重试',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])  # 允许未认证访问
def payment_success(request):
    """支付成功页面"""
    try:
        # 获取所有参数
        data = request.GET.dict()
        logger.info(f"支付成功页面收到参数: {data}")
        
        # 获取关键参数
        order_no = data.get('out_trade_no')
        trade_no = data.get('trade_no')
        total_amount = data.get('total_amount')
        auth_app_id = data.get('auth_app_id')
        seller_id = data.get('seller_id')
        timestamp = data.get('timestamp')
        
        logger.info(f"支付成功回调: order_no={order_no}, trade_no={trade_no}")
        
        try:
            # 查询订单信息
            order = MembershipOrder.objects.get(order_no=order_no)
            
            # 验证订单金额
            if float(total_amount) != float(order.amount):
                logger.error(f"订单金额不匹配: 支付金额={total_amount}, 订单金额={order.amount}")
                return JsonResponse({
                    'code': 400,
                    'message': '订单金额不匹配',
                    'data': None
                }, status=400)
            
            # 验证商家信息
            if auth_app_id != settings.ALIPAY_CONFIG['APP_ID']:
                logger.error(f"商家ID不匹配: {auth_app_id}")
                return JsonResponse({
                    'code': 400,
                    'message': '商家信息不匹配',
                    'data': None
                }, status=400)
            
            # 更新订单状态和会员信息
            if order.status == 'pending':
                try:
                    with transaction.atomic():
                        # 更新订单状态
                        order.status = 'paid'
                        order.paid_time = timezone.now()
                        order.save()
                        logger.info(f"更新订单状态为已支付: {order.order_no}")
                        
                        # 更新会员信息
                        membership, created = UserMembership.objects.get_or_create(
                            user=order.user,
                            defaults={'tier': order.tier}
                        )
                        
                        # 更新会员等级和到期时间
                        membership.tier = order.tier
                        if membership.expire_time and membership.expire_time > timezone.now():
                            # 如果会员未过期，在当前到期时间基础上延长
                            membership.expire_time += timezone.timedelta(days=order.days)
                        else:
                            # 如果会员已过期，从当前时间开始计算
                            membership.expire_time = timezone.now() + timezone.timedelta(days=order.days)
                        
                        membership.save()
                        logger.info(f"更新会员信息成功: 用户={order.user.phone}, 等级={membership.tier.name}, 到期时间={membership.expire_time}")
                        
                except Exception as e:
                    logger.error(f"更新订单和会员信息失败: {str(e)}")
                    return JsonResponse({
                        'code': 500,
                        'message': '订单处理失败',
                        'data': None
                    }, status=500)
            
            return JsonResponse({
                'code': 200,
                'message': '支付成功',
                'data': {
                    'order_no': order_no,
                    'trade_no': trade_no,
                    'amount': total_amount,
                    'tier_name': order.tier.name,
                    'days': order.days,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'paid_at': timestamp,
                    'status': order.status,
                    'payment_method': order.payment_method,
                    'seller_id': seller_id,
                    'expire_time': order.user.membership.expire_time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(order.user, 'membership') else None
                }
            })
            
        except MembershipOrder.DoesNotExist:
            logger.error(f"未找到订单: {order_no}")
            return JsonResponse({
                'code': 404,
                'message': '订单不存在',
                'data': None
            }, status=404)
            
    except Exception as e:
        logger.error(f"处理支付成功页面异常: {str(e)}")
        logger.error(f"请求参数: {request.GET}")
        return JsonResponse({
            'code': 500,
            'message': '系统错误',
            'data': None
        }, status=500)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])  # 允许未认证访问
def payment_fail(request):
    """支付失败页面"""
    try:
        reason = request.GET.get('reason', 'unknown')
        order_no = request.GET.get('order_no')
        
        logger.info(f"支付失败回调: order_no={order_no}, reason={reason}")
        
        error_messages = {
            'process_failed': '订单处理失败',
            'invalid_status': '订单状态异常',
            'order_not_found': '订单不存在',
            'verify_failed': '签名验证失败',
            'system_error': '系统错误',
            'unknown': '未知错误'
        }
        
        return JsonResponse({
            'code': 500,
            'message': error_messages.get(reason, '支付失败'),
            'data': {
                'reason': reason,
                'order_no': order_no
            }
        })
        
    except Exception as e:
        logger.error(f"处理支付失败页面异常: {str(e)}")
        logger.error(f"请求参数: {request.GET}")
        return JsonResponse({
            'code': 500,
            'message': '系统错误',
            'data': None
        }, status=500) 

class MembershipOrderViewSet(viewsets.GenericViewSet):
    """会员订单视图集"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembershipOrderSerializer
    
    def get_queryset(self):
        return MembershipOrder.objects.filter(user=self.request.user)
    
    def list(self, request):
        """获取订单列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
    
    def create(self, request):
        """创建订单"""
        try:
            logger.info(f"接收到订单创建请求: {request.data}")
            
            tier_id = request.data.get('tier_id')
            duration = request.data.get('duration')
            payment_method = request.data.get('payment_method')
            
            # 参数验证
            if not all([tier_id, duration, payment_method]):
                logger.warning(f"缺少必要参数: tier_id={tier_id}, duration={duration}, payment_method={payment_method}")
                return Response({
                    'code': 400,
                    'message': '缺少必要参数'
                }, status=400)
            
            logger.info(f"开始创建订单 - tier_id:{tier_id}, duration:{duration}, payment_method:{payment_method}")
            logger.info(f"当前用户: {request.user.id}")

            # 创建订单
            try:
                order_data = PaymentService.create_order(
                    user=request.user,
                    tier_id=tier_id,
                    duration=duration,
                    payment_method=payment_method
                )
                
                logger.info(f"订单创建成功: {order_data}")
                
                return Response({
                    'code': 200,
                    'message': '创建订单成功',
                    'data': order_data
                })
                
            except ValueError as e:
                logger.warning(f"订单创建失败(参数错误): {str(e)}")
                return Response({
                    'code': 400,
                    'message': str(e)
                }, status=400)
                
        except Exception as e:
            logger.error(f"订单创建失败(系统错误): {str(e)}")
            logger.error("完整错误信息:", exc_info=True)
            return Response({
                'code': 500,
                'message': '系统错误，请稍后重试'
            }, status=500)

class PaymentCreateView(APIView):
    """创建支付"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            order_no = request.data.get('order_no')
            payment_method = request.data.get('payment_method')
            
            logger.info(f"开始创建支付 - order_no: {order_no}, method: {payment_method}")
            
            # 获取订单
            try:
                order = MembershipOrder.objects.get(
                    order_no=order_no,
                    user=request.user,
                    status='pending'
                )
            except MembershipOrder.DoesNotExist:
                logger.error(f"订单不存在或状态异常: {order_no}")
                return Response({
                    'code': 404,
                    'message': '订单不存在或状态异常'
                }, status=404)
            
            # 创建支付
            try:
                payment_service = PaymentService()
                payment_url = payment_service.create_payment(order)
                
                logger.info(f"支付链接创建成功 - URL: {payment_url}")
                
                return Response({
                    'code': 200,
                    'message': '创建支付成功',
                    'data': {
                        'payment_url': payment_url,
                        'order_no': order.order_no,
                        'amount': float(order.amount)
                    }
                })
            except Exception as e:
                logger.error(f"创建支付链接失败: {str(e)}", exc_info=True)
                return Response({
                    'code': 500,
                    'message': '创建支付链接失败'
                }, status=500)
            
        except Exception as e:
            logger.error(f"创建支付失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '系统错误，请稍后重试'
            }, status=500)

class PaymentNotifyView(APIView):
    """支付通知处理"""
    permission_classes = [AllowAny]

    def post(self, request):
        return alipay_notify(request)

class PaymentReturnView(APIView):
    """支付返回处理"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            logger.info(f"收到支付同步回调: {request.GET}")
            
            # 获取参数
            out_trade_no = request.GET.get('out_trade_no')
            trade_no = request.GET.get('trade_no')
            total_amount = request.GET.get('total_amount')
            
            logger.info(f"订单号: {out_trade_no}")
            logger.info(f"支付宝交易号: {trade_no}")
            logger.info(f"支付金额: {total_amount}")
            
            # 验证签名
            payment_service = PaymentService()
            verify_result = payment_service.verify_alipay_params(request.GET)
            
            if verify_result:
                # 更新订单状态
                try:
                    order = MembershipOrder.objects.get(order_no=out_trade_no)
                    PaymentService.complete_order(order)
                    logger.info(f"订单 {out_trade_no} 处理成功")
                    
                    # 重定向到前端成功页面
                    return redirect(f"{settings.FRONTEND_URL}/payment/success")
                except MembershipOrder.DoesNotExist:
                    logger.error(f"订单不存在: {out_trade_no}")
                    return redirect(f"{settings.FRONTEND_URL}/payment/fail?reason=order_not_found")
            else:
                logger.error("支付宝签名验证失败")
                return redirect(f"{settings.FRONTEND_URL}/payment/fail?reason=verify_failed")
                
        except Exception as e:
            logger.error(f"处理支付回调异常: {str(e)}", exc_info=True)
            return redirect(f"{settings.FRONTEND_URL}/payment/fail?reason=system_error")

class AlipayNotifyView(APIView):
    """支付宝异步通知"""
    permission_classes = [AllowAny]

    def post(self, request):
        return alipay_notify(request)

class AlipayReturnView(APIView):
    """支付宝同步返回"""
    permission_classes = [AllowAny]

    def get(self, request):
        return alipay_return(request)

class UserPointViewSet(viewsets.GenericViewSet):
    """用户积分视图集"""
    serializer_class = UserPointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPoint.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def balance(self, request):
        """获取积分余额"""
        try:
            point, _ = UserPoint.objects.get_or_create(
                user=request.user,
                defaults={
                    'balance': 0,
                    'total_earned': 0,
                    'point_level': 1,
                    'sign_in_days': 0
                }
            )
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'balance': point.balance,
                    'total_earned': point.total_earned,
                    'level': point.point_level,
                    'sign_in_days': point.sign_in_days
                }
            })
            
        except Exception as e:
            logger.error(f"获取积分信息失败: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                'code': 500,
                'message': '获取积分信息失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PointRecordListView(APIView):
    """积分记录列表"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            
            # 获取用户的积分记录
            records = PointRecord.objects.filter(user=request.user).order_by('-created_at')
            
            # 分页
            start = (page - 1) * page_size
            end = start + page_size
            
            # 获取当前页的记录
            current_records = records[start:end]
            
            # 序列化数据
            serializer = PointRecordSerializer(current_records, many=True)
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'records': serializer.data,
                    'has_more': records.count() > end,
                    'total': records.count()
                }
            })
            
        except Exception as e:
            logger.error(f"获取积分记录失败: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                'code': 500,
                'message': '获取积分记录失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentVerifyView(APIView):
    """支付验证"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            order_no = request.data.get('order_no')
            if not order_no:
                return Response({
                    'code': 400,
                    'message': '缺少订单号'
                }, status=400)

            # 获取订单
            try:
                order = MembershipOrder.objects.get(
                    order_no=order_no,
                    user=request.user
                )
            except MembershipOrder.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '订单不存在'
                }, status=404)

            # 如果订单已支付
            if order.status == 'paid':
                return Response({
                    'code': 200,
                    'message': '支付成功',
                    'data': {
                        'order_no': order.order_no,
                        'status': order.status
                    }
                })

            # 如果订单未支付，调用支付宝查询接口
            payment_service = PaymentService()
            try:
                response = payment_service.alipay.api_alipay_trade_query(out_trade_no=order_no)
                logger.info(f"支付宝查询结果: {response}")
                
                if response.get('code') == '10000':  # 接口调用成功
                    trade_status = response.get('trade_status')
                    if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
                        try:
                            with transaction.atomic():
                                # 更新订单状态
                                order.status = 'paid'
                                order.paid_time = timezone.now()
                                order.save()
                                
                                # 更新会员信息
                                membership, created = UserMembership.objects.get_or_create(
                                    user=order.user,
                                    defaults={'tier': order.tier}
                                )
                                membership.tier = order.tier
                                if not membership.expire_time or membership.expire_time < timezone.now():
                                    membership.expire_time = timezone.now() + timezone.timedelta(days=order.days)
                                else:
                                    membership.expire_time = membership.expire_time + timezone.timedelta(days=order.days)
                                membership.save()
                                
                                # 清除会员信息缓存
                                MembershipCacheService.clear_user_membership_cache(order.user)
                            
                            logger.info(f"订单 {order_no} 处理成功")
                            logger.info(f"会员信息更新成功 - 用户:{order.user.phone}, 等级:{order.tier.name}, 到期时间:{membership.expire_time}")
                            
                            return Response({
                                'code': 200,
                                'message': '支付成功',
                                'data': {
                                    'order_no': order.order_no,
                                    'status': 'paid'
                                }
                            })
                        except Exception as e:
                            logger.error(f"更新订单状态失败: {str(e)}", exc_info=True)
                            return Response({
                                'code': 500,
                                'message': '订单处理失败'
                            }, status=500)
                
                return Response({
                    'code': 400,
                    'message': '支付未完成',
                    'data': {
                        'order_no': order.order_no,
                        'status': order.status,
                        'trade_status': response.get('trade_status')
                    }
                })
                
            except Exception as e:
                logger.error(f"查询支付状态失败: {str(e)}", exc_info=True)
                return Response({
                    'code': 500,
                    'message': '查询支付状态失败'
                }, status=500)

        except Exception as e:
            logger.error(f"验证支付失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '系统错误'
            }, status=500) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_in_status(request):
    """获取签到状态"""
    try:
        # 获取用户积分账户
        user_point, _ = UserPoint.objects.get_or_create(user=request.user)
        
        # 检查今日是否已签到
        can_sign_in = not PointService.check_daily_sign_in(request.user)
        
        # 获取连续签到天数
        sign_in_days = PointService.get_sign_in_days(request.user)
        
        # 计算下次奖励
        next_reward = None
        if can_sign_in:
            if (sign_in_days + 1) % 7 == 0:  # 即将获得7天奖励
                next_reward = {
                    'days': 1,
                    'points': 10
                }
            elif (sign_in_days + 1) % 30 == 0:  # 即将获得30天奖励
                next_reward = {
                    'days': 1,
                    'points': 50
                }
            else:
                days_to_weekly = 7 - ((sign_in_days + 1) % 7)
                next_reward = {
                    'days': days_to_weekly,
                    'points': 10
                }
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'can_sign_in': can_sign_in,
                'sign_in_days': sign_in_days,
                'next_reward': next_reward,
                'balance': user_point.balance,
                'total_earned': user_point.total_earned
            }
        })
        
    except Exception as e:
        logger.error(f"获取签到状态失败: {str(e)}")
        logger.error(traceback.format_exc())
        return Response({
            'code': 500,
            'message': '获取签到状态失败',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 