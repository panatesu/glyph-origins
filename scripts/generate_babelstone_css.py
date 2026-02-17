import csv
import re

csv_file = "./babelglyph_coverage.csv"

# Keywords for blocks to INCLUDE
include_keywords = [
    "CJK",
    "Hiragana",
    "Katakana",
    "Bopomofo",
    "Kanbun",
    "Tibetan",
    "Mongolian",
    "Ideographic",
    "Radical",
    "Stroke",
    "Han",
    "Yijing",
    "Tai Xuan Jing",
    "Counting Rod",
    "Fullwidth",
    "Vertical Forms",
    "Small Form",
    "Variation Selectors",
    "Private Use Area",
    "Chess Symbols",
    "Specials",
    "Kana",
    "Yi",
    "Lisu",
    "Miao",
    "Tangut",
    "Nushu",
]

exclude_keywords = [
    "Latin",
    "Greek",
    "Cyrillic",
    "Hebrew",
    "Arabic",
    "Mathematical",
    "Technical",
    "Geometric",
    "Symbols for Legacy Computing",
    "Alphanumeric",
]


def should_include(block_name):
    for kw in exclude_keywords:
        if kw in block_name:
            return False
    for kw in include_keywords:
        if kw in block_name:
            return True
    return False


complete_ranges = []
partial_ranges = []
current_section = "complete"

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if not row:
            continue
        block = row[0]
        if block.startswith("#"):
            current_section = "partial"
            continue
        css_range = row[2]
        if should_include(block):
            if current_section == "complete":
                complete_ranges.append((block, css_range))
            else:
                partial_ranges.append((block, css_range))

# Prepare the range lines list (all_chunks)
all_chunks = []
if complete_ranges:
    all_chunks.append("    /* Complete Coverage Blocks */")
    for name, rng in complete_ranges:
        all_chunks.append(f"    {rng}, /* {name} */")

if partial_ranges:
    all_chunks.append("    /* Partial Coverage Blocks */")
    for name, rng in partial_ranges:
        all_chunks.append(f"    {rng}, /* {name} */")

# Remove trailing comma from the very last item if it exists
if all_chunks and "," in all_chunks[-1]:
    last = all_chunks[-1]
    idx = last.rfind(",")
    if idx != -1:
        all_chunks[-1] = last[:idx] + last[idx + 1 :]

# Join lines
range_content = "\n".join(all_chunks)

# Generate CSS
# Block 1: BabelStone Han (Webfont)
css_content = """@font-face {
  font-family: 'BabelStone Han';
  src: url('BabelStoneHan.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
  unicode-range:
"""
css_content += range_content
css_content += ";\n}\n\n"

# Block 2: SimSun-Ext (Backup local font with limited range)
css_content += """@font-face {
  font-family: 'SimSun-Ext';
  src: local('SimSun'), local('宋体'), local('Songti SC'), local('PMingLiU');
  font-weight: normal;
  font-style: normal;
  unicode-range:
"""
css_content += range_content
css_content += ";\n}\n"

print(css_content)
