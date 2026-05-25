#!/usr/bin/env python3
"""
欧冶钢材价格搜索 + 最优采购表生成

用法:
  python3 ouyeel_search.py <excel_path>
  
流程:
  1. 读 Excel 采购表
  2. 在欧冶(ouyeel.com)搜索每种材料
  3. 记录各地发货价格
  4. 结合运杂费计算最优采购方案
  5. 输出最优采购表 Excel
"""

import sys
import xlrd
from pathlib import Path

# 运杂费标准
SHIPPING = {
    "上海": 350,
    "佛山": 150,
    "湛江": 170,
    "武汉": 300,
}

def read_excel(path):
    """读取采购表，返回材料列表"""
    wb = xlrd.open_workbook(path)
    ws = wb.sheet_by_index(0)
    materials = []
    for r in range(1, ws.nrows):
        seq = ws.cell_value(r, 0)
        material = ws.cell_value(r, 1)
        spec = ws.cell_value(r, 2)
        demand = ws.cell_value(r, 3)
        if material and spec and demand:
            materials.append({
                "seq": seq,
                "material": str(material).strip(),
                "spec": str(spec).strip(),
                "demand": float(demand),
            })
    return materials

def generate_search_urls(materials):
    """为每种材料生成欧冶搜索 URL"""
    urls = []
    for m in materials:
        # 构造搜索关键词：材质+规格
        query = f"{m['material']} {m['spec']}"
        url = f"https://www.ouyeel.com/xhb/search?keyword={query}"
        urls.append((m, url))
    return urls

def main():
    if len(sys.argv) < 2:
        print("用法: python3 ouyeel_search.py <excel路径>")
        sys.exit(1)
    
    path = sys.argv[1]
    if not Path(path).exists():
        print(f"文件不存在: {path}")
        sys.exit(1)
    
    materials = read_excel(path)
    print(f"读取到 {len(materials)} 种材料")
    
    urls = generate_search_urls(materials)
    
    print("\n=== 需要在欧冶搜索以下材料 ===")
    print("格式: 材质,规格,需求(T),搜索URL")
    print()
    for m, url in urls:
        print(f"{m['material']},{m['spec']},{m['demand']},{url}")
    
    print(f"\n=== 运杂费标准 ===")
    for loc, fee in SHIPPING.items():
        print(f"  {loc}: {fee}元/件")
    
    print(f"\n共 {len(urls)} 个搜索链接。请在浏览器中打开搜索，记录每个发货地的最优单价。")
    print("记录格式: 材质,规格,发货地,单价(元/吨)")
    print()
    print("下一步: 将搜索结果保存为 prices.csv，运行 optimal_table.py 生成最优采购表")

if __name__ == "__main__":
    main()
