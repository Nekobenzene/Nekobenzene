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

OPEN_DIV = '<div align="center">'
QUOTE_HEADING = '<h1 align="center">quote of the day</h1>'
SECTION_DIVIDER = '<!-- ============================================================ -->'
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
    lines = README_PATH.read_text(encoding="utf-8").splitlines(keepends=True)

    # Clean up any accidental quote block that got inserted near the top.
    open_idx = next((i for i, line in enumerate(lines) if line.strip() == OPEN_DIV), None)
    if open_idx is not None:
        divider_idx = next(
            (i for i in range(open_idx + 1, len(lines)) if lines[i].strip() == SECTION_DIVIDER),
            None,
        )
        if divider_idx is not None:
            lines = lines[: open_idx + 1] + ["\n"] + lines[divider_idx:]

    # Replace the actual quote-of-the-day block.
    heading_idx = next((i for i, line in enumerate(lines) if line.strip() == QUOTE_HEADING), None)
    if heading_idx is None:
        raise RuntimeError("Could not find quote of the day heading in README.md")

    divider_idx = next(
        (i for i in range(heading_idx + 1, len(lines)) if lines[i].strip() == SECTION_DIVIDER),
        None,
    )
    if divider_idx is None:
        raise RuntimeError("Could not find quote of the day divider in README.md")

    new_lines = (
        lines[: heading_idx + 1]
        + ["\n", f'> *"{quote}"*\n', "\n"]
        + lines[divider_idx:]
    )

    README_PATH.write_text("".join(new_lines), encoding="utf-8")
    print(f"Updated README with quote: {quote}")


def main():
    update_readme(get_todays_quote())


if __name__ == "__main__":
    main()
