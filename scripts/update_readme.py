#!/usr/bin/env python3
"""
Daily quote updater for README.md.
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"
QUOTES_PATH = ROOT_DIR / "config" / "quotes.json"

QUOTE_START = "<!-- quote-of-day:start -->"
QUOTE_END = "<!-- quote-of-day:end -->"
FALLBACK_TEXT = "Keep coding, stay purr-sonal!"


def get_todays_quote():
    try:
        with open(QUOTES_PATH, "r", encoding="utf-8") as f:
            quotes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return FALLBACK_TEXT

    if not quotes:
        return FALLBACK_TEXT

    today = datetime.now().strftime("%Y%m%d")
    return quotes[int(today) % len(quotes)]


def update_readme(quote):
    content = README_PATH.read_text(encoding="utf-8")

    start_idx = content.find(QUOTE_START)
    end_idx = content.find(QUOTE_END)

    if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
        raise RuntimeError("Could not find quote-of-day markers in README.md")

    end_idx += len(QUOTE_END)

    new_block = (
        f"{QUOTE_START}\n"
        '<h1 align="center">quote of the day</h1>\n\n'
        f'> *"{quote}"*\n\n'
        f"{QUOTE_END}"
    )

    new_content = content[:start_idx] + new_block + content[end_idx:]
    README_PATH.write_text(new_content, encoding="utf-8")
    print(f"Updated README with quote: {quote}")


def main():
    update_readme(get_todays_quote())


if __name__ == "__main__":
    main()
