"""구역 A 건물·소품을 포근 26 팔레트로 그립니다. (참고용 예시 그림 — 직접 그린 그림으로 덮어써도 됩니다)

사용법: python scripts/draw_zone_a_props.py
결과:   public/assets/sprites/ 에 hotel-a.png, hotel-b.png, spa-gate.png, canopy.png, washstand.png,
        signboard.png, pavilion.png, waterwheel.png, stall-red.png, stall-blue.png, stall-green.png 저장
"""
from pathlib import Path
import math
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public' / 'assets' / 'sprites'
HEX = (ROOT / 'public' / 'assets' / 'pogeun-26.hex').read_text().split()
C = {h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for h in HEX}

INK, INK2, STONE, SAND, CREAM, MILK = '3b2f3a', '5a4a4f', '8a7a72', 'c9bba8', 'f3e9d2', 'fffbf2'
FOREST, MOSS, LEAF, SPROUT, LIME, SPA = '2f5d46', '3f7d4e', '5fa35a', '8cc864', 'c4e08a', '3f8f8a'
LAKE, RIPPLE, SKY = '4f86b8', '7fb8d8', 'c8e6ef'
BARK, WOOD, STRAW, HAY = '6b4632', '9a6a45', 'c9955c', 'e8c48a'
CORAL, APRICOT, BUTTER, BLOSSOM, LAVENDER = 'e8826a', 'f2b37a', 'f6dd7a', 'f2a6b4', 'b07ac0'


class Canvas:
    def __init__(self, w, h):
        self.im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    def px(self, x, y, c):
        if 0 <= x < self.im.width and 0 <= y < self.im.height:
            self.im.putpixel((int(x), int(y)), C[c])

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.px(x + i, y + j, c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def save(self, name, outline=True):
        im = self.im
        if outline:
            out = im.copy()
            W, H = im.size
            for y in range(H):
                for x in range(W):
                    if im.getpixel((x, y))[3] == 0 and any(
                            0 <= x + dx < W and 0 <= y + dy < H and im.getpixel((x + dx, y + dy))[3]
                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        out.putpixel((x, y), C[INK])
            im = out
        im.save(OUT / f'{name}.png')
        print('saved', name, im.size)


def window(c, x, y):
    c.rect(x, y, 6, 7, INK2)
    c.rect(x + 1, y + 1, 4, 5, LAKE)
    c.rect(x + 1, y + 1, 2, 2, SKY)
    c.vline(x + 3, y + 1, 5, INK2)


def steam_mark(c, x, y):
    """온천 표시(♨): 그릇과 김 세 줄."""
    c.rect(x, y + 6, 9, 2, CORAL)
    c.rect(x + 1, y + 8, 7, 1, CORAL)
    for i in (1, 4, 7):
        c.px(x + i, y + 4, CORAL); c.px(x + i + 1, y + 3, CORAL); c.px(x + i, y + 2, CORAL); c.px(x + i + 1, y + 1, CORAL)


def hotel(name, w, h, roof, roof_light, floors):
    c = Canvas(w, h)
    roof_h = 14
    # roof with eaves
    c.rect(1, 2, w - 2, roof_h, roof)
    c.rect(1, 2, w - 2, 2, roof_light)
    for y in range(6, roof_h + 2, 4):
        c.hline(1, y, w - 2, roof_light if y % 8 else roof)
    c.rect(0, roof_h, w, 2, INK2)
    # walls
    wall_top = roof_h + 2
    c.rect(2, wall_top, w - 4, h - wall_top - 1, CREAM)
    c.rect(2, h - 4, w - 4, 3, SAND)
    for f in range(floors):
        y = wall_top + 3 + f * 10
        for x in range(5, w - 9, 9):
            window(c, x, y)
    # sign with steam mark and door
    sx = w // 2 - 7
    c.rect(sx, wall_top + 2 + floors * 10 - 1, 14, 11, MILK)
    steam_mark(c, sx + 2, wall_top + 2 + floors * 10)
    c.rect(w // 2 - 4, h - 11, 8, 10, WOOD)
    c.rect(w // 2 - 3, h - 10, 6, 9, STRAW)
    c.px(w // 2 + 1, h - 6, BUTTER)
    # chimney steam
    for i, x in enumerate((w - 12, w - 9)):
        c.rect(x, 0, 2, 4, MILK) if i == 0 else c.rect(x, 1, 2, 3, MILK)
    c.save(name)


def spa_gate():
    """유성온천 입구 아치 (사진 속 파란 아치를 단순화)."""
    w, h = 80, 44
    c = Canvas(w, h)
    for x0 in (4, w - 10):
        c.rect(x0, 14, 6, h - 14, SAND)
        c.vline(x0, 14, h - 14, MILK)
        c.rect(x0 - 1, h - 4, 8, 4, STONE)
    for x in range(2, w - 2):
        t = (x - w / 2) / (w / 2 - 2)
        top = int(4 + 8 * t * t)
        c.rect(x, top, 1, 10, LAKE)
        c.px(x, top, SKY)
        if x % 6 == 0:
            c.rect(x, top + 3, 2, 3, MILK)
    c.rect(w // 2 - 14, 6, 28, 8, MILK)
    for x in range(w // 2 - 12, w // 2 + 12, 4):
        c.rect(x, 9, 2, 2, LAKE)
    c.save('spa-gate')


def canopy():
    """족욕장 흰 그늘막 (막구조 지붕 + 기둥 4개)."""
    w, h = 48, 36
    c = Canvas(w, h)
    for x in (4, w - 6):
        c.rect(x, 14, 2, h - 14, STONE)
    for x in (14, w - 16):
        c.rect(x, 16, 2, h - 18, SAND)
    for x in range(1, w - 1):
        t = abs(x - w / 2) / (w / 2)
        top = int(3 + 6 * (1 - t))
        c.rect(x, top, 1, 10 - int(4 * (1 - t)), MILK if (x // 6) % 2 else CREAM)
        c.px(x, top + 9 - int(4 * (1 - t)), SAND)
    c.rect(w // 2 - 1, 0, 2, 5, STONE)
    c.save('canopy')


def washstand():
    """발 씻는 곳: 돌 세면대와 수도꼭지."""
    c = Canvas(16, 22)
    c.rect(2, 10, 12, 10, STONE)
    c.rect(2, 10, 12, 2, SAND)
    c.rect(4, 12, 8, 3, RIPPLE)
    c.rect(7, 2, 2, 9, INK2)
    c.rect(7, 2, 5, 2, INK2)
    c.px(11, 4, RIPPLE)
    c.save('washstand')


def signboard():
    """나무 안내판."""
    c = Canvas(18, 24)
    c.rect(7, 12, 2, 12, BARK)
    c.rect(1, 2, 16, 12, WOOD)
    c.rect(2, 3, 14, 10, HAY)
    for y in (5, 8, 11):
        c.hline(4, y, 10 if y != 11 else 6, BARK)
    c.save('signboard')


def pavilion():
    """유림공원 정자: 기와지붕과 붉은 기둥."""
    w, h = 48, 46
    c = Canvas(w, h)
    for x in range(0, w):
        lift = 3 if x < 4 or x >= w - 4 else 0
        c.rect(x, 8 - lift, 1, 12, INK2)
    for y in range(9, 19, 3):
        c.hline(3, y, w - 6, STONE)
    c.rect(10, 2, w - 20, 7, INK2)
    c.hline(10, 2, w - 20, STONE)
    c.rect(4, 20, w - 8, 2, CORAL)
    for x in (6, w // 2 - 1, w - 8):
        c.rect(x, 22, 3, 16, CORAL)
        c.vline(x, 22, 16, APRICOT)
    c.rect(2, 38, w - 4, 4, WOOD)
    c.hline(2, 38, w - 4, STRAW)
    c.rect(4, 42, w - 8, 3, BARK)
    c.save('pavilion')


def waterwheel():
    """반도지 물레방아."""
    c = Canvas(28, 32)
    cx, cy, r = 13, 14, 11
    for a in range(0, 360, 3):
        x = cx + r * math.cos(math.radians(a)); y = cy + r * math.sin(math.radians(a))
        c.px(round(x), round(y), WOOD)
    for a in range(0, 360, 45):
        for k in range(0, r):
            c.px(round(cx + k * math.cos(math.radians(a))), round(cy + k * math.sin(math.radians(a))), STRAW)
        bx = round(cx + r * math.cos(math.radians(a))); by = round(cy + r * math.sin(math.radians(a)))
        c.rect(bx - 1, by - 1, 3, 3, BARK)
    c.rect(cx - 1, cy - 1, 3, 3, BARK)
    c.rect(24, 6, 3, 26, BARK)
    c.rect(22, 4, 6, 3, WOOD)
    c.save('waterwheel')


def stall(name, a, b):
    """장터 좌판 천막: 줄무늬 지붕과 채소·과일 상자."""
    w, h = 32, 30
    c = Canvas(w, h)
    for x in range(0, w):
        col = a if (x // 4) % 2 else b
        c.rect(x, 2, 1, 9, col)
        if x % 4 == 2:
            c.px(x, 11, col)
    c.hline(0, 2, w, MILK)
    for x in (2, w - 4):
        c.rect(x, 11, 2, 12, STONE)
    goods = [CORAL, BUTTER, SPROUT, LAVENDER, APRICOT, LEAF]
    for i, x in enumerate(range(3, w - 6, 9)):
        c.rect(x, 20, 8, 7, WOOD)
        c.hline(x, 20, 8, STRAW)
        for j in range(3):
            c.rect(x + 1 + j * 2 + (i % 2), 17 + (j % 2), 2, 3, goods[(i + j) % len(goods)])
    c.rect(1, 27, w - 2, 2, HAY)
    c.save(name)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    hotel('hotel-a', 64, 62, LAVENDER, BLOSSOM, 3)
    hotel('hotel-b', 48, 52, SPA, LAKE, 2)
    spa_gate()
    canopy()
    washstand()
    signboard()
    pavilion()
    waterwheel()
    stall('stall-red', CORAL, MILK)
    stall('stall-blue', LAKE, MILK)
    stall('stall-green', LEAF, BUTTER)
