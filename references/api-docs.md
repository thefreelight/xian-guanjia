# 闲管家 API 文档

## 接入说明

生产环境地址：https://open.goofish.pro

## 相关文档

完整的 API 列表：

### 用户接口
- [查询闲鱼店铺](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586388.md)

### 商品接口
- [查询商品类目](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-97448687.md)
- [查询商品属性](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-95804125.md)
- [查询商品列表](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586381.md)
- [查询商品详情](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586380.md)
- [查询商品规格](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-165788779.md) - 仅多规格商品才能查询
- [创建商品（单个）](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586377.md)
- [创建商品（批量）](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586378.md)
- [上架商品](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-95038267.md)
- [下架商品](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586382.md)
- [编辑商品](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586379.md)
- [编辑库存](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586384.md)
- [删除商品](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586383.md)

### 订单接口
- [查询订单列表](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-95074856.md)
- [查询订单详情](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586385.md)
- [订单卡密列表](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-97142794.md)
- [订单物流发货](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586386.md)
- [订单修改价格](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-333703388.md)

### 推送回调接口
- [商品回调通知](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-98676477.md) - 请商家自行在上架商品和编辑商品接口填写真实的推送地址
- [商品推送通知](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-108700789.md) - 请商家自行在闲管家的开放平台填写真实的推送地址
- [订单推送通知](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-93586387.md) - 请商家自行在闲管家的开放平台填写真实的推送地址

### 其他接口
- [查询快递公司](https://s.apifox.cn/3ac13d69-5a38-4536-ae9b-a54001854ef8/api-97431955.md) - 如列表内没有需要的快递公司，可以联系闲管家技术支持补充

## 相关下载

- 闲管家省市区：
  - https://file.goofish.pro/doc/闲管家省市区.xlsx
  - https://file.goofish.pro/doc/闲管家省市区.sql

- 商品发布异常状态码及处理建议：
  - https://file.goofish.pro/doc/商品异常状态码.xlsx
  - https://file.goofish.pro/doc/商品异常状态码.sql

## 注意事项

1. 闲管家所有参数都是强校验，需要严格按照文档的字段类型传参+返回
2. 返回结果 `code = 0` 才是成功，其他值表示失败

## 签名规则说明

### 签名参数说明

```
app_id：管家平台提供的对接应用ID
app_secret：管家平台提供的对接密钥
mch_id：货源平台提供的对接商户ID
mch_secret：货源平台提供的对接密钥
timestamp：发起请求时的时间戳（秒）
bodyString：POST原文字符串
```

### 签名生成示例

```python
app_id = 677859093659717
app_secret = wK63PxlOBaY9NoqMksLeZySzGIW25ifA
mch_id = 100
mch_secret = o9wl81dncmvby3ijpq7eur456zhgtaxs
timestamp = 1724414553
body = {"goods_type":1,"goods_no":"12344532"}
```

### 拼接签名参数

```python
// 接口采用MD5加密算法生成签名值

// 报文值 = md5(Json格式的Body报文) 
bodyMd5 = md5({"goods_type":1,"goods_no":"12344532"}) 
// output：9b8030f5097d5ed123405b003dd247c5

// 接口无body参数时签名字符串（请求时body也需要传入相同的值）
// bodyMd5 = md5("{}") 或者 md5("")

// 签名值 = md5("管家应用ID,管家对接密钥,Body报文Md5值,时间戳,货源商户ID,货源对接密钥")
signMd5 = md5("677859093659717,wK63PxlOBaY9NoqMksLeZySzGIW25ifA,9b8030f5097d5ed123405b003dd247c5,1724414553,1001,o9wl81dncmvby3ijpq7eur456zhgtaxs")
// output：fda5954f48ab32b3b271c84450440ead
```

最终的签名值：`sign = fda5954f48ab32b3b271c84450440ead`

## 全局错误码说明

| 错误码 | 错误描述 |
| --- | --- |
| 0 | 请求成功 |
| 1 | 请求错误（不在定义范围内的错误） |
| 401 | 签名错误 |
| 403 | 访问IP不在IP白名单内 |
| 408 | 时间戳已超过有效期 |
| 500 | 系统异常，请重试 |
| 1000 | 商户不存在 |
| 1001 | 商户不可用 |
| 1002 | 商户余额不足 |
| 1100 | 商品不存在 |
| 1101 | 商品不可用 |
| 1102 | 商品库存不足 |
| 1200 | 订单不存在 |
| 1201 | 下单参数错误 |
| 1202 | 下单金额低于成本价 |
| 1203 | 下单管家订单号已存在 |
| 1209 | 下单超时，请查单确认下单结果 |
