"""UI용 픽셀아트 소품 (트로피, 스탬프 아이콘, 꽃가루) 생성 스크립트.

사용법: python scripts/draw_ui_props.py
"""
from PIL import Image
from draw_zone_a_props import (Canvas, C, OUT, INK, INK2, STONE, SAND, CREAM, MILK,
                               LEAF, SPROUT, LIME, LAKE, RIPPLE, SKY, BARK, WOOD, STRAW, HAY, CORAL, APRICOT, BUTTER)

def trophy():
    """32x32 금색 픽셀 트로피."""
    c = Canvas(32, 32)
    # 컵 몸체 (금색)
    c.rect(8, 4, 16, 10, BUTTER)
    c.rect(10, 14, 12, 4, STRAW)
    c.rect(12, 18, 8, 3, WOOD)
    # 컵 손잡이 (양옆)
    c.rect(5, 6, 3, 6, STRAW)
    c.rect(24, 6, 3, 6, STRAW)
    c.rect(6, 7, 1, 4, BUTTER)
    c.rect(25, 7, 1, 4, BUTTER)
    # 광택 하이라이트 (왼쪽 위)
    c.rect(9, 5, 2, 6, CREAM)
    c.rect(10, 5, 4, 2, CREAM)
    # 받침대
    c.rect(13, 21, 6, 4, BARK)
    c.rect(9, 25, 14, 4, BARK)
    c.rect(7, 29, 18, 2, WOOD)
    c.hline(10, 26, 12, STRAW)
    c.save('trophy')

def stamp_on():
    """16x16 찍힌 스탬프 도장 (CORAL 원 안의 MILK 체크)."""
    c = Canvas(16, 16)
    # CORAL 원형 바탕
    for y in range(2, 14):
        for x in range(2, 14):
            if (x - 7.5)**2 + (y - 7.5)**2 <= 32:
                c.px(x, y, CORAL)
    # 원 테두리 음영 (APRICOT / INK)
    c.px(4, 3, APRICOT); c.px(5, 2, APRICOT)
    # MILK 색상 체크 표시
    check_pixels = [(4, 8), (5, 9), (6, 10), (7, 9), (8, 8), (9, 7), (10, 6), (11, 5)]
    for x, y in check_pixels:
        c.px(x, y, MILK)
        c.px(x, y + 1, MILK)
    c.save('stamp-on')

def stamp_off():
    """16x16 빈 스탬프 칸 (SAND 점선 원)."""
    c = Canvas(16, 16)
    # 점선 테두리
    dots = [(5, 2), (7, 2), (9, 2), (11, 3), (13, 5), (13, 7), (13, 9), (12, 11),
            (10, 13), (8, 13), (6, 13), (4, 12), (2, 10), (2, 8), (2, 6), (3, 4)]
    for x, y in dots:
        c.px(x, y, SAND)
    c.save('stamp-off')

def confetti():
    """48x16 포근 26 색상의 작은 픽셀 꽃가루 조각들."""
    c = Canvas(48, 16)
    pieces = [
        (4, 3, 3, 3, CORAL), (10, 8, 2, 4, SKY), (16, 2, 4, 2, BUTTER),
        (22, 10, 3, 3, LIME), (28, 4, 2, 3, BLOSSOM), (34, 9, 4, 2, RIPPLE),
        (40, 3, 3, 3, SPROUT), (44, 11, 2, 2, APRICOT), (8, 12, 3, 2, LAVENDER)
    ]
    for x, y, w, h, col in pieces:
        c.rect(x, y, w, h, col)
    c.save('confetti')

if __name__ == '__main__':
    trophy()
    stamp_on()
    stamp_off()
    confetti()