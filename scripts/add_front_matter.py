#!/usr/bin/env python3
"""
为缺少 front matter 的报告添加标题
"""

import os
import re
from pathlib import Path

REPORTS_DIR = "/Users/apple/Documents/分析报告/investment-reports-site/content/reports"

COMPANY_NAMES = {
    '000858': '五粮液',
    '000895': '双汇发展',
    '001965': '招商公路',
    '002027': '分众传媒',
    '002304': '洋河股份',
    '002327': '富安娜',
    '002352': '顺丰控股',
    '002415': '海康威视',
    '002507': '涪陵榨菜',
    '002572': '索菲亚',
    '300979': '华利集团',
    '600566': '济川药业',
    '601728': '中国电信',
}

def add_front_matter(file_path, code, company_name):
    """为文件添加 front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        print(f"  跳过 {code}，已有 front matter")
        return False
    
    front_matter = f'''---
title: "{company_name}（{code}）稳健投资策略分析报告"
date: 2026-04-15
draft: false
---

'''
    
    new_content = front_matter + content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ 已添加 front matter: {company_name}")
    return True

def main():
    print("开始添加 front matter...\n")
    
    count = 0
    for code, company_name in COMPANY_NAMES.items():
        dir_path = Path(REPORTS_DIR) / code
        if not dir_path.exists():
            print(f"  ⚠️ 目录不存在: {code}")
            continue
        
        md_files = list(dir_path.glob("*稳健投资策略分析报告.md"))
        if not md_files:
            print(f"  ⚠️ 文件不存在: {code}")
            continue
        
        if add_front_matter(md_files[0], code, company_name):
            count += 1
    
    print(f"\n完成！共添加 {count} 个 front matter")

if __name__ == "__main__":
    main()
