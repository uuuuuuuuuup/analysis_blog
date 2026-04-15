#!/bin/bash

# 复制龟龟投资策略分析报告到 Hugo 内容目录

SOURCE_DIR="/Users/apple/Documents/分析报告/龟龟投资策略分析报告"
TARGET_DIR="/Users/apple/Documents/分析报告/investment-reports-site/content/reports"

# 股票代码列表
STOCKS=("000333" "000651" "000858" "000596" "002304" "000895" "000513" "600085" "600566" "600763" "002415" "300628" "002690" "600900" "600941" "601728" "001965" "002714" "002507" "603345" "002991" "003000" "002027" "002327" "002352" "002867" "600398" "002572" "603833" "600585" "600048" "600132" "603198" "300146" "300015" "300979" "600887" "600050" "603605" "000568")

for stock in "${STOCKS[@]}"; do
    source_path="$SOURCE_DIR/$stock"
    target_path="$TARGET_DIR/$stock"
    
    if [ -d "$source_path" ]; then
        echo "复制 $stock..."
        mkdir -p "$target_path"
        
        # 复制分析报告（查找包含"分析报告"的md文件）
        for file in "$source_path"/*分析报告*.md "$source_path"/analysis_report.md; do
            if [ -f "$file" ]; then
                cp "$file" "$target_path/"
                echo "  - 复制: $(basename "$file")"
            fi
        done
        
        # 复制数据包文件
        if [ -f "$source_path/data_pack_market.md" ]; then
            cp "$source_path/data_pack_market.md" "$target_path/"
            echo "  - 复制: data_pack_market.md"
        fi
        
        if [ -f "$source_path/data_pack_report.md" ]; then
            cp "$source_path/data_pack_report.md" "$target_path/"
            echo "  - 复制: data_pack_report.md"
        fi
    else
        echo "警告: $stock 目录不存在"
    fi
done

echo "复制完成！"
