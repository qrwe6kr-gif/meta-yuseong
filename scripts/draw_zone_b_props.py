"""구역 B(과학로 박물관길) 건물·소품·NPC를 포근 26 팔레트로 그립니다. (참고용 예시 그림 — 직접 그린 그림으로 덮어써도 됩니다)

사용법: python scripts/draw_zone_b_props.py
먼저 픽셀 간판(public/assets/boards/*.png)이 있어야 액자 간판(sign-*.png)이 만들어집니다.
"""
import math
from PIL import Image
from draw_zone_a_props import (Canvas, C, OUT, ROOT, INK, INK2, STONE, SAND, CREAM, MILK, FOREST, MOSS, LEAF,
                               SPROUT, LIME, LAKE, RIPPLE, SKY, BARK, WOOD, STRAW, HAY, CORAL, APRICOT, BUTTER,
                               BLOSSOM, LAVENDER, window)


def museum_geo():
    """지질박물관: 스테고사우루스 골판을 닮은 지붕."""
    w, h = 112, 66
    c = Canvas(w, h)
    c.rect(2, 22, w - 4, 10, INK2)                      # dark roof band
    c.hline(2, 22, w - 4, STONE)
    for i in range(9):                                  # plates along the ridge
        px = 10 + i * 11.5
        ph = 10 + (8 if i % 2 == 0 else 2) + (4 if i in (3, 4, 5) else 0)
        for k in range(ph):
            hw = max(1, round((ph - k) * 0.42))
            col = APRICOT if k > ph - 4 else CORAL
            c.rect(round(px - hw), 22 - k, hw * 2, 1, col)
    c.rect(4, 32, w - 8, h - 33, SAND)                  # stone walls
    c.rect(4, 32, w - 8, 2, CREAM)
    for x in range(8, w - 12, 12):
        if abs(x - w // 2) > 10:
            window(c, x, 38)
    c.rect(w // 2 - 7, h - 16, 14, 15, INK2)            # glass entrance
    c.rect(w // 2 - 6, h - 15, 12, 14, LAKE)
    c.rect(w // 2 - 6, h - 15, 4, 4, SKY)
    c.rect(2, h - 3, w - 4, 3, STONE)
    c.save('museum-geo')


def museum_money():
    """화폐박물관: 초록 지붕과 큰 금화 문양."""
    w, h = 96, 62
    c = Canvas(w, h)
    c.rect(2, 8, w - 4, 16, MOSS)
    for y in range(11, 24, 4):
        c.hline(2, y, w - 4, FOREST)
    c.hline(2, 8, w - 4, LEAF)
    cx, cy, r = w // 2, 16, 9                            # gold coin
    for y in range(-r, r + 1):
        hw = round(math.sqrt(r * r - y * y))
        c.rect(cx - hw, cy + y, hw * 2, 1, BUTTER if abs(y) < r - 2 else STRAW)
    c.rect(cx - 2, cy - 2, 4, 4, MOSS)
    c.rect(0, 24, w, 3, INK2)
    c.rect(4, 27, w - 8, h - 28, CREAM)
    for x in range(8, w - 8, 14):                       # columns
        c.rect(x, 27, 4, h - 31, MILK)
        c.vline(x + 3, 27, h - 31, SAND)
    c.rect(w // 2 - 6, h - 15, 12, 14, WOOD)
    c.rect(w // 2 - 5, h - 14, 10, 13, STRAW)
    c.rect(2, h - 4, w - 4, 4, SAND)
    c.save('museum-money')


def museum_science():
    """국립중앙과학관: 흰 건물과 가운데 큰 유리 아치."""
    w, h = 144, 74
    c = Canvas(w, h)
    for x0 in (4, w - 44):                              # two white wings
        c.rect(x0, 18, 40, h - 19, MILK)
        c.rect(x0, 18, 40, 3, SAND)
        for y in range(26, h - 10, 10):
            c.hline(x0 + 2, y, 36, SKY)
            c.hline(x0 + 2, y + 1, 36, RIPPLE)
    cx, base, r = w // 2, h - 2, 34                     # glass arch
    for y in range(base - r, base):
        hw = round(math.sqrt(max(0, r * r - (base - y) ** 2)))
        c.rect(cx - hw, y, hw * 2, 1, SKY if (y // 4) % 2 else RIPPLE)
    for a in range(0, 181, 15):                         # arch ribs
        for k in range(r):
            c.px(round(cx - k * math.cos(math.radians(a))), round(base - k * math.sin(math.radians(a))), STONE)
    for a in range(0, 181, 2):
        c.px(round(cx - r * math.cos(math.radians(a))), round(base - r * math.sin(math.radians(a))), INK2)
    c.rect(cx - 6, h - 12, 12, 11, LAKE)
    c.rect(2, h - 2, w - 4, 2, SAND)
    c.save('museum-science')


def rocket():
    c = Canvas(16, 52)
    for y in range(6, 44):
        hw = 3 if y > 10 else max(1, (y - 4) // 2)
        c.rect(8 - hw, y, hw * 2, 1, MILK)
        c.px(8 + hw - 1, y, SAND)
    c.rect(7, 2, 2, 5, CORAL)
    c.rect(5, 20, 6, 2, LAKE)
    for side in (-1, 1):
        for k in range(6):
            c.rect(8 + side * (3 + k // 2) - (1 if side < 0 else 0), 36 + k, 1, 8 - k, CORAL)
    c.rect(4, 44, 8, 6, STONE)
    c.rect(2, 49, 12, 3, SAND)
    c.save('rocket')


def rock_garden():
    c = Canvas(56, 26)
    rocks = [(4, 10, 14, 12, STONE), (20, 4, 16, 18, INK2), (38, 12, 14, 10, SAND), (14, 16, 10, 8, SAND)]
    for x, y, w, h, col in rocks:
        for j in range(h):
            inset = abs(j - h // 2) // 2
            c.rect(x + inset, y + j, w - inset * 2, 1, col)
        c.rect(x + 3, y + 2, 3, 2, CREAM)
    c.rect(0, 22, 56, 4, HAY)
    c.save('rock-garden')


def lamp():
    c = Canvas(10, 34)
    c.rect(4, 8, 2, 24, INK2)
    c.rect(1, 2, 8, 6, BUTTER)
    c.rect(1, 2, 8, 2, INK2)
    c.rect(2, 31, 6, 3, STONE)
    c.save('lamp')


def bridge_arch():
    """엑스포다리: 빨강·파랑 두 아치와 케이블. 다리 바닥 타일 위에 겹쳐 놓습니다."""
    w, h = 96, 104
    c = Canvas(w, h)
    for col, cx, lean in ((LAKE, 52, 1), (CORAL, 44, -1)):
        for t in range(0, 181):
            a = math.radians(t)
            x = cx + 38 * math.cos(a)
            y = h - 8 - 88 * math.sin(a)
            c.rect(round(x) + (lean if t > 90 else 0), round(y), 4, 3, col)
    for i in range(1, 9):                               # cables
        x = 12 + i * 9
        top = h - 8 - 88 * math.sin(math.acos(max(-1, min(1, (x - 48) / 40))))
        for y in range(int(top) + 3, h - 6, 2):
            c.px(x, y, SAND)
    c.rect(0, h - 6, w, 2, MILK)
    c.rect(0, h - 4, w, 4, STONE)
    c.save('bridge-arch', outline=False)


def framed_sign(board_name, out_name):
    """제1유형 사진 픽셀 간판을 동적 크기 나무 액자와 다리에 끼웁니다."""
    src = ROOT / 'public' / 'assets' / 'boards' / f'{board_name}.png'
    if not src.exists():
        print('skip', out_name, '(no board)')
        return
    board = Image.open(src).convert('RGBA')
    bw, bh = board.size
    cw, ch = bw + 8, bh + 22
    c = Canvas(cw, ch)
    c.rect(0, 0, cw, bh + 6, BARK)
    c.rect(1, 1, cw - 2, bh + 4, CREAM)
    c.im.paste(board, (4, 3))
    for x in (12, cw - 14):
        c.rect(x, bh + 6, 3, 16, WOOD)
        c.vline(x, bh + 6, 16, STRAW)
    c.save(out_name)


def person(name, shirt, shirt_dark, hair=None, hair_light=None):
    base = Image.open(OUT / 'player.png').convert('RGBA')
    G1, G2 = C['5fa35a'][:3], C['3f7d4e'][:3]
    H1, H2 = C['6b4632'][:3], C['9a6a45'][:3]
    mp = {G1: C[shirt][:3], G2: C[shirt_dark][:3]}
    if hair:
        mp.update({H1: C[hair][:3], H2: C[hair_light][:3]})
    px = base.load()
    for y in range(base.height):
        for x in range(base.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in mp:
                px[x, y] = mp[(r, g, b)] + (255,)
    base.save(OUT / f'{name}.png')
    print('saved', name)


def robot():
    """큐레이터 로봇 사이언 (16×24)."""
    c = Canvas(16, 24)
    c.vline(8, 1, 3, INK2); c.px(8, 0, BUTTER)
    c.rect(3, 4, 10, 8, MILK)
    c.rect(4, 6, 8, 4, INK2)
    c.px(6, 7, SKY); c.px(10, 7, SKY)
    c.rect(4, 13, 8, 7, SAND)
    c.rect(4, 13, 8, 1, MILK)
    c.rect(6, 15, 4, 3, LAKE)
    c.rect(2, 14, 2, 5, STONE); c.rect(12, 14, 2, 5, STONE)
    c.rect(5, 20, 2, 3, STONE); c.rect(9, 20, 2, 3, STONE)
    c.save('npc-robot')


if __name__ == '__main__':
    museum_geo()
    museum_money()
    museum_science()
    rocket()
    rock_garden()
    lamp()
    bridge_arch()
    for b in ('geo', 'money', 'science', 'bridge'):
        framed_sign(b, f'sign-{b}')
    person('npc-geo', STRAW, WOOD, BARK, WOOD)
    person('npc-mint', BUTTER, STRAW, INK, INK2)
    person('npc-photo', LAVENDER, INK2, INK2, STONE)
    person('res-pupil', LAKE, INK2, INK, INK2)
    person('res-cyclist', CORAL, INK2, INK, INK2)
    robot()
