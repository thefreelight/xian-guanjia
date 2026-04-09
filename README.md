# xian-guanjia

闲管家 API Python 客户端 - 闲鱼自动化发货、订单管理工具

## 简介

这是一个闲管家开放平台的 Python API 客户端，支持通过 API 进行：

- 订单查询和管理
- 自动发货
- 商品管理
- 余额查询
- 货源对接下单

## 安装

```bash
git clone https://github.com/kingofmarketing/xian-guanjia.git
cd xian-guanjia
pip install requests
```

## 使用方法

### Python 代码调用

```python
from xian_guanjia import XianGuanjiaClient

client = XianGuanjiaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    mch_id="your_mch_id",
    mch_secret="your_mch_secret"
)

# 查询订单列表
result = client.get_order_list(page=1, page_size=20)
print(result)

# 订单发货
result = client.ship_order(
    order_id=12345,
    logistics_no="7894561230",
    logistics_company="顺丰速运"
)

# 查询余额
result = client.query_balance()
print(result)
```

### 命令行使用

```bash
python scripts/xian_guanjia.py \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --mch-id YOUR_MCH_ID \
  --mch-secret YOUR_MCH_SECRET
```

## 签名算法

闲管家使用 MD5 签名认证，本客户端已经自动处理签名，无需手动计算。

详细的签名规则参见 [SKILL.md](SKILL.md) 或 [references/api-docs.md](references/api-docs.md)

## 错误码

| 错误码 | 错误描述 |
| --- | --- |
| 0 | 请求成功 |
| 401 | 签名错误 |
| 403 | IP不在白名单 |
| 408 | 时间戳过期 |
| 1000 | 商户不存在 |
| 1002 | 余额不足 |

完整错误码参见 [references/api-docs.md](references/api-docs.md)

## 许可证

MIT License

## 相关链接

- 闲管家官网：https://goofish.pro
- API 文档：https://apifox.com/apidoc/shared-cf4d53fd-8bb2-41c5-8da3-371ba9a38956/doc-4985015
