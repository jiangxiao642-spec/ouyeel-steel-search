#!/usr/bin/env python3
"""
欧冶自动搜索 — 使用 Selenium + Edge 浏览器
"""

import sys, time, csv, re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlrd

SHIPPING = {"上海": 350, "佛山": 150, "湛江": 170, "武汉": 300}

def read_excel(path):
    wb = xlrd.open_workbook(path)
    ws = wb.sheet_by_index(0)
    materials = []
    for r in range(1, ws.nrows):
        material = ws.cell_value(r, 1)
        spec = ws.cell_value(r, 2)
        demand = ws.cell_value(r, 3)
        if material and spec and demand:
            materials.append({
                "material": str(material).strip(),
                "spec": str(spec).strip(),
                "demand": float(demand),
            })
    return materials

def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Try to find msedgedriver
    driver_path = Path.home() / ".hermes" / "edgedriver" / "msedgedriver.exe"
    if driver_path.exists():
        service = Service(executable_path=str(driver_path))
    else:
        service = Service()
    
    driver = webdriver.Edge(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def search_material(driver, material, spec):
    """搜索一种材料，返回找到的报价列表"""
    query = f"{material} {spec}"
    url = f"https://www.ouyeel.com/xhb/search?keyword={query}"
    
    driver.get(url)
    time.sleep(5)  # 等页面加载和反爬检测
    
    results = []
    try:
        # 尝试找价格表格
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 5:
                text = " | ".join([c.text for c in cells])
                # 尝试解析价格
                price_match = re.findall(r'[\d,.]+', text)
                location_match = re.findall(r'(上海|佛山|湛江|武汉)', text)
                if price_match and location_match:
                    try:
                        price = float(price_match[-1].replace(',', ''))
                        location = location_match[0]
                        results.append({"price": price, "location": location})
                    except ValueError:
                        pass
    except Exception as e:
        print(f"  搜索 {material} {spec} 出错: {e}")
    
    return results

def main():
    if len(sys.argv) < 2:
        print("用法: python ouyeel_auto_search.py <Excel路径>")
        sys.exit(1)
    
    path = sys.argv[1]
    materials = read_excel(path)
    print(f"读取到 {len(materials)} 种材料")
    
    driver = setup_driver()
    print("Edge 浏览器已启动")
    
    all_prices = []
    
    for i, m in enumerate(materials):
        print(f"\n[{i+1}/{len(materials)}] 搜索: {m['material']} {m['spec']}")
        results = search_material(driver, m['material'], m['spec'])
        
        if results:
            print(f"  找到 {len(results)} 个报价")
            for r in results:
                print(f"    {r['location']}: {r['price']}元/吨")
                all_prices.append({
                    "material": m["material"],
                    "spec": m["spec"],
                    "location": r["location"],
                    "unit_price": r["price"],
                })
        else:
            print(f"  ⚠️ 未找到报价，尝试手动搜索")
            all_prices.append({
                "material": m["material"],
                "spec": m["spec"],
                "location": "需手动查",
                "unit_price": 0,
            })
        
        time.sleep(3)  # 避免触发反爬
    
    driver.quit()
    
    # 保存搜索结果
    output = Path(path).parent / "search_results.csv"
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["material", "spec", "location", "unit_price"])
        writer.writeheader()
        writer.writerows(all_prices)
    
    print(f"\n✅ 搜索结果保存到: {output}")
    print(f"共 {len(all_prices)} 条记录")
    print("\n下一步: python optimal_table.py 生成最优采购表")

if __name__ == "__main__":
    main()
