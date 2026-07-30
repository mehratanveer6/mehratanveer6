CHAR_W = 7.74
FONT_SIZE = 12.9
BAR_H = 30.0

EMAIL_LINE = "email: tanveermehracs@gmail.com"


def main():
    width = len(EMAIL_LINE) * CHAR_W + 20
    body_h = 80.0
    height = body_h + BAR_H

    parts = []
    parts.append(f'<svg viewBox="0 0 {width:.1f} {height:.1f}" xmlns="http://www.w3.org/2000/svg">')
    parts.append(f'<rect width="{width:.1f}" height="{height:.1f}" rx="8" fill="black" stroke="#333333" stroke-width="1"/>')
    parts.append(f'<rect width="{width:.1f}" height="{BAR_H:.1f}" rx="8" fill="#1a1a1a"/>')
    parts.append(f'<rect y="{BAR_H/2:.1f}" width="{width:.1f}" height="{BAR_H/2:.1f}" fill="#1a1a1a"/>')
    parts.append(f'<circle cx="20" cy="{BAR_H/2:.1f}" r="5" fill="#ff5f56"/>')
    parts.append(f'<circle cx="38" cy="{BAR_H/2:.1f}" r="5" fill="#ffbd2e"/>')
    parts.append(f'<circle cx="56" cy="{BAR_H/2:.1f}" r="5" fill="#27c93f"/>')
    parts.append(f'<text x="{width/2:.1f}" y="{BAR_H/2+4:.1f}" font-family="monospace" font-size="11" fill="#888888" text-anchor="middle">contact.sh</text>')
    parts.append(f'<style>text.body {{ font-family: monospace; font-size: {FONT_SIZE}px; fill: white; white-space: pre; }}</style>')

    y = BAR_H + 30
    row_w = len(EMAIL_LINE) * CHAR_W
    parts.append('<clipPath id="emailclip">')
    parts.append(f'<rect x="10" y="{y-14:.1f}" width="0" height="20">')
    parts.append(f'<animate attributeName="width" from="0" to="{row_w:.1f}" dur="0.8s" begin="0s" fill="freeze"/>')
    parts.append('</rect>')
    parts.append('</clipPath>')
    parts.append(f'<text class="body" x="10" y="{y:.1f}" clip-path="url(#emailclip)">{EMAIL_LINE}</text>')

    dot_y = y + 28
    for i in range(3):
        cx = 10 + i * 16
        parts.append(
            f'<circle cx="{cx}" cy="{dot_y:.1f}" r="4" fill="#a855f7" opacity="0.3">'
            f'<animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" '
            f'begin="{1.0 + i*0.2:.2f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    parts.append('</svg>')

    with open('contact.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    print('wrote contact.svg')


if __name__ == '__main__':
    main()
