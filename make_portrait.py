import io
import numpy as np
from PIL import Image
import cv2
from rembg import remove

RAMP = ' .`:-=+*cs#%@'
COLS = 90

def main():
    with open('photo.jpg', 'rb') as f:
        input_bytes = f.read()

    out_bytes = remove(input_bytes)
    img = Image.open(io.BytesIO(out_bytes)).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(bg, img).convert('RGB')

    arr = np.array(img)
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    bgr = cv2.bilateralFilter(bgr, d=9, sigmaColor=75, sigmaSpace=75)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    gray = (255 * (gray / 255.0) ** 1.7).astype(np.uint8)

    h, w = gray.shape
    cols = COLS
    rows = int(cols * (h / w) * 0.48)

    small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)

    n = len(RAMP) - 1
    lines = []
    for row in small:
        line = ''.join(RAMP[int(v / 255 * n)] for v in row)
        lines.append(line)

    text = '\n'.join(lines)
    with open('portrait.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print(text)

if __name__ == '__main__':
    main()
