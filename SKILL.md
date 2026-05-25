---
name: ouyeel-steel-search
description: "欧冶(ouyeel.com)钢材现货价格自动搜索 — Selenium + Edge 浏览器。输入采购Excel，输出含运杂费的最优采购表。"
---

# 欧冶钢材价格搜索 Skill

**用户需求：** 从欧冶(ouyeel.com)搜索钢材现货价格，结合各发货地运杂费，生成最优采购表。

## 核心功能

1. 读取采购 Excel → 逐条在欧冶搜索 → 提取各发货地单价
2. 结合运杂费标准 → 计算含运费总价 → 选最优发货地
3. 输出最优采购表 Excel

## 运杂费标准

| 发货地 | 元/件 |
|--------|-------|
| 上海 | 350 |
| 佛山 | 150 |
| 湛江 | 170 |
| 武汉 | 300 |

## 文件结构

```
ouyeel-steel-search/
├── SKILL.md
├── README.md
├── scripts/
│   ├── ouyeel_search.py          # 搜索清单生成器
│   ├── optimal_table.py          # 最优采购表计算
│   └── ouyeel_auto_search.py     # Selenium 全自动搜索
└── templates/
    └── install_and_run.bat       # 一键安装+运行
```

## 使用方式

### 方式一：全自动（推荐）
1. 安装 Python + Selenium + Edge WebDriver
2. 双击 `install_and_run.bat`
3. 等待浏览器自动搜索完成

### 方式二：半自动（备用）
1. `python3 ouyeel_search.py 采购表.xls` → 生成搜索链接清单
2. 手动在欧冶搜索，记录价格到 `prices.csv`
3. `python3 optimal_table.py materials.csv prices.csv` → 输出最优表

## 已知限制

- 欧冶有 `$_ts` 反爬保护，Selenium 可能被拦截
- 如自动搜索失败，回退到方式二
