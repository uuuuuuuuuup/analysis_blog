#!/usr/bin/env python3
"""
提取所有报告的投资结论数据
支持两种格式：
1. decision-card-v2 shortcode
2. 旧格式的"最终决策"表格
"""

import os
import re
import json
from pathlib import Path

def extract_decision_card(content):
    """从报告内容中提取 decision-card-v2 参数"""
    pattern = r'\{\{<\s*decision-card-v2\s+([^>]+)>\}\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    params_str = match.group(1)
    
    result = {}
    
    decision_match = re.search(r'decision="([^"]+)"', params_str)
    if decision_match:
        result['decision'] = decision_match.group(1)
    
    position_match = re.search(r'position="([^"]+)"', params_str)
    if position_match:
        result['position'] = position_match.group(1)
    
    targetPrice_match = re.search(r'targetPrice="([^"]+)"', params_str)
    if targetPrice_match:
        result['targetPrice'] = targetPrice_match.group(1)
    
    currentPrice_match = re.search(r'currentPrice="([^"]+)"', params_str)
    if currentPrice_match:
        result['currentPrice'] = currentPrice_match.group(1)
    
    priority_match = re.search(r'priority="([^"]+)"', params_str)
    if priority_match:
        result['priority'] = priority_match.group(1)
    
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
        if '买入' in pos or '仓位' in pos:
            result['decision'] = 'buy' if '买入' in pos else 'observe'
        elif '不建仓' in pos or '暂不' in pos or '观望' in pos:
            result['decision'] = 'wait'
        else:
            result['decision'] = 'observe'
    
    return result if result else None

def extract_stock_info(content):
    """从报告内容中提取股票信息"""
    result = {}
    
    title_match = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
    if title_match:
        result['title'] = title_match.group(1)
    
    company_match = re.search(r'company="([^"]+)"', content)
    if company_match:
        result['company'] = company_match.group(1)
    
    code_match = re.search(r'code="([^"]+)"', content)
    if code_match:
        result['code'] = code_match.group(1)
    
    h1_match = re.search(r'^#\s*(.+?)(?:（|\(|\s*稳健|\s*$)', content, re.MULTILINE)
    if h1_match and 'company' not in result:
        result['company'] = h1_match.group(1).strip()
    
    stock_code_match = re.search(r'[（\(](\d{6})[）\)]', content)
    if stock_code_match and 'code' not in result:
        result['code'] = stock_code_match.group(1)
    
    return result

def process_reports(reports_dir):
    """处理所有报告文件"""
    reports_path = Path(reports_dir)
    results = []
    
    for stock_dir in sorted(reports_path.iterdir()):
        if not stock_dir.is_dir():
            continue
        
        stock_code = stock_dir.name
        
        md_files = list(stock_dir.glob("*.md"))
        analysis_files = [f for f in md_files if 'analysis' in f.name.lower() or '稳健投资策略' in f.name]
        
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
                    stock_info = extract_stock_info(content)
                    
                    company_name = stock_info.get('company', '未知')
                    if '稳健投资策略' in company_name:
                        company_name = company_name.replace('稳健投资策略分析报告', '').replace('（', '').replace('）', '').strip()
                    
                    results.append({
                        'code': stock_code,
                        'company': company_name,
                        'decision': decision,
                        'file': str(md_file)
                    })
                    break
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
    
    return results

def calculate_distance(current_price, target_price):
    """计算距离目标价的百分比"""
    try:
        current = float(re.sub(r'[^\d.]', '', current_price.split('/')[0].split('（')[0]))
        target = float(re.sub(r'[^\d.]', '', target_price.split('/')[0].split('（')[0]))
        if current > 0:
            return f"{((target - current) / current * 100):.1f}%"
    except:
        pass
    return "-"

def main():
    reports_dir = "/Users/apple/Documents/分析报告/investment-reports-site/content/reports"
    
    results = process_reports(reports_dir)
    
    print(f"找到 {len(results)} 份报告\n")
    
    print("| 股票代码 | 公司名称 | 投资建议 | 建议仓位 | 目标买入价 | 当前股价 | 优先级 |")
    print("|:---:|:---|:---:|:---|:---:|:---:|:---|")
    
    for r in sorted(results, key=lambda x: x['code']):
        d = r['decision']
        decision_map = {
            'buy': '建议买入',
            'observe': '观察等待',
            'wait': '暂不操作'
        }
        decision_text = decision_map.get(d.get('decision', ''), d.get('decision', '未知'))
        
        print(f"| {r['code']} | {r['company']} | {decision_text} | {d.get('position', '-')} | {d.get('targetPrice', '-')} | {d.get('currentPrice', '-')} | {d.get('priority', '-')} |")
    
    print("\n\n=== JSON 数据 ===\n")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
