import base64

def main():
    with open('ramp.woff2', 'rb') as f:
        font_bytes = f.read()
    b64 = base64.b64encode(font_bytes).decode('ascii')

    with open('portrait.svg', 'r', encoding='utf-8') as f:
        svg = f.read()

    font_face = (
        '<style>'
        '@font-face{'
        "font-family:'ramp';"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');"
        '}'
        'text{font-family:ramp;}'
        '</style>'
    )

    # insert right after the opening <svg ...> tag
    idx = svg.index('>') + 1
    svg = svg[:idx] + font_face + svg[idx:]

    with open('portrait.svg', 'w', encoding='utf-8') as f:
        f.write(svg)

    print('embedded font into portrait.svg')

if __name__ == '__main__':
    main()
