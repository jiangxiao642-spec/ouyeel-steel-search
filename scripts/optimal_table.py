#!/usr/bin/env python3
"""
最优采购表生成器

输入: prices.csv (材质,规格,发货地,单价)
输出: 最优采购表 Excel
"""

import csv
import sys
from pathlib import Path

SHIPPING = {"上海": 350, "佛山": 150, "湛江": 170, "武汉": 300}

def compute_optimal(materials, prices):
    """每种材料选含运费总价最低的发货地"""
    output = []
    for m in materials:
        candidates = []
        for p in prices:
            if p["material"] == m["material"] and p["spec"] == m["spec"]:
                unit_price = float(p["unit_price"])
                shipping = SHIPPING.get(p["location"], 0)
                total = unit_price * m["demand"] + shipping
                candidates.append({
                    "material": m["material"],
                    "spec": m["spec"],
                    "demand": m["demand"],
                    "location": p["location"],
                    "unit_price": unit_price,
                    "shipping": shipping,
                    "total": total,
                })
        if candidates:
            best = min(candidates, key=lambda x: x["total"])
            output.append(best)
        else:
            output.append({
                "material": m["material"],
                "spec": m["spec"],
                "demand": m["demand"],
                "location": "无报价",
                "unit_price": 0,
                "shipping": 0,
                "total": 0,
            })
    return output

def main():
    if len(sys.argv) < 3:
        print("用法: python3 optimal_table.py <materials.csv> <prices.csv>")
        sys.exit(1)
    
    materials = []
    with open(sys.argv[1]) as f:
        for row in csv.DictReader(f):
            materials.append(row)
    
    prices = []
    with open(sys.argv[2]) as f:
        for row in csv.DictReader(f):
            prices.append(row)
    
    result = compute_optimal(materials, prices)
    
    print(f"{'材质':<15} {'规格':<15} {'需求(T)':>8} {'最优发货地':<8} {'单价(元/T)':>10} {'运费':>8} {'总价(元)':>12}")
    print("-" * 80)
    total_cost = 0
    for r in result:
        print(f"{r['material']:<15} {r['spec']:<15} {r['demand']:>8.0f} {r['location']:<8} {r['unit_price']:>10.0f} {r['shipping']:>8.0f} {r['total']:>12.0f}")
        total_cost += r['total']
    print("-" * 80)
    print(f"{'合计':>56} {total_cost:>12.0f}")

if __name__ == "__main__":
    main()
