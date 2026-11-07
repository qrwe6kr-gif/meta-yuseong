"""UI용 픽셀아트 소품 (트로피, 스탬프 아이콘, 꽃가루) 생성 스크립트.

사용법: python scripts/draw_ui_props.py
"""
from pathlib import Path
from PIL import Image
from draw_zone_a_props import (Canvas, C, INK, INK2, STONE, SAND, CREAM, MILK,
                               LEAF, SPROUT, LIME, LAKE, RIPPLE, SKY, BARK, WOOD, STRAW, HAY, CORAL, APRICOT, BUTTER, BLOSSOM, LAVENDER)

# 저장 경로를 public/assets/sprites/ 로 명확히 지정
SPRITES_DIR = Path(__file__).resolve().parent.parent / 'public' / 'assets' / 'sprites'
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

def save_sprite(canvas, name):
    canvas.save_to(SPRITES_DIR / f'{name}.png')

# Canvas 클래스에 save_to 지원용 함수 추가 적용
def trophy():
    c = Canvas(32, 32)
    c.rect(8, 4, 16, 10, BUTTER)
    c.rect(10, 14, 12, 4, STRAW)
    c.rect(12, 18, 8, 3, WOOD)
    c.rect(5, 6, 3, 6, STRAW)
    c.rect(24, 6, 3, 6, STRAW)
    c.rect(6, 7, 1, 4, BUTTER)
    c.rect(25, 7, 1, 4, BUTTER)
    c.rect(9, 5, 2, 6, CREAM)
    c.rect(10, 5, 4, 2, CREAM)
    c.rect(13, 21, 6, 4, BARK)
    c.rect(9, 25, 14, 4, BARK)
    c.rect(7, 29, 18, 2, WOOD)
    c.hline(10, 26, 12, STRAW)
    c.im.save(SPRITES_DIR / 'trophy.png')

def stamp_on():
    c = Canvas(16, 16)
    for y in range(2, 14):
        for x in range(2, 14):
            if (x - 7.5)**2 + (y - 7.5)**2 <= 32:
                c.px(x, y, CORAL)
    c.px(4, 3, APRICOT); c.px(5, 2, APRICOT)
    check_pixels = [(4, 8), (5, 9), (6, 10), (7, 9), (8, 8), (9, 7), (10, 6), (11, 5)]
    for x, y in check_pixels:
        c.px(x, y, MILK)
        c.px(x, y + 1, MILK)
    c.im.save(SPRITES_DIR / 'stamp-on.png')

def stamp_off():
    c = Canvas(16, 16)
    dots = [(5, 2), (7, 2), (9, 2), (11, 3), (13, 5), (13, 7), (13, 9), (12, 11),
            (10, 13), (8, 13), (6, 13), (4, 12), (2, 10), (2, 8), (2, 6), (3, 4)]
    for x, y in dots:
        c.px(x, y, SAND)
    c.im.save(SPRITES_DIR / 'stamp-off.png')

def confetti():
    c = Canvas(48, 16)
    pieces = [
        (4, 3, 3, 3, CORAL), (10, 8, 2, 4, SKY), (16, 2, 4, 2, BUTTER),
        (22, 10, 3, 3, LIME), (28, 4, 2, 3, BLOSSOM), (34, 9, 4, 2, RIPPLE),
        (40, 3, 3, 3, SPROUT), (44, 11, 2, 2, APRICOT), (8, 12, 3, 2, LAVENDER)
    ]
    for x, y, w, h, col in pieces:
        c.rect(x, y, w, h, col)
    c.im.save(SPRITES_DIR / 'confetti.png')

if __name__ == '__main__':
    trophy()
    stamp_on()
    stamp_off()
    confetti()
    print("Successfully generated PNGs in public/assets/sprites/")