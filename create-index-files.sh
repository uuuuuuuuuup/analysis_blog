#!/bin/bash

# 为每个股票创建索引文件

REPORTS_DIR="/Users/apple/Documents/分析报告/investment-reports-site/content/reports"

for stock_dir in "$REPORTS_DIR"/*/; do
    if [ -d "$stock_dir" ]; then
        stock_code=$(basename "$stock_dir")
        index_file="$stock_dir/_index.md"
        
        # 查找分析报告文件名
        analysis_file=$(find "$stock_dir" -name "*分析报告*.md" -o -name "analysis_report.md" | head -1)
        
        if [ -f "$analysis_file" ]; then
            # 从文件名提取股票名称
            filename=$(basename "$analysis_file" .md)
            stock_name=$(echo "$filename" | sed 's/_.*//' | sed 's/analysis_report/分析报告/')
            
            cat > "$index_file" << EOF
---
title: "${stock_name} (${stock_code})"
linkTitle: "${stock_name}"
weight: 10
type: docs
---

# ${stock_name} (${stock_code})

## 📄 报告文件

- [分析报告]($(basename "$analysis_file"))
- [市场数据包](data_pack_market.md)
- [研报数据包](data_pack_report.md)

---

**股票代码**：${stock_code}  
**分析框架**：龟龟投资策略 v2.0
EOF
            echo "创建索引: $stock_code"
        fi
    fi
done

echo "索引文件创建完成！"
