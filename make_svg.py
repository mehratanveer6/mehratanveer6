CHAR_W = 7.74
FONT_SIZE = 12.9
LINE_H = 15.0
BAR_H = 30.0

def main():
    with open('portrait.txt', 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    cols = max(len(l) for l in lines)
    rows = len(lines)

    width = cols * CHAR_W + 20
    body_h = rows * LINE_H + 20
    height = body_h + BAR_H

    svg_parts = []
    svg_parts.append(f'<svg viewBox="0 0 {width:.1f} {height:.1f}" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append(f'<rect width="{width:.1f}" height="{height:.1f}" rx="8" fill="black" stroke="#333333" stroke-width="1"/>')
    svg_parts.append(f'<rect width="{width:.1f}" height="{BAR_H:.1f}" rx="8" fill="#1a1a1a"/>')
    svg_parts.append(f'<rect y="{BAR_H/2:.1f}" width="{width:.1f}" height="{BAR_H/2:.1f}" fill="#1a1a1a"/>')
    svg_parts.append(f'<circle cx="20" cy="{BAR_H/2:.1f}" r="5" fill="#ff5f56"/>')
    svg_parts.append(f'<circle cx="38" cy="{BAR_H/2:.1f}" r="5" fill="#ffbd2e"/>')
    svg_parts.append(f'<circle cx="56" cy="{BAR_H/2:.1f}" r="5" fill="#27c93f"/>')
    svg_parts.append(f'<text x="{width/2:.1f}" y="{BAR_H/2+4:.1f}" font-family="monospace" font-size="11" fill="#888888" text-anchor="middle">portrait.sh</text>')
    svg_parts.append(f'<style>text.body {{ font-family: monospace; font-size: {FONT_SIZE}px; fill: white; white-space: pre; }}</style>')

    for i, line in enumerate(lines):
        y = 20 + i * LINE_H + BAR_H
        row_w = cols * CHAR_W
        clip_id = f'clip{i}'
        svg_parts.append(f'<clipPath id="{clip_id}">')
        svg_parts.append(f'<rect x="10" y="{y-12:.1f}" width="0" height="{LINE_H:.1f}">')
        svg_parts.append(f'<animate attributeName="width" from="0" to="{row_w:.1f}" dur="0.5s" begin="{i*0.09:.2f}s" fill="freeze"/>')
        svg_parts.append('</rect>')
        svg_parts.append('</clipPath>')
        safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg_parts.append(f'<text class="body" x="10" y="{y:.1f}" clip-path="url(#{clip_id})">{safe_line}</text>')

    total_dur = rows * 0.09 + 0.5
    last_y = 20 + (rows - 1) * LINE_H + BAR_H
    cursor_x = 10 + (max(len(l) for l in lines)) * CHAR_W
    svg_parts.append(
        f'<rect x="{cursor_x:.1f}" y="{last_y-12:.1f}" width="{CHAR_W:.1f}" height="{LINE_H:.1f}" fill="white" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;0" dur="1s" '
        f'begin="{total_dur:.2f}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    svg_parts.append('</svg>')

    svg = '\n'.join(svg_parts)
    with open('portrait.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote portrait.svg')

if __name__ == '__main__':
    main()
