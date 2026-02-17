# %%
from bs4 import BeautifulSoup
from io import StringIO


urls = {
    1: "https://telegra.ph/Glyph-Origins-1-12-16",
    3: "https://telegra.ph/Glyph-Origins-3-02-02",
    5: "https://telegra.ph/Glyph-Origins-5-12-17",
    7: "https://telegra.ph/Glyph-Origins-7-12-17",
    9: "https://telegra.ph/Glyph-Origins-9-12-17",
    10: "https://telegra.ph/Glyph-Origins-10-01-06",
    12: "https://telegra.ph/Glyph-Origins-12-12-17",
    13: "https://telegra.ph/Glyph-Origins-13-01-31",
    15: "https://telegra.ph/Glyph-Origins-15-02-02",
    17: "https://telegra.ph/Glyph-Origins-17-12-18",
    19: "https://telegra.ph/Glyph-Origins-19-12-18",
    20: "https://telegra.ph/Glyph-Origins-20-02-03",
    21: "https://telegra.ph/Glyph-Origins-21-02-04",
    24: "https://telegra.ph/Glyph-Origins-24-12-18",
    26: "https://telegra.ph/Glyph-Origins-26-02-01",
    27: "https://telegra.ph/Glyph-Origins-27-02-03",
    29: "https://telegra.ph/Glyph-Origins-29-02-03",
    30: "https://telegra.ph/Glyph-Origins-30-12-18",
    31: "https://telegra.ph/Glyph-Origins-31-12-18",
    32: "https://telegra.ph/Glyph-Origins-32-01-27",
    33: "https://telegra.ph/Glyph-Origins-33-12-18",
    36: "https://telegra.ph/Glyph-Origins-36-12-18",
    37: "https://telegra.ph/Glyph-Origins-37-12-18",
    38: "https://telegra.ph/Glyph-Origins-38-12-18",
    39: "https://telegra.ph/Glyph-Origins-39-12-18",
    40: "https://telegra.ph/Glyph-Origins-40-12-18",
    41: "https://telegra.ph/Glyph-Origins-41-02-03",
    42: "https://telegra.ph/Glyph-Origins-42-12-18",
    44: "https://telegra.ph/Glyph-Origins-44-02-04",
    46: "https://telegra.ph/Glyph-Origins-46-12-18",
    47: "https://telegra.ph/Glyph-Origins-47-02-01",
    48: "https://telegra.ph/Glyph-Origins-48-01-31",
    50: "https://telegra.ph/Glyph-Origins-50-12-18",
    51: "https://telegra.ph/Glyph-Origins-51-12-18",
    54: "https://telegra.ph/Glyph-Origins-54-02-01",
    56: "https://telegra.ph/Glyph-Origins-56-02-02",
    57: "https://telegra.ph/Glyph-Origins-57-02-02",
    58: "https://telegra.ph/Glyph-Origins-58-12-19",
    61: "https://telegra.ph/Glyph-Origins-61-12-18",
    62: "https://telegra.ph/Glyph-Origins-62-02-01",
    63: "https://telegra.ph/Glyph-Origins-63-02-01",
    64: "https://telegra.ph/Glyph-Origins-64-12-18",
    72: "https://telegra.ph/Glyph-Origins-72-12-18",
    74: "https://telegra.ph/Glyph-Origins-74-12-18",
    75: "https://telegra.ph/Glyph-Origins-75-12-18",
    76: "https://telegra.ph/Glyph-Origins-76-01-27",
    77: "https://telegra.ph/Glyph-Origins-77-02-01",
    78: "https://telegra.ph/Glyph-Origins-78-12-18",
    80: "https://telegra.ph/Glyph-Origins-80-12-18",
    84: "https://telegra.ph/Glyph-Origins-84-01-31",
    85: "https://telegra.ph/Glyph-Origins-85-12-18",
    86: "https://telegra.ph/Glyph-Origins-86-12-18",
    92: "https://telegra.ph/Glyph-Origins-92-02-01",
    93: "https://telegra.ph/Glyph-Origins-93-12-18",
    94: "https://telegra.ph/Glyph-Origins-94-12-18",
    96: "https://telegra.ph/Glyph-Origins-96-12-18",
    100: "https://telegra.ph/Glyph-Origins-100-12-18",
    102: "https://telegra.ph/Glyph-Origins-102-12-18",
    103: "https://telegra.ph/Glyph-Origins-103-02-01",
    109: "https://telegra.ph/Glyph-Origins-109-12-18",
    110: "https://telegra.ph/Glyph-Origins-110-02-05",
    112: "https://telegra.ph/Glyph-Origins-112-02-01",
    113: "https://telegra.ph/Glyph-Origins-113-12-18",
    114: "https://telegra.ph/Glyph-Origins-114-12-18",
    116: "https://telegra.ph/Glyph-Origins-116-12-19",
    118: "https://telegra.ph/Glyph-Origins-118-12-19",
    120: "https://telegra.ph/Glyph-Origins-120-12-18",
    128: "https://telegra.ph/Glyph-Origins-128-12-18",
    130: "https://telegra.ph/Glyph-Origins-130-02-04",
    140: "https://telegra.ph/Glyph-Origins-140-12-18",
    146: "https://telegra.ph/Glyph-Origins-146-02-02",
    147: "https://telegra.ph/Glyph-Origins-147-12-18",
    151: "https://telegra.ph/Glyph-Origins-151-12-19",
    154: "https://telegra.ph/Glyph-Origins-154-12-18",
    155: "https://telegra.ph/Glyph-Origins-155-02-01",
    157: "https://telegra.ph/Glyph-Origins-157-01-27",
    159: "https://telegra.ph/Glyph-Origins-159-12-18",
    162: "https://telegra.ph/Glyph-Origins-162-02-01",
    167: "https://telegra.ph/Glyph-Origins-167-01-31",
    169: "https://telegra.ph/Glyph-Origins-169-02-02",
    173: "https://telegra.ph/Glyph-Origins-173-12-18",
    174: "https://telegra.ph/Glyph-Origins-174-02-01",
    176: "https://telegra.ph/Glyph-Origins-176-02-04",
    180: "https://telegra.ph/Glyph-Origins-180-12-18",
    181: "https://telegra.ph/Glyph-Origins-181-02-04",
    187: "https://telegra.ph/Glyph-Origins-187-12-18",
    215: "https://telegra.ph/Glyph-Origins-215-Other-02-04",
}
# %%
import urllib.request
import time

soups = {}

for radical_i, url in urls.items():
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soups[radical_i] = BeautifulSoup(html, "html.parser")
    time.sleep(0.3)

# %%
import subprocess
import re
from pathlib import Path

root = Path("/home/sentr/hdd/etc/panates/old_files/glyphs")
title_re = re.compile(r"^(.+?) \(U\+(.+?)\)$")
pandoc_cmd = "/home/sentr/Programs/miniconda3/envs/web/bin/pandoc"

# %%
for radical_i, soup in soups.items():
    article = soup.body.article
    sections = []
    current_section = []
    found_h3 = False

    for tag in article.children:
        if tag.name == "h3":
            found_h3 = True
            if current_section:
                sections.append(current_section)
            current_section = [tag.text]
        elif found_h3:
            if tag.name != "figure":
                current_section.append(tag)
            else:
                current_section.append(tag.img)

    if current_section:
        sections.append(current_section)

    sections = {x[0]: x[1:] for x in sections}

    markdown_sections = {}
    for key, section in sections.items():
        # Join the tags into a single HTML string
        section_html = "".join(str(tag) for tag in section)

        # Run pandoc
        try:
            proc = subprocess.run(
                [pandoc_cmd, "--from", "html", "--to", "gfm"],
                input=section_html,
                capture_output=True,
                text=True,
                check=True,
            )
            markdown_sections[key] = proc.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error processing section: {e}")

    for i, (key, section) in enumerate(markdown_sections.items()):
        glyph, codepoint = title_re.match(key).groups()
        try:
            int(codepoint, 16)
            glyph_id = "U+" + codepoint
        except ValueError:
            glyph_id = glyph

        (root / glyph_id).mkdir()
        (root / glyph_id / "index.md").write_text(
            "+++\n"
            + ("" if glyph_id.startswith("U+") else f'title = "{glyph}"\n')
            + f'radical = "{radical_i}"\n'
            + f"weight = {i}\n+++\n\n"
            + section
        )


# %%
for x in root.iterdir():
    for y in x.iterdir():
        y.unlink()
    x.rmdir()
