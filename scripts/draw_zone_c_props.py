"""구역 C(수통골 숲길) 건물·소품·NPC를 포근 26 팔레트로 그립니다.

사용법: python scripts/draw_zone_c_props.py
"""
import math
from PIL import Image
from draw_zone_a_props import (Canvas, C, OUT, ROOT, INK, INK2, STONE, SAND, CREAM, MILK, FOREST, MOSS, LEAF,
                               SPROUT, LIME, LAKE, RIPPLE, SKY, BARK, WOOD, STRAW, HAY, CORAL, APRICOT, BUTTER,
                               BLOSSOM, LAVENDER, window)
from draw_zone_b_props import framed_sign, person


def restaurant_kam():
    """수통골 감나무집 본점: 주황 감나무가 옆에 있는 한옥풍 식당."""
    w, h = 96, 58
    c = Canvas(w, h)
    # 한옥 기와지붕
    for x in range(0, w):
        lift = 2 if x < 6 or x >= w - 6 else 0
        c.rect(x, 10 - lift, 1, 10, INK2)
    c.hline(2, 10, w - 4, STONE)
    c.rect(8, 4, w - 16, 6, INK2)
    # 기둥 및 벽면 (나무와 흙벽)
    c.rect(4, 20, w - 8, h - 21, CREAM)
    for x in range(6, w - 6, 16):
        c.rect(x, 20, 3, h - 24, BARK)
        c.vline(x, 20, h - 24, WOOD)
    # 대문 / 입구
    c.rect(w // 2 - 8, h - 18, 16, 17, WOOD)
    c.rect(w // 2 - 7, h - 17, 14, 16, STRAW)
    # 창문 (창살)
    window(c, 16, 26)
    window(c, w - 22, 26)
    c.rect(2, h - 3, w - 4, 3, STONE)
    c.save('restaurant-kam')


def restaurant_duck():
    """수통골장수오리: 모던하고 깔끔한 외관의 식당."""
    w, h = 88, 54
    c = Canvas(w, h)
    # 깔끔한 사각형 지붕선 및 간판부
    c.rect(2, 6, w - 4, 12, WOOD)
    c.rect(2, 6, w - 4, 2, STRAW)
    c.rect(w // 2 - 16, 9, 32, 6, MILK)
    c.rect(w // 2 - 14, 11, 28, 2, CORAL)  # 식당 로고 느낌의 포인트
    c.rect(0, 18, w, 2, INK2)
    # 밝은 톤의 벽과 통유리 창문
    c.rect(4, 20, w - 8, h - 21, MILK)
    c.rect(10, 26, 20, 16, SKY)
    c.rect(10, 26, 20, 2, RIPPLE)
    c.rect(w - 30, 26, 20, 16, SKY)
    c.rect(w - 30, 26, 20, 2, RIPPLE)
    # 유리 자동문
    c.rect(w // 2 - 7, h - 18, 14, 17, LAKE)
    c.rect(w // 2 - 6, h - 17, 12, 16, SKY)
    c.vline(w // 2, h - 17, 16, INK2)
    c.rect(2, h - 3, w - 4, 3, STONE)
    c.save('restaurant-duck')


def persimmon_tree():
    """주황색 감이 맺힌 감나무."""
    w, h = 32, 36
    c = Canvas(w, h)
    # 나무 줄기
    c.rect(13, 18, 6, 18, BARK)
    c.vline(13, 18, 18, WOOD)
    # 풍성한 잎사귀 (포근 26 초록 계열)
    for x, y, r in [(16, 12, 11), (9, 14, 8), (23, 14, 8), (16, 7, 7)]:
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    c.px(x + dx, y + dy, FOREST if dy > 2 else (MOSS if dy > -3 else LEAF))
    # 주황색 감 열매
    persimmons = [(10, 10), (20, 9), (14, 15), (24, 16), (8, 16), (17, 6), (12, 18)]
    for px, py in persimmons:
        c.rect(px, py, 2, 2, APRICOT)
        c.px(px, py, CORAL)
    c.save('persimmon-tree')


def waterfall_rocks():
    """계곡 바위와 작은 폭포 물줄기."""
    w, h = 48, 32
    c = Canvas(w, h)
    # 암석들
    rocks = [(2, 8, 18, 16, INK2), (28, 6, 18, 18, STONE), (16, 18, 16, 12, SAND)]
    for x, y, rw, rh, col in rocks:
        for j in range(rh):
            inset = abs(j - rh // 2) // 2
            c.rect(x + inset, y + j, rw - inset * 2, 1, col)
    # 폭포 물줄기 및 물보라
    c.rect(20, 0, 8, 20, RIPPLE)
    c.rect(22, 0, 4, 20, SKY)
    for y in range(0, 20, 3):
        c.hline(21, y, 6, MILK)
    c.rect(16, 18, 16, 4, MILK)
    c.save('waterfall-rocks')


def trail_sign():
    """보훈둘레길 정돈된 안내판 (차분한 디자인)."""
    c = Canvas(20, 26)
    c.rect(8, 12, 4, 14, BARK)
    c.rect(2, 2, 16, 12, WOOD)
    c.rect(3, 3, 14, 10, STRAW)
    # 정돈된 안내선
    c.hline(5, 5, 10, BARK)
    c.hline(5, 8, 10, BARK)
    c.hline(5, 11, 6, BARK)
    c.save('trail-sign')


def bench():
    """나무 벤치."""
    c = Canvas(24, 14)
    c.rect(2, 4, 20, 3, WOOD)
    c.hline(2, 4, 20, STRAW)
    c.rect(2, 8, 20, 3, WOOD)
    c.hline(2, 8, 20, STRAW)
    c.rect(4, 10, 2, 4, INK2)
    c.rect(18, 10, 2, 4, INK2)
    c.save('bench')


if __name__ == '__main__':
    restaurant_kam()
    restaurant_duck()
    persimmon_tree()
    waterfall_rocks()
    trail_sign()
    bench()
    framed_sign('valley', 'sign-valley')
    
    # NPC (valley, kam, duck, trail)
    person('npc-valley', MOSS, FOREST, BARK, WOOD)
    person('npc-kam', APRICOT, CORAL, INK, INK2)
    person('npc-duck', SKY, LAKE, BARK, WOOD)
    person('npc-trail', STONE, INK2, INK, INK2)
    
    # 주민 (res-hiker, res-visitor)
    person('res-hiker', CORAL, INK2, BARK, WOOD)
    person('res-visitor', LEAF, MOSS, INK2, STONE)