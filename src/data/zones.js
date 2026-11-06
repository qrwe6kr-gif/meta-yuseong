// One entry per zone. A zone becomes playable once its Tiled map exists in public/assets/maps/.
// To add zone B: draw it in Tiled, save as public/assets/maps/zone-b.json, then set ready: true.
export const ZONES = {
  A: { key: 'A', title: '온천과 장터', area: '봉명동 · 장대동', map: 'zone-a', ready: true },
  B: { key: 'B', title: '과학로 박물관길', area: '가정동 · 구성동 · 도룡동', map: 'zone-b', ready: true },
  C: { key: 'C', title: '수통골 숲길', area: '덕명동 · 갑동', map: 'zone-c', ready: true },
};

export const ZONE_KEYS = ['A', 'B', 'C'];
