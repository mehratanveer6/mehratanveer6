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
    line_len = w - 5 - line_start
    svg = f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<rect width="{w}" height="{h}" fill="black"/>
<text x="0" y="20" font-family="monospace" font-size="{FONT_SIZE}" fill="white" opacity="0">{label}
<animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0s" fill="freeze"/>
</text>
<line x1="{line_start:.1f}" y1="15" x2="{line_start:.1f}" y2="15" stroke="white" stroke-width="1">
<animate attributeName="x2" from="{line_start:.1f}" to="{w-5}" dur="0.8s" begin="0.3s" fill="freeze"/>
</line>
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
