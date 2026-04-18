#!/usr/bin/env python3
"""
生成投资汇总表格
"""

import os
import re
import json
from pathlib import Path

COMPANY_NAMES = {
    '000333': '美的集团',
    '000513': '丽珠集团',
    '000568': '泸州老窖',
    '000596': '古井贡酒',
    '000651': '格力电器',
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
    '002690': '美亚光电',
    '002714': '牧原股份',
    '002867': '周大生',
    '002991': '甘源食品',
    '003000': '劲仔食品',
    '300015': '爱尔眼科',
    '300146': '汤臣倍健',
    '300628': '亿联网络',
    '300979': '华利集团',
    '600048': '保利发展',
    '600050': '中国联通',
    '600085': '同仁堂',
    '600132': '重庆啤酒',
    '600398': '海澜之家',
    '600566': '济川药业',
    '600585': '海螺水泥',
    '600763': '通策医疗',
    '600887': '伊利股份',
    '600900': '长江电力',
    '600941': '中国移动',
    '601728': '中国电信',
    '603198': '迎驾贡酒',
    '603345': '安井食品',
    '603605': '珀莱雅',
    '603833': '欧派家居',
}

def extract_decision_card(content):
    """从报告内容中提取 decision-card-v2 参数"""
    pattern = r'\{\{<\s*decision-card-v2\s+([^>]+)>\}\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    params_str = match.group(1)
    result = {}
    
    for key in ['decision', 'position', 'targetPrice', 'currentPrice', 'priority']:
        match = re.search(rf'{key}="([^"]+)"', params_str)
        if match:
            result[key] = match.group(1)
    
    return result

def extract_old_format_decision(content):
    """从旧格式报告中提取最终决策数据"""
    result = {}
    
    patterns = [
        (r'\|\s*\*\*投资建议\*\*\s*\|\s*\*\*([^|]+)\*\*\s*\|', 'position'),
        (r'\|\s*投资建议\s*\|\s*([^|]+)\s*\|', 'position'),
        (r'\|\s*\*\*目标买入价\*\*\s*\|\s*\*\*([^|]+)\*\*\s*\|', 'targetPrice'),
        (r'\|\s*目标买入价\s*\|\s*\*\*([^|]+)\*\*\s*\|', 'targetPrice'),
        (r'\|\s*目标买入价\s*\|\s*([^|]+)\s*\|', 'targetPrice'),
        (r'\|\s*当前股价\s*\|\s*([^|]+)\s*\|', 'currentPrice'),
        (r'\|\s*优先级\s*\|\s*\*\*([^|]+)\*\*\s*\|', 'priority'),
        (r'\|\s*优先级\s*\|\s*([^|]+)\s*\|', 'priority'),
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, content)
        if match and key not in result:
            result[key] = match.group(1).strip()
    
    if 'position' in result:
        pos = result['position']
        if '买入' in pos or ('仓位' in pos and '不建仓' not in pos and '暂不' not in pos and '观察仓位' not in pos):
            result['decision'] = 'buy'
        elif '不建仓' in pos or '暂不' in pos or '排除' in pos:
            result['decision'] = 'wait'
        else:
            result['decision'] = 'observe'
    
    return result if result else None

def clean_value(value):
    """清理值中的markdown格式"""
    if not value:
        return '-'
    value = re.sub(r'\*\*', '', value)
    value = re.sub(r'🔍|⚠️', '', value)
    value = value.strip()
    return value if value else '-'

def process_reports(reports_dir):
    """处理所有报告文件"""
    reports_path = Path(reports_dir)
    results = {}
    
    for stock_dir in sorted(reports_path.iterdir()):
        if not stock_dir.is_dir():
            continue
        
        stock_code = stock_dir.name
        if stock_code not in COMPANY_NAMES:
            continue
        
        md_files = list(stock_dir.glob("*.md"))
        analysis_files = [f for f in md_files if '稳健投资策略分析报告' in f.name]
        
        if analysis_files:
            md_files = analysis_files
        
        for md_file in md_files:
            if 'data_pack' in md_file.name or '_index' in md_file.name:
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                decision = extract_decision_card(content)
                
                if not decision:
                    decision = extract_old_format_decision(content)
                
                if decision:
                    results[stock_code] = {
                        'code': stock_code,
                        'company': COMPANY_NAMES[stock_code],
                        'decision': decision,
                    }
                    break
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
    
    return results

def generate_table(results):
    """生成汇总表格"""
    lines = []
    lines.append("| 股票代码 | 股票名称 | 当前股价 | 买入目标价 | 投资建议 | 优先级 |")
    lines.append("|:---:|:---|:---:|:---:|:---|:---|")
    
    decision_map = {
        'buy': '建议买入',
        'observe': '观察等待',
        'wait': '暂不操作'
    }
    
    for code in sorted(results.keys()):
        r = results[code]
        d = r['decision']
        
        current_price = clean_value(d.get('currentPrice', '-'))
        target_price = clean_value(d.get('targetPrice', '-'))
        position = clean_value(d.get('position', '-'))
        priority = clean_value(d.get('priority', '-'))
        decision_text = decision_map.get(d.get('decision', ''), '未知')
        
        if target_price == '-':
            target_price_display = '-'
        else:
            target_price_display = f"**{target_price}**"
        
        lines.append(f"| {code} | {r['company']} | {current_price} | {target_price_display} | {position} | {priority} |")
    
    return '\n'.join(lines)

def main():
    reports_dir = "/Users/apple/Documents/分析报告/investment-reports-site/content/reports"
    
    results = process_reports(reports_dir)
    
    print(f"找到 {len(results)} 份报告\n")
    
    table = generate_table(results)
    print(table)
    
    output_file = "/Users/apple/Documents/分析报告/investment-reports-site/scripts/summary_table.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(table)
    
    print(f"\n表格已保存到: {output_file}")

if __name__ == "__main__":
    main()
