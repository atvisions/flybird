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
        membership = self.get_object()
        if not membership:
            return Response({'detail': '未找到会员信息'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(membership)
        return Response(serializer.data)

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
                        return redirect(f"/payment/success?order_no={order_no}&trade_no={trade_no}")
                    else:
                        logger.error("订单处理失败")
                        return redirect(f"/payment/fail?order_no={order_no}&reason=process_failed")
                elif order.status == 'paid':
                    logger.info("订单已经是支付成功状态")
                    return redirect(f"/payment/success?order_no={order_no}&trade_no={trade_no}")
                else:
                    logger.warning(f"订单状态异常: {order.status}")
                    return redirect(f"/payment/fail?order_no={order_no}&reason=invalid_status")
                    
            except MembershipOrder.DoesNotExist:
                logger.error(f"未找到订单: {order_no}")
                return redirect(f"/payment/fail?reason=order_not_found")
        else:
            logger.error("签名验证失败")
            return redirect("/payment/fail?reason=verify_failed")
            
    except Exception as e:
        logger.error(f"处理支付跳转异常: {str(e)}")
        logger.error(traceback.format_exc())
        return redirect("/payment/fail?reason=system_error")
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