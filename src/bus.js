// A tiny event bus so the Phaser game and the React UI can talk without knowing about each other.
// Game → UI:  'zone:ready', 'near', 'talk:npc', 'talk:resident', 'bus:open', 'toast'
// UI → Game:  'ui:open', 'ui:close', 'input:talk', 'zone:go', 'input:dir'
const target = new EventTarget();

export function emit(type, detail) {
  target.dispatchEvent(new CustomEvent(type, { detail }));
}

export function on(type, handler) {
  const listener = (e) => handler(e.detail);
  target.addEventListener(type, listener);
  return () => target.removeEventListener(type, listener);
}
