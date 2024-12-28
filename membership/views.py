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
from .services import PaymentService
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
    queryset = MembershipTier.objects.all()
    serializer_class = MembershipTierSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    # 检查今日是否已签到
    today = timezone.now().date()
    checked = PointRecord.objects.filter(
        user=request.user,
        event_type='daily_check_in',
        created_at__date=today
    ).exists()
    
    if checked:
        return Response({'detail': '今日已签到'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        record = PointService.add_points(
            user=request.user,
            event_type='daily_check_in',
            description='每日签到奖励'
        )
        return Response({
            'points': record.points,
            'balance': record.balance,
            'message': '签到成功'
        })
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

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
    """支付失败��面"""
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