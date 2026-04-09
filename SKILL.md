---
name: xian-guanjia
description: 闲管家 API 集成，用于闲鱼自动化发货、订单管理、商品发布。支持通过 API 批量处理订单、自动发货。Use when: (1) 需要操作闲管家 API，(2) 帮用户处理闲鱼订单发货，(3) 查询订单列表和余额，(4) 用户提到"闲管家"、"闲鱼自动发货"。
---

# 闲管家

闲管家 API 客户端，用于闲鱼自动化发货、订单管理和商品发布。

## API 文档

完整的 API 签名规则和错误码参见 [references/api-docs.md](references/api-docs.md)

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

### 常用操作

**查询订单列表**
```python
result = client.get_order_list(page=1, page_size=20)
```

**查询订单详情**
```python
result = client.get_order_detail(order_id=12345)
```

**订单发货**
```python
result = client.ship_order(
    order_id=12345,
    logistics_no="物流单号",
    logistics_company="快递公司"
)
```

**下单（货源对接）**
```python
result = client.place_order(
    goods_no="商品编号",
    goods_type=1,  # 1-普通 2-虚拟
    buyer_nick="买家昵称",
    buyer_id="买家ID",
    order_no="管家订单号",
    price=29.90
)
```

**查询余额**
```python
result = client.query_balance()
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
