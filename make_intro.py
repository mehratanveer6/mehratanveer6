import os

CHAR_W = 7.74
FONT_SIZE = 12.9
LINE_H = 20.0

LOGIN = os.environ.get("GH_LOGIN", "user")

LINE1 = f"guest@github:~$ whoami"
LINE2 = f"{LOGIN} — building experiences"

LINES = [LINE1, LINE2]


def main():
    cols = max(len(l) for l in LINES)
    width = cols * CHAR_W + 20
    height = len(LINES) * LINE_H + 20

    parts = []
    parts.append(f'<svg viewBox="0 0 {width:.1f} {height:.1f}" xmlns="http://www.w3.org/2000/svg">')
    parts.append(f'<rect width="{width:.1f}" height="{height:.1f}" rx="6" fill="black"/>')
    parts.append(f'<style>text {{ font-family: monospace; font-size: {FONT_SIZE}px; fill: white; white-space: pre; }}</style>')

    delay_between_lines = 1.0
    for i, line in enumerate(LINES):
        y = 25 + i * LINE_H
        row_w = len(line) * CHAR_W
        clip_id = f'introclip{i}'
        begin = i * delay_between_lines
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'<rect x="10" y="{y-14:.1f}" width="0" height="{LINE_H:.1f}">')
        parts.append(f'<animate attributeName="width" from="0" to="{row_w:.1f}" dur="0.8s" begin="{begin:.2f}s" fill="freeze"/>')
        parts.append('</rect>')
        parts.append('</clipPath>')
        safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        parts.append(f'<text x="10" y="{y:.1f}" clip-path="url(#{clip_id})">{safe}</text>')

    total_dur = len(LINES) * delay_between_lines + 0.5
    last_y = 25 + (len(LINES) - 1) * LINE_H
    cursor_x = 10 + len(LINES[-1]) * CHAR_W
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="{last_y-14:.1f}" width="{CHAR_W:.1f}" height="{LINE_H:.1f}" fill="white" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;0" dur="1s" begin="{total_dur:.2f}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append('</svg>')

    with open('intro.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    print('wrote intro.svg')


if __name__ == '__main__':
    main()
