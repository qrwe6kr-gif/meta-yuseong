import Phaser from 'phaser';
import { ZONES } from '../../data/zones.js';

// Loads every image and map once, then starts the first zone.
const SPRITES = [
  'player', 'tree', 'bush', 'bus-stop',
  'npc-halmae', 'npc-spa', 'npc-parkboy', 'npc-merchant',
  'res-grandpa', 'res-student', 'res-kid',
  // 구역 A 건물·소품 (scripts/draw_zone_a_props.py 로 그린 예시)
  'hotel-a', 'hotel-b', 'spa-gate', 'canopy', 'washstand', 'signboard',
  'pavilion', 'waterwheel', 'stall-red', 'stall-blue', 'stall-green',
  // 구역 B 건물·소품·NPC (scripts/draw_zone_b_props.py)
  'museum-geo', 'museum-money', 'museum-science', 'rocket', 'rock-garden', 'lamp', 'bridge-arch',
  'sign-geo', 'sign-money', 'sign-science', 'sign-bridge',
  'npc-geo', 'npc-mint', 'npc-robot', 'npc-photo', 'res-pupil', 'res-cyclist',
  // 구역 C 건물·소품·NPC (scripts/draw_zone_c_props.py)
  'restaurant-kam', 'restaurant-duck', 'persimmon-tree', 'waterfall-rocks', 'trail-sign', 'bench', 'sign-valley',
  'npc-valley', 'npc-kam', 'npc-duck', 'npc-trail', 'res-hiker', 'res-visitor',
];

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('boot');
  }

  preload() {
    this.load.setPath('assets/');
    this.load.image('pogeun-tiles', 'tiles/pogeun-tiles.png');
    SPRITES.forEach((key) => this.load.image(key, `sprites/${key}.png`));
    Object.values(ZONES).filter((z) => z.ready).forEach((z) => this.load.tilemapTiledJSON(z.map, `maps/${z.map}.json`));
  }

  create() {
    this.scene.start('world', { zone: 'A' });
  }
}