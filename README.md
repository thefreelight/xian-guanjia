# xian-guanjia

闲管家 API Python 客户端 - 闲鱼自动化发货、商品管理工具

[![GitHub](https://img.shields.io/github/stars/thefreelight/xian-guanjia?style=social)](https://github.com/thefreelight/xian-guanjia)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

这是一个闲管家开放平台的 Python API 客户端，支持完整的闲鱼自动化操作：

- 🔐 **自动签名** - 按照闲管家规则自动生成 MD5 签名
- 📦 **商品管理** - 创建、编辑、上架、下架、删除商品，批量创建
- 📦 **订单管理** - 查询订单、发货、改价、获取卡密
- 🔍 **查询功能** - 类目查询、属性查询、快递公司查询、余额查询
- 🪝 **Webhook 支持** - 支持商品和订单推送回调

## 安装

```bash
git clone https://github.com/thefreelight/xian-guanjia.git
cd xian-guanjia
pip install requests
```

## 功能列表

| 模块 | 方法 | 功能 |
|------|------|------|
| 用户 | `get_xianyu_shops()` | 查询闲鱼店铺列表 |
| 商品 | `get_categories()` | 查询商品类目 |
| 商品 | `get_product_attributes(category_id)` | 查询商品属性 |
| 商品 | `get_product_list(page, page_size, status)` | 查询商品列表 |
| 商品 | `get_product_detail(product_id)` | 查询商品详情 |
| 商品 | `get_product_skus(product_id)` | 查询商品规格（多规格） |
| 商品 | `create_product(data)` | 创建单个商品 |
| 商品 | `create_products_batch(products)` | 批量创建商品 |
| 商品 | `publish_product(product_id)` | 上架商品 |
| 商品 | `unpublish_product(product_id)` | 下架商品 |
| 商品 | `update_product(product_id, data)` | 编辑商品 |
| 商品 | `update_stock(product_id, stock, sku_id)` | 编辑库存 |
| 商品 | `delete_product(product_id)` | 删除商品 |
| 订单 | `get_order_list(page, page_size, status)` | 获取订单列表 |
| 订单 | `get_order_detail(order_id)` | 获取订单详情 |
| 订单 | `get_order_cards(order_id)` | 获取卡密列表（虚拟商品） |
| 订单 | `ship_order(order_id, logistics_no, logistics_company)` | 订单发货 |
| 订单 | `update_order_price(order_id, price)` | 修改订单价格 |
| 订单 | `place_order(...)` | 下单（货源对接） |
| 其他 | `get_logistics_companies()` | 查询快递公司列表 |
| 其他 | `query_balance()` | 查询商户余额 |

## 使用方法

```python
from xian_guanjia import XianGuanjiaClient

client = XianGuanjiaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    mch_id="your_mch_id",
    mch_secret="your_mch_secret"
)

# 查询订单列表
result = client.get_order_list(page=1, page_size=20, status=1)  # status=1 待发货
print(result)

# 订单发货
result = client.ship_order(
    order_id=12345,
    logistics_no="7894561230",
    logistics_company="顺丰速运"
)

# 创建商品
product_data = {
    "title": "商品标题",
    "price": 29.90,
    "category_id": 123,
    # 更多字段请参考官方 API 文档
}
result = client.create_product(product_data)

# 上架商品
if result['code'] == 0:
    product_id = result['data']['product_id']
    client.publish_product(product_id)

# 查询余额
result = client.query_balance()
print(result)
```

## 命令行使用

```bash
python scripts/xian_guanjia.py \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --mch-id YOUR_MCH_ID \
  --mch-secret YOUR_MCH_SECRET
```

## 签名算法

闲管家使用 MD5 签名认证，本客户端已经自动处理签名，无需手动计算。

**签名流程：**

1. 将请求体 JSON 序列化得到 `body_str`
2. 计算 `body_md5 = md5(body_str)`
3. 拼接签名字符串：`app_id,app_secret,body_md5,timestamp,mch_id,mch_secret`
4. 计算最终签名：`sign = md5(sign_str)`

详细的签名规则参见 [references/api-docs.md](references/api-docs.md)

## 错误码

| 错误码 | 错误描述 |
| --- | --- |
| 0 | 请求成功 |
| 1 | 请求错误（不在定义范围内的错误） |
| 401 | 签名错误 |
| 403 | IP不在白名单 |
| 408 | 时间戳过期 |
| 500 | 系统异常，请重试 |
| 1000 | 商户不存在 |
| 1001 | 商户不可用 |
| 1002 | 商户余额不足 |
| 1100 | 商品不存在 |
| 1101 | 商品不可用 |
| 1102 | 商品库存不足 |
| 1200 | 订单不存在 |

完整错误码参见 [references/api-docs.md](references/api-docs.md)

## 官方文档

- 闲管家开放平台：https://open.goofish.pro
- 完整 API 文档：https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/llms.txt

## 许可证

MIT License - see [LICENSE](LICENSE) for details

## 相关链接

- 闲管家官网：https://goofish.pro
