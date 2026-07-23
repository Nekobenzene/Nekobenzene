#!/usr/bin/env python3
"""
Daily quote updater for README.md
Uses date-based hash to select a quote from quotes.json
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
README_PATH = ROOT_DIR / "README.md"
QUOTES_PATH = ROOT_DIR / "config" / "quotes.json"


def get_todays_quote():
    """根据日期哈希值从配置文件中选取一句鸡汤"""
    try:
        with open(QUOTES_PATH, "r", encoding="utf-8") as f:
            quotes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Keep coding, stay purr-sonal! 🐾"

    if not quotes:
        return "Keep coding, stay purr-sonal! 🐾"

    # 用日期的 YYYYMMDD 作为种子，生成一个伪随机索引
    today = datetime.now().strftime("%Y%m%d")
    seed = int(today)

    # 简单的伪随机算法：使用 hash 取余
    # 避免使用 random 模块以保证可复现
    index = seed % len(quotes)
    return quotes[index]


def update_readme(quote):
    """更新 README.md 中的引用区块"""
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 查找并替换 quote of the day 区块
    # 匹配从 "<!-- ============ quote of the day ..." 到下一个 "---" 或 "<!--"
    pattern = r'(<!-- ============================================================\n     quote of the day.*?-->)\n\n> .*?\n\n(<!-- ============================================================)'

    replacement = r'\1\n\n> *"' + quote + r'"*\n\n\2'

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 如果替换失败（pattern 没匹配上），在文件末尾追加
    if new_content == content:
        # 在 footer 之前插入
        footer_pattern = r'(<!-- ============================================================\n     .*?底部.*?-->.*?)(<img src="https://capsule-render\.vercel\.app/api)'
        quote_block = f'\n> *"{quote}"*\n\n'
        new_content = re.sub(footer_pattern, quote_block + r'\1\2', content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ README updated with quote: {quote}")


def main():
    quote = get_todays_quote()
    update_readme(quote)


if __name__ == "__main__":
    main()
