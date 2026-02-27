from pathlib import Path
from bs4 import BeautifulSoup
import re
import subprocess
import sys

if len(sys.argv) != 5:
    print("Usage: python port_from_wordpress.py <file> <title> <date> <tags>")
    sys.exit(1)

file, title, date, tags = sys.argv[1:]
file = Path(file)

frontmatter = f"""
+++
title = "{title}"
date = {date}
tags = {tags}
+++
"""

html_file = Path(file).read_text(encoding="utf-8")
bs = BeautifulSoup(html_file, "html.parser")

# Find p.has-large-font-size
for p in bs.find_all("p", class_="has-large-font-size"):
    h1 = bs.new_tag("h1")
    h1.string = p.text.strip()
    p.replace_with(h1)

# Remove all classes from bs
for tag in bs.find_all(class_=True):
    del tag["class"]

# Remove strong inside any title h1, h2, h3
for tag in bs.find_all(["h1", "h2", "h3"]):
    for strong in tag.find_all("strong"):
        strong.replace_with(strong.string)

# Send string to pandoc
output = subprocess.run(
    ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
    input=str(bs),
    capture_output=True,
    text=True,
    encoding="utf-8",
)
file = output.stdout

# Shorten line breaks
file = re.sub(r"""--+""", "---", file)

# Replace figures with shortcodes
figure_re = re.compile(r"""<figure>(.+?)</figure>""", flags=re.DOTALL)
def repl_fun(match):
    soup = BeautifulSoup(match.group(0), "html.parser")
    img = soup.img
    img_src = img.attrs.get("data-orig-file", img.attrs.get("src"))
    return (
        "{{< figure \n" +
        f'  src="{img_src}"\n' +
        f'  link="{img_src}"\n' +
        ">}}"
    )
file = figure_re.sub(repl_fun, file)
file = frontmatter + file
Path(file.with_suffix(".md")).write_text(file, encoding="utf-8")
