"""콘텐츠랩 사진을 포근 26 팔레트 픽셀아트 간판으로 바꿉니다.

사용법:  python scripts/pixelate.py <사진 경로> <저장 경로> [가로] [세로]
예:      python scripts/pixelate.py public/photos/geo/geo_hq_06_type1.jpg public/assets/boards/geo.png 60 36

주의: 공공누리 제1유형 사진만 변환하세요. 제3·4유형은 변형 금지입니다.
필요 패키지: pip install pillow
"""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance

HEX = Path(__file__).resolve().parent.parent / 'public' / 'assets' / 'pogeun-26.hex'
PAL = [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in HEX.read_text().split()]
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def _luma_chroma(c):
    r, g, b = (v / 255 for v in c)
    return 0.299 * r + 0.587 * g + 0.114 * b, r - g, b - (r + g) / 2


_PL = [_luma_chroma(p) for p in PAL]


def nearest(c):
    l = _luma_chroma(c)
    return PAL[min(range(len(PAL)), key=lambda i: 3 * (l[0] - _PL[i][0]) ** 2 + (l[1] - _PL[i][1]) ** 2 + (l[2] - _PL[i][2]) ** 2)]


def pixelate(src, w=100, h=60, dither=10):
    im = Image.open(src).convert('RGB')
    iw, ih = im.size
    ratio = w / h
    sw, sh = (iw, iw / ratio) if iw / ratio <= ih else (ih * ratio, ih)
    im = im.crop(((iw - sw) / 2, (ih - sh) / 2, (iw + sw) / 2, (ih + sh) / 2))
    im = im.resize((w * 4, h * 4), Image.LANCZOS).resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(1.18)   # 포근 26은 밝은 색이 많아 살짝 밝게
    im = ImageEnhance.Color(im).enhance(1.35)        # 초록을 살리기 위해 채도 보정
    im = ImageEnhance.Contrast(im).enhance(1.05)
    out = Image.new('RGB', (w, h))
    for y in range(h):
        for x in range(w):
            o = (BAYER[(y % 4) * 4 + x % 4] / 16 - .5) * dither
            c = tuple(max(0, min(255, int(v + o))) for v in im.getpixel((x, y)))
            out.putpixel((x, y), nearest(c))
    return out


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    pixelate(sys.argv[1], w, h).save(sys.argv[2])
    print('저장:', sys.argv[2])
