# 长沙智拓无界面试

本仓库包含 5 个 Python 面试题解答，涵盖列表去重算法与三个电商网站（Shopify 系统）的数据抓取，以及一个接口翻页采集练习。

## 环境准备

- Python 3.8+
- 安装依赖：

```bash
pip install requests
```

## 文件说明

### test1.py —— 列表去重的三种方法

**思路：** 对 `[3, 1, 2, 3, 4, 1, 2]` 去重并保持原始顺序，分别用三种方式实现：

1. 遍历原列表，用 `not in` 判断结果列表中不存在则追加（最直观，但 O(n²)）；
2. 利用 `dict.fromkeys()` 天然去重且保留插入顺序的特性，一行实现；
3. 用一个 `set` 记录已出现的元素，配合列表遍历，查询效率 O(1)，兼顾顺序与性能。

**运行：**

```bash
python test1.py
```

### test2.py —— Cosrx 全站商品采集（cosrx_products.csv）

**思路：**

1. 请求 Shopify 站点公开的 `/collections/all/products.json` 接口，循环翻 5 页拿到全量商品；
2. 过滤掉赠品（`FREEGIFT_HIDDEN`）和标签含 "Not available" 的下架商品；
3. 用正则 + `html.unescape` 把富文本 `body_html` 清洗成纯文本，再按标签（Key Ingredients、Size 等）逐项提取字段；
4. 价格取所有变体中的最低现价与划线价的最大值；图片协议补全 `https:`；尺码从 options 中模糊匹配 size/volume 收集并去重；
5. 结果写入 CSV（`utf-8-sig` 编码，保证 Excel 打开中文不乱码）。

**运行：**

```bash
python test2.py
```

### test3.py —— Quest Nutrition 蛋白棒商品列表采集（quest_products.csv）

**思路：** 请求 Quest 官网（Shopify 系统）蛋白棒合集的 `products.json` 接口，一次性获取全部商品，遍历每个商品提取 `handle`（URL 标识）、`title`（标题）以及所有 SKU 的 `variant id`（逗号拼接），写入 CSV。该接口无需翻页参数，一次请求即返回合集全量数据。

**运行：**

```bash
python test3.py
```

### test4.py —— 单个商品详情页数据解析

**思路：** 请求 Shopify 商品详情接口（商品页 URL 加 `.js` 后缀即返回 JSON），针对单个商品解析：

- 标题、现价与划线价（接口返回"分"，除以 100 转美元格式化）；
- 颜色：优先取第一个**有库存**变体的 `option1`，无库存时回退到颜色选项第一个值；
- 尺码：直接取 Size 选项的全部可选值；
- 图片：补全协议前缀并列出全部链接。

**运行：**

```bash
python test4.py
```

### test5.py —— 接口翻页采集与求和

**思路：** 请求目标接口循环翻 5 页采集数字列表。关键点：接口对第 5 页做了校验，需要将 `User-Agent` 替换为指定值（`yuanrenxue`）才能正常返回数据，因此在循环内对最后一页动态修改请求头；最终将 5 页数据汇总求和输出。

**运行：**

```bash
python test5.py
```

## 目录结构

```
├── test1.py             # 列表去重三种方法
├── test2.py             # Cosrx 商品采集 → cosrx_products.csv
├── test3.py             # Quest 蛋白棒采集 → quest_products.csv
├── test4.py             # 单商品详情解析
├── test5.py             # 接口翻页采集求和
├── cosrx_products.csv   # test2 输出结果
└── quest_products.csv   # test3 输出结果
```
