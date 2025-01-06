import os
import django
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from membership.models import MembershipOrder
from django.conf import settings
from alipay import AliPay
import logging
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from base64 import b64encode

logger = logging.getLogger(__name__)

def create_test_signature(data):
    """创建测试签名"""
    # 读取密钥
    with open(settings.PAYMENT_CONFIG['alipay']['private_key_path'], 'r') as f:
        private_key = f.read().strip()
    
    # 按支付宝的规则生成待签名字符串
    ordered_items = []
    for k, v in sorted(data.items()):
        if k not in ['sign', 'sign_type'] and v:  # 排除 sign 和 sign_type，且值不为空
            ordered_items.append(f'{k}={v}')
    unsigned_string = '&'.join(ordered_items)
    
    # 使用 OpenSSL 命令行工具生成签名
    import tempfile
    import subprocess
    from base64 import b64encode
    
    # 创建临时文件存储数据和私钥
    with tempfile.NamedTemporaryFile(mode='w+') as data_file, \
         tempfile.NamedTemporaryFile(mode='w+') as key_file:
        
        # 写入数据
        data_file.write(unsigned_string)
        data_file.flush()
        
        # 写入私钥
        key_file.write(private_key)
        key_file.flush()
        
        # 使用 OpenSSL 生成签名
        cmd = [
            'openssl', 'dgst', '-sha256', '-sign', key_file.name,
            data_file.name
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            # Base64 编码签名
            signature = b64encode(result.stdout).decode('utf-8')
            return signature
        else:
            raise Exception(f"OpenSSL signing failed: {result.stderr.decode()}")

def test_alipay_notify():
    """测试支付宝回调"""
    # 使用新的订单号
    order_no = "M17352338414236"  # 替换为新订单号
    
    try:
        order = MembershipOrder.objects.get(order_no=order_no)
        print(f"\nTesting with order: {order.order_no}")
        print(f"Order amount: {order.amount}")
        print(f"Current status: {order.status}")
        
        # 构造回调数据
        notify_data = {
            'app_id': settings.ALIPAY_APP_ID,
            'auth_app_id': settings.ALIPAY_APP_ID,
            'charset': 'utf-8',
            'version': '1.0',
            'sign_type': 'RSA2',
            'timestamp': '2024-01-01 12:00:00',
            'notify_id': f'2024{order.order_no[1:]}notify',
            'notify_type': 'trade_status_sync',
            'out_trade_no': order.order_no,
            'trade_no': f'2024{order.order_no[1:]}',  # 支付宝交易号
            'trade_status': 'TRADE_SUCCESS',
            'total_amount': str(order.amount),
            'buyer_id': '2088123456789012',  # 买家支付宝账号ID
            'gmt_payment': '2024-01-01 12:00:00',  # 支付时间
            'gmt_create': '2024-01-01 12:00:00',
            'subject': f'Order-{order.order_no}'
        }
        
        # 生成签名
        signature = create_test_signature(notify_data)
        notify_data['sign'] = signature
        
        print("\nSending notify request with data:")
        for key, value in notify_data.items():
            print(f"{key}: {value}")
        
        # 发送回调请求
        response = requests.post(
            'http://127.0.0.1:8000/api/v1/membership/notify/alipay/',
            data=notify_data
        )
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        # 验证订单状态
        order.refresh_from_db()
        print(f"\nOrder status after notification: {order.status}")
        print(f"Order paid time: {order.paid_time}")
        
        # 验证用户会员状态
        user_membership = order.user.membership
        if user_membership:
            print(f"\nUser membership status:")
            print(f"Tier: {user_membership.tier.name}")
            print(f"Expire time: {user_membership.expire_time}")
        else:
            print("\nUser membership not found!")
            
    except MembershipOrder.DoesNotExist:
        print(f"Order not found: {order_no}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == '__main__':
    test_alipay_notify()