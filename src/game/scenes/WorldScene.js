import Phaser from 'phaser';
import { emit, on } from '../../bus.js';
import { ZONES } from '../../data/zones.js';

const SPEED = 72;          // world pixels per second
const TALK_RANGE = 22;     // how close (world px) the player must be to talk

// Reads a custom property that was set on an object in Tiled.
const prop = (obj, name) => (obj.properties || []).find((p) => p.name === name)?.value;

export default class WorldScene extends Phaser.Scene {
  constructor() {
    super('world');
  }

  init(data) {
    this.zoneKey = data.zone || 'A';
    this.from = data.from;     // 'bus' when the player arrived by bus
    this.uiOpen = false;
    this.nearId = null;
    this.onBusStop = true;      // ignore the stop until the player has stepped off it once
    this.touchDir = { x: 0, y: 0 };
  }

  create() {
    const zone = ZONES[this.zoneKey];
    const map = this.make.tilemap({ key: zone.map });
    const tiles = map.addTilesetImage('pogeun-tiles', 'pogeun-tiles');
    const ground = map.createLayer('ground', tiles, 0, 0);
    ground.setCollisionByProperty({ collides: true });   // 물·온천물 tiles are marked "collides" in Tiled

    this.obstacles = this.physics.add.staticGroup();
    this.talkers = [];
    const objects = map.getObjectLayer('objects').objects;
    let spawn = { x: map.widthInPixels / 2, y: map.heightInPixels / 2 };
    let arrive = null;

    for (const o of objects) {
      switch (o.type) {
        case 'spawn':
          spawn = { x: o.x, y: o.y };
          break;
        case 'arrive':     // where the player appears after taking the bus
          arrive = { x: o.x, y: o.y };
          break;
        case 'tree':
          this.addSolidImage('tree', o.x, o.y, 8, 5);
          break;
        case 'building': {
          const scale = prop(o, 'scale') ?? 1;
          this.addSolidImage(prop(o, 'sprite'), o.x, o.y, prop(o, 'footW') || 24, prop(o, 'footH') || 8, scale);
          break;
        }
        case 'decor': {
          const scale = prop(o, 'scale') ?? 1;
          this.add.image(o.x, o.y, prop(o, 'sprite')).setOrigin(0.5, 1).setScale(scale).setDepth(o.y);
          break;
        }
        case 'bush':
          this.addSolidImage('bush', o.x, o.y, 12, 6);
          break;
        case 'npc':
        case 'resident':
          this.addTalker(o);
          break;
        case 'bus':
          this.busZone = new Phaser.Geom.Rectangle(o.x, o.y, o.width, o.height);
          this.add.image(o.x + o.width - 4, o.y + 8, 'bus-stop').setOrigin(0.5, 1).setDepth(o.y + 8);
          this.keepInside(this.add.text(o.x + o.width / 2, o.y - 26, '버스 정류장', labelStyle('#e39b3f')).setOrigin(0.5, 1).setDepth(9000), map);
          break;
        case 'label':
          this.keepInside(this.add.text(o.x, o.y, prop(o, 'text') || o.name, labelStyle()).setOrigin(0.5, 1).setDepth(9000), map);
          break;
        default:
          break;
      }
    }

    const start = this.from === 'bus' && arrive ? arrive : spawn;
    this.player = this.physics.add.image(start.x, start.y, 'player').setOrigin(0.5, 1);
    this.player.body.setSize(10, 6).setOffset(3, 18);     // collide with the feet, not the head
    this.player.setCollideWorldBounds(true);
    this.physics.world.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
    this.physics.add.collider(this.player, ground);
    this.physics.add.collider(this.player, this.obstacles);

    const cam = this.cameras.main;
    cam.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
    cam.startFollow(this.player, true, 0.15, 0.15);
    this.fitZoom();
    this.scale.on('resize', this.fitZoom, this);

    this.keys = this.input.keyboard.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,SPACE,ENTER,E');
    ['keydown-SPACE', 'keydown-ENTER', 'keydown-E'].forEach((k) => this.input.keyboard.on(k, () => this.talk()));

    const offs = [
      on('ui:open', () => { this.uiOpen = true; this.player.setVelocity(0); }),
      on('ui:close', () => { this.uiOpen = false; }),
      on('input:talk', () => this.talk()),
      on('input:dir', (d) => { this.touchDir = d; }),
      on('zone:go', (key) => { if (key !== this.zoneKey && ZONES[key].ready) this.scene.restart({ zone: key, from: 'bus' }); }),
    ];
    this.events.once('shutdown', () => { offs.forEach((off) => off()); this.scale.off('resize', this.fitZoom, this); });

    emit('zone:ready', this.zoneKey);
  }

  // Nudges a centred label so it never hangs off the left/right edge of the map.
  keepInside(text, map) {
    const half = text.width / 2 + 2;
    text.x = Phaser.Math.Clamp(text.x, half, map.widthInPixels - half);
  }

  // A picture that stands on the map with a small solid footprint at its base.
  addSolidImage(key, x, y, w, h, scale = 1) {
    const img = this.add.image(x, y, key).setOrigin(0.5, 1).setScale(scale).setDepth(y);
    const block = this.add.zone(x, y - h / 2, w, h);
    this.obstacles.add(block);
  }

  addTalker(o) {
    const kind = o.type;   // 'npc' opens a place popup, 'resident' says one tip
    const sprite = this.add.image(o.x, o.y, prop(o, 'sprite') || 'player').setOrigin(0.5, 1).setDepth(o.y);
    this.tweens.add({ targets: sprite, scaleY: 1.04, duration: 800 + Math.random() * 300, yoyo: true, repeat: -1 });
    const name = this.add.text(o.x, o.y - 26, o.name, nameStyle(kind)).setOrigin(0.5, 1).setDepth(9500);
    const bubble = this.add.text(o.x + 9, o.y - 36, '…', bubbleStyle()).setOrigin(0.5, 1).setDepth(9600).setVisible(false);
    this.obstacles.add(this.add.zone(o.x, o.y - 3, 10, 6));
    sprite.setInteractive({ useHandCursor: true }).on('pointerdown', () => this.talk(o.id));
    this.talkers.push({ id: o.id, kind, x: o.x, y: o.y, name: o.name, bubble, name_text: name,
      placeId: prop(o, 'placeId'), greeting: prop(o, 'greeting'), line: prop(o, 'line'), sprite: prop(o, 'sprite') });
  }

  fitZoom() {
    const { width, height } = this.scale;
    // ?zoom=1 in the address bar shows the whole map (handy for checking a layout or taking a capture)
    const forced = Number(new URLSearchParams(window.location.search).get('zoom'));
    const zoom = forced || Phaser.Math.Clamp(Math.floor(Math.min(width / 320, height / 200)), 2, 4);
    this.cameras.main.setZoom(zoom);
  }

  talk(id = this.nearId) {
    if (this.uiOpen || id == null) return;
    const t = this.talkers.find((n) => n.id === id);
    if (!t) return;
    if (Phaser.Math.Distance.Between(this.player.x, this.player.y, t.x, t.y) > TALK_RANGE * 1.8) {
      emit('toast', `${t.name}에게 조금 더 가까이 가 주세요`);
      return;
    }
    if (t.kind === 'npc') emit('talk:npc', { placeId: t.placeId, name: t.name, greeting: t.greeting, sprite: t.sprite });
    else emit('talk:resident', { name: t.name, line: t.line, sprite: t.sprite });
  }

  update() {
    const k = this.keys;
    let vx = 0;
    let vy = 0;
    if (!this.uiOpen) {
      vx = (k.LEFT.isDown || k.A.isDown ? -1 : 0) + (k.RIGHT.isDown || k.D.isDown ? 1 : 0) + this.touchDir.x;
      vy = (k.UP.isDown || k.W.isDown ? -1 : 0) + (k.DOWN.isDown || k.S.isDown ? 1 : 0) + this.touchDir.y;
    }
    const len = Math.hypot(vx, vy) || 1;
    this.player.setVelocity((vx / len) * SPEED, (vy / len) * SPEED);
    if (vx) this.player.setFlipX(vx < 0);
    this.player.setDepth(this.player.y);

    // Who is close enough to talk to?
    let best = null;
    let bestD = TALK_RANGE;
    for (const t of this.talkers) {
      const d = Phaser.Math.Distance.Between(this.player.x, this.player.y, t.x, t.y);
      if (d < bestD) { best = t; bestD = d; }
    }
    const nearId = best ? best.id : null;
    this.talkers.forEach((t) => t.bubble.setVisible(t.id === nearId && !this.uiOpen));
    if (nearId !== this.nearId) {
      this.nearId = nearId;
      emit('near', best ? { name: best.name, kind: best.kind } : null);
    }

    // Bus stop: open the route picker when the player steps onto it.
    if (this.busZone) {
      const inside = this.busZone.contains(this.player.x, this.player.y);
      if (inside && !this.onBusStop && !this.uiOpen) emit('bus:open', this.zoneKey);
      this.onBusStop = inside;
    }
  }
}

const FONT = '"Galmuri11", sans-serif';
const labelStyle = (bg = '#f3e9d2') => ({ fontFamily: FONT, fontSize: '12px', color: '#3b2f3a', backgroundColor: bg, padding: { x: 4, y: 2 }, resolution: 4 });
const nameStyle = (kind) => ({ fontFamily: FONT, fontSize: '9px', color: kind === 'npc' ? '#fffbf2' : '#3b2f3a', backgroundColor: kind === 'npc' ? '#3b2f3acc' : '#f3e9d2cc', padding: { x: 2, y: 1 }, resolution: 4 });
const bubbleStyle = () => ({ fontFamily: FONT, fontSize: '12px', color: '#3b2f3a', backgroundColor: '#fffbf2', padding: { x: 3, y: 1 }, resolution: 4 });