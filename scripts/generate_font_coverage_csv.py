import re
import csv
import os

input_file = "./babelglyph_coverage.html"
output_file = "./babelglyph_coverage.csv"

# Check if file exists
if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
    exit(1)

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find tbody content
tbody_match = re.search(r"<tbody>(.*?)</tbody>", content, re.DOTALL)
if not tbody_match:
    print("No tbody found")
    exit(1)
tbody_content = tbody_match.group(1)

# Find rows
rows = re.findall(r"<tr>(.*?)</tr>", tbody_content, re.DOTALL)

complete_coverage = []
partial_coverage = []

for row in rows:
    # Find all tds with their attributes
    # We use non-greedy matching for content
    td_matches = re.findall(r"<td([^>]*)>(.*?)</td>", row, re.DOTALL)

    if len(td_matches) < 3:
        continue

    # Column 0: Block Name
    name = td_matches[0][1].strip()

    # Column 1: Range
    range_str = td_matches[1][1].strip()

    # Column 2: Coverage (check class in attributes)
    attrs_3, content_3 = td_matches[2]
    is_green = 'class="green"' in attrs_3
    coverage_text = content_3.strip()

    # Format range for CSS: 00000..0007F -> U+0000-007F
    parts = range_str.split("..")
    if len(parts) == 2:
        start, end = parts
        # Ensure proper hexadecimal format? They seem to be 5-digit hex in source.
        # CSS unicode-range usually drops leading zeros if possible but U+XXXX is standard.
        # Let's keep the source hex but add U+. Format: U+Start-End
        css_range = f"U+{start}-{end}"
    else:
        css_range = range_str

    item = {
        "Block": name,
        "OriginalRange": range_str,
        "CSSRange": css_range,
        "Coverage": coverage_text,
    }

    if is_green:
        complete_coverage.append(item)
    else:
        partial_coverage.append(item)

# Write to CSV
try:
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Block", "OriginalRange", "CSSRange", "Coverage"])

        for item in complete_coverage:
            writer.writerow(
                [
                    item["Block"],
                    item["OriginalRange"],
                    item["CSSRange"],
                    item["Coverage"],
                ]
            )

        # Add comment/separator as requested
        writer.writerow(["# Partial Coverage below", "", "", ""])

        for item in partial_coverage:
            writer.writerow(
                [
                    item["Block"],
                    item["OriginalRange"],
                    item["CSSRange"],
                    item["Coverage"],
                ]
            )

    print(f"CSV generated at {output_file}")
    print(f"Found {len(complete_coverage)} complete coverage blocks.")
    print(f"Found {len(partial_coverage)} partial coverage blocks.")

except Exception as e:
    print(f"Error writing CSV: {e}")
