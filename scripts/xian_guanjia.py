#!/usr/bin/env python3
"""
闲管家 API 客户端
用于通过 API 操作闲鱼自动发货、商品发布等功能
"""

import hashlib
import time
import json
import requests
from typing import Dict, Any, Optional, List


class XianGuanjiaClient:
    """闲管家 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str, mch_id: str, mch_secret: str, base_url: str = "https://open.goofish.pro"):
        """
        初始化客户端
        
        Args:
            app_id: 管家平台提供的对接应用ID
            app_secret: 管家平台提供的对接密钥
            mch_id: 货源平台提供的对接商户ID
            mch_secret: 货源平台提供的对接密钥
            base_url: API 基础地址，默认为生产环境
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.mch_id = mch_id
        self.mch_secret = mch_secret
        self.base_url = base_url.rstrip('/')
    
    def _generate_sign(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成签名
        
        Args:
            body: 请求体字典
        
        Returns:
            包含 timestamp 和 sign 的字典
        """
        timestamp = int(time.time())
        body_str = json.dumps(body, separators=(',', ':')) if body else "{}"
        
        # 计算 body MD5
        body_md5 = hashlib.md5(body_str.encode('utf-8')).hexdigest()
        
        # 拼接签名字符串
        sign_str = f"{self.app_id},{self.app_secret},{body_md5},{timestamp},{self.mch_id},{self.mch_secret}"
        
        # 计算最终签名
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        return {
            'timestamp': timestamp,
            'sign': sign
        }
    
    def request(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送 API 请求
        
        Args:
            method: HTTP 方法 (GET, POST, etc.)
            path: API 路径
            body: 请求体数据
        
        Returns:
            API 响应 JSON
        """
        if body is None:
            body = {}
        
        url = f"{self.base_url}{path}"
        
        # 生成签名
        sign_info = self._generate_sign(body)
        
        # 将签名和时间戳添加到请求头
        headers = {
            'Content-Type': 'application/json',
            'X-App-Id': str(self.app_id),
            'X-Mch-Id': str(self.mch_id),
            'X-Timestamp': str(sign_info['timestamp']),
            'X-Sign': sign_info['sign']
        }
        
        response = requests.request(method, url, json=body, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    # ==================== 用户接口 ====================
    
    def get_xianyu_shops(self) -> Dict[str, Any]:
        """
        查询闲鱼店铺列表
        
        Returns:
            店铺列表响应
        """
        return self.request('POST', '/api/user/shops', {})
    
    # ==================== 商品接口 ====================
    
    def get_categories(self) -> Dict[str, Any]:
        """
        查询商品类目
        
        Returns:
            类目列表响应
        """
        return self.request('POST', '/api/product/categories', {})
    
    def get_product_attributes(self, category_id: int) -> Dict[str, Any]:
        """
        查询商品属性
        
        Args:
            category_id: 类目ID
        
        Returns:
            属性列表响应
        """
        return self.request('POST', '/api/product/attributes', {
            'category_id': category_id
        })
    
    def get_product_list(self, page: int = 1, page_size: int = 20, status: Optional[int] = None) -> Dict[str, Any]:
        """
        查询商品列表
        
        Args:
            page: 页码
            page_size: 每页数量
            status: 商品状态 (可选) 1-上架 2-下架
        
        Returns:
            商品列表响应
        """
        body = {
            'page': page,
            'page_size': page_size
        }
        if status is not None:
            body['status'] = status
        return self.request('POST', '/api/product/list', body)
    
    def get_product_detail(self, product_id: int) -> Dict[str, Any]:
        """
        查询商品详情
        
        Args:
            product_id: 商品ID
        
        Returns:
            商品详情响应
        """
        return self.request('POST', '/api/product/detail', {
            'product_id': product_id
        })
    
    def get_product_skus(self, product_id: int) -> Dict[str, Any]:
        """
        查询商品规格（仅多规格商品）
        
        Args:
            product_id: 商品ID
        
        Returns:
            规格列表响应
        """
        return self.request('POST', '/api/product/skus', {
            'product_id': product_id
        })
    
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建单个商品
        
        Args:
            data: 商品数据（包含标题、图片、价格等完整信息）
        
        Returns:
            创建响应
        """
        return self.request('POST', '/api/product/create', data)
    
    def create_products_batch(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量创建商品
        
        Args:
            products: 商品数据列表
        
        Returns:
            创建响应
        """
        return self.request('POST', '/api/product/create_batch', {
            'products': products
        })
    
    def publish_product(self, product_id: int) -> Dict[str, Any]:
        """
        上架商品
        
        Args:
            product_id: 商品ID
        
        Returns:
            上架响应
        """
        return self.request('POST', '/api/product/publish', {
            'product_id': product_id
        })
    
    def unpublish_product(self, product_id: int) -> Dict[str, Any]:
        """
        下架商品
        
        Args:
            product_id: 商品ID
        
        Returns:
            下架响应
        """
        return self.request('POST', '/api/product/unpublish', {
            'product_id': product_id
        })
    
    def update_product(self, product_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        编辑商品
        
        Args:
            product_id: 商品ID
            data: 更新的商品数据
        
        Returns:
            更新响应
        """
        body = {'product_id': product_id}
        body.update(data)
        return self.request('POST', '/api/product/update', body)
    
    def update_stock(self, product_id: int, stock: int, sku_id: Optional[int] = None) -> Dict[str, Any]:
        """
        编辑库存
        
        Args:
            product_id: 商品ID
            stock: 库存数量
            sku_id: SKU ID（多规格商品需要）
        
        Returns:
            更新响应
        """
        body = {
            'product_id': product_id,
            'stock': stock
        }
        if sku_id is not None:
            body['sku_id'] = sku_id
        return self.request('POST', '/api/product/update_stock', body)
    
    def delete_product(self, product_id: int) -> Dict[str, Any]:
        """
        删除商品
        
        Args:
            product_id: 商品ID
        
        Returns:
            删除响应
        """
        return self.request('POST', '/api/product/delete', {
            'product_id': product_id
        })
    
    # ==================== 订单接口 ====================
    
    def get_order_list(self, page: int = 1, page_size: int = 20, status: Optional[int] = None) -> Dict[str, Any]:
        """
        获取订单列表
        
        Args:
            page: 页码
            page_size: 每页数量
            status: 订单状态 (可选)
        
        Returns:
            订单列表响应
        """
        body = {
            'page': page,
            'page_size': page_size
        }
        if status is not None:
            body['status'] = status
        return self.request('POST', '/api/order/list', body)
    
    def get_order_detail(self, order_id: int) -> Dict[str, Any]:
        """
        获取订单详情
        
        Args:
            order_id: 订单ID
        
        Returns:
            订单详情响应
        """
        return self.request('POST', '/api/order/detail', {
            'order_id': order_id
        })
    
    def get_order_cards(self, order_id: int) -> Dict[str, Any]:
        """
        获取订单卡密列表（虚拟商品）
        
        Args:
            order_id: 订单ID
        
        Returns:
            卡密列表响应
        """
        return self.request('POST', '/api/order/cards', {
            'order_id': order_id
        })
    
    def ship_order(self, order_id: int, logistics_no: str, logistics_company: str) -> Dict[str, Any]:
        """
        订单物流发货
        
        Args:
            order_id: 订单ID
            logistics_no: 物流单号
            logistics_company: 物流公司代码/名称
        
        Returns:
            发货响应
        """
        return self.request('POST', '/api/order/ship', {
            'order_id': order_id,
            'logistics_no': logistics_no,
            'logistics_company': logistics_company
        })
    
    def update_order_price(self, order_id: int, price: float) -> Dict[str, Any]:
        """
        修改订单价格
        
        Args:
            order_id: 订单ID
            price: 新价格
        
        Returns:
            修改响应
        """
        return self.request('POST', '/api/order/update_price', {
            'order_id': order_id,
            'price': price
        })
    
    def place_order(self, goods_no: str, goods_type: int, buyer_nick: str, 
                   buyer_id: str, order_no: str, price: float) -> Dict[str, Any]:
        """
        下单（对接收货源）
        
        Args:
            goods_no: 商品编号
            goods_type: 商品类型 1-普通 2-虚拟
            buyer_nick: 买家昵称
            buyer_id: 买家ID
            order_no: 管家订单号
            price: 下单价格
        
        Returns:
            下单响应
        """
        return self.request('POST', '/api/order/place', {
            'goods_no': goods_no,
            'goods_type': goods_type,
            'buyer_nick': buyer_nick,
            'buyer_id': buyer_id,
            'order_no': order_no,
            'price': price
        })
    
    # ==================== 其他接口 ====================
    
    def get_logistics_companies(self) -> Dict[str, Any]:
        """
        查询快递公司列表
        
        Returns:
            快递公司列表响应
            如果列表内没有需要的快递公司，可以联系闲管家技术支持补充
        """
        return self.request('POST', '/api/logistics/companies', {})
    
    def query_balance(self) -> Dict[str, Any]:
        """
        查询商户余额
        
        Returns:
            余额信息响应
        """
        return self.request('POST', '/api/mch/balance', {})


def main():
    """
    命令行交互示例
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='闲管家 API 客户端')
    parser.add_argument('--app-id', required=True, help='应用ID')
    parser.add_argument('--app-secret', required=True, help='应用密钥')
    parser.add_argument('--mch-id', required=True, help='商户ID')
    parser.add_argument('--mch-secret', required=True, help='商户密钥')
    parser.add_argument('--base-url', default='https://open.goofish.pro', help='API 地址')
    
    args = parser.parse_args()
    
    client = XianGuanjiaClient(
        app_id=args.app_id,
        app_secret=args.app_secret,
        mch_id=args.mch_id,
        mch_secret=args.mch_secret,
        base_url=args.base_url
    )
    
    # 测试查询余额
    try:
        result = client.query_balance()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
