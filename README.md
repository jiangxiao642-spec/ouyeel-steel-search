# 欧冶钢材价格搜索

> Hermes Agent Skill — 从欧冶自动搜索钢材现货价格，生成含运杂费的最优采购表。

## 快速开始

```bash
# 安装依赖
pip install selenium xlrd

# 下载 Edge WebDriver
# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# 放到: %USERPROFILE%\.hermes\edgedriver\

# 运行
python ouyeel_auto_search.py 采购表.xls
```

## 适用范围

- 汽车用钢现货采购（DC系列、双相钢DP、SAPH440等）
- 平台限定：欧冶(ouyeel.com)
- 发货地：上海/佛山/湛江/武汉

## 作者

陈一 + 小鹿  
MIT 协议
