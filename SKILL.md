---
name: xian-guanjia
description: 闲管家 API 集成，用于闲鱼自动化发货、订单管理、商品发布。支持通过 API 批量处理订单、自动发货、商品创建上下架。Use when: (1) 需要操作闲管家 API，(2) 帮用户处理闲鱼订单发货，(3) 查询订单列表和余额，(4) 商品创建上架下架，(5) 用户提到"闲管家"、"闲鱼自动发货"、"闲鱼自动化"。
---

# 闲管家

闲管家 API 客户端，用于闲鱼自动化发货、订单管理和商品发布。支持完整的商品管理、订单处理流程。

## API 文档

完整的 API 签名规则和错误码参见 [references/api-docs.md](references/api-docs.md)

## 功能列表

### 用户接口
- `get_xianyu_shops()` - 查询闲鱼店铺列表

### 商品接口
- `get_categories()` - 查询商品类目
- `get_product_attributes(category_id)` - 查询商品属性
- `get_product_list(page, page_size, status)` - 查询商品列表
- `get_product_detail(product_id)` - 查询商品详情
- `get_product_skus(product_id)` - 查询商品规格（仅多规格）
- `create_product(data)` - 创建单个商品
- `create_products_batch(products)` - 批量创建商品
- `publish_product(product_id)` - 上架商品
- `unpublish_product(product_id)` - 下架商品
- `update_product(product_id, data)` - 编辑商品
- `update_stock(product_id, stock, sku_id)` - 编辑库存
- `delete_product(product_id)` - 删除商品

### 订单接口
- `get_order_list(page, page_size, status)` - 获取订单列表
- `get_order_detail(order_id)` - 获取订单详情
- `get_order_cards(order_id)` - 获取订单卡密列表（虚拟商品）
- `ship_order(order_id, logistics_no, logistics_company)` - 订单发货
- `update_order_price(order_id, price)` - 修改订单价格
- `place_order(...)` - 下单（货源对接）

### 其他接口
- `get_logistics_companies()` - 查询快递公司列表
- `query_balance()` - 查询商户余额

## 使用方法

### 初始化客户端

```python
from scripts.xian_guanjia import XianGuanjiaClient

client = XianGuanjiaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    mch_id="your_mch_id",
    mch_secret="your_mch_secret"
)
```

### 示例：查询待发货订单

```python
# 获取订单列表（不指定status则返回全部）
result = client.get_order_list(page=1, page_size=20, status=1)
print(result)
```

### 示例：订单发货

```python
result = client.ship_order(
    order_id=12345,
    logistics_no="7894561230",
    logistics_company="顺丰速运"
)
```

### 示例：创建并上架商品

```python
# 创建商品
product_data = {
    "title": "商品标题",
    "price": 29.90,
    "category_id": 123,
    # ... 其他必填字段见API文档
}
result = client.create_product(product_data)

if result['code'] == 0:
    product_id = result['data']['product_id']
    # 上架商品
    client.publish_product(product_id)
```

### 示例：查询余额

```python
result = client.query_balance()
print(result)
```

## 响应格式

所有请求返回格式：
```json
{
  "code": 0,
  "msg": "OK",
  "data": { ... }
}
```

- `code = 0` 表示成功
- 其他值表示失败，错误信息在 `msg`

## 错误码

详见 [references/api-docs.md](references/api-docs.md) 中的全局错误码说明。

## 命令行使用

```bash
python scripts/xian_guanjia.py \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --mch-id YOUR_MCH_ID \
  --mch-secret YOUR_MCH_SECRET
```

## 依赖

需要安装 requests：
```bash
pip install requests
```
