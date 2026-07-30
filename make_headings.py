HEADINGS = {
    "about": "about — building experiences",
    "stats": "stats",
    "projects": "projects",
    "contact": "contact",
}

CHAR_W = 6.5
FONT_SIZE = 14

def make_heading_svg(label):
    w = 500
    h = 30
    text_w = len(label) * CHAR_W
    line_start = text_w + 15
    svg = f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<rect width="{w}" height="{h}" fill="white"/>
<text x="0" y="20" font-family="monospace" font-size="{FONT_SIZE}" fill="black">{label}</text>
<line x1="{line_start:.1f}" y1="15" x2="{w-5}" y2="15" stroke="black" stroke-width="1"/>
</svg>'''
    return svg


def main():
    for key, label in HEADINGS.items():
        svg = make_heading_svg(label)
        fname = f'heading-{key}.svg'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f'wrote {fname}')


if __name__ == '__main__':
    main()
