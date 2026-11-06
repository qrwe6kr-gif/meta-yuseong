import Phaser from 'phaser';
import BootScene from './scenes/BootScene.js';
import WorldScene from './scenes/WorldScene.js';

export function createGame(parent) {
  return new Phaser.Game({
    type: Phaser.AUTO,
    parent,
    backgroundColor: '#2f5d46',
    pixelArt: true,                       // keep 16px art sharp when zoomed
    scale: { mode: Phaser.Scale.RESIZE, width: '100%', height: '100%' },
    physics: { default: 'arcade', arcade: { debug: false } },
    scene: [BootScene, WorldScene],
  });
}
