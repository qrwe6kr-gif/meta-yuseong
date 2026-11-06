import React, { useCallback, useEffect, useRef, useState } from 'react';
import { PlaceSheet, ResidentSheet, BusSheet, StampCompleteSheet } from './ui/Sheets.jsx';
import { createGame } from './game/createGame.js';
import { emit, on } from './bus.js';
import { ZONES } from './data/zones.js';

const STORE_KEY = 'meta-yuseong-stamps';
const loadStamps = () => { try { return new Set(JSON.parse(localStorage.getItem(STORE_KEY) || '[]')); } catch { return new Set(); } };
const saveStamps = (s) => { try { localStorage.setItem(STORE_KEY, JSON.stringify([...s])); } catch { /* private mode */ } };

export default function App() {
  const gameRef = useRef(null);
  const [zone, setZone] = useState('A');
  const [near, setNear] = useState(null);
  const [sheet, setSheet] = useState(null);       // { kind: 'npc' | 'resident' | 'bus', data }
  const [toast, setToast] = useState(null);
  const [stamps, setStamps] = useState(loadStamps);
  const [showCompletePopup, setShowCompletePopup] = useState(false);
  const [hasShownCongrats, setHasShownCongrats] = useState(false);

  const open = useCallback((s) => { setSheet(s); emit('ui:open'); }, []);
  const close = useCallback(() => { setSheet(null); emit('ui:close'); }, []);

  // 스탬프가 12개가 되는 순간 축하 팝업 표시 (Set 자료구조는 .size 로 확인)
  useEffect(() => {
    if (stamps.size >= 12 && !hasShownCongrats) {
      setShowCompletePopup(true);
      setHasShownCongrats(true);
    }
  }, [stamps.size, hasShownCongrats]);

  useEffect(() => {
    const game = createGame(gameRef.current);
    let timer;
    const offs = [
      on('zone:ready', setZone),
      on('near', setNear),
      on('toast', (t) => { setToast(t); clearTimeout(timer); timer = setTimeout(() => setToast(null), 2200); }),
      on('talk:npc', (data) => {
        open({ kind: 'npc', data });
        setStamps((prev) => { const next = new Set(prev).add(data.placeId); saveStamps(next); return next; });
      }),
      on('talk:resident', (data) => open({ kind: 'resident', data })),
      on('bus:open', (from) => open({ kind: 'bus', data: from })),
    ];
    return () => { offs.forEach((off) => off()); clearTimeout(timer); game.destroy(true); };
  }, [open]);

  const pickZone = (key) => { close(); emit('zone:go', key); };
  const z = ZONES[zone];

  return (
    <div className="shell">
      <header className="top">
        <h1>메타-<b>대전</b> <span>유성 편</span></h1>
        <div className="stamps">스탬프 {stamps.size}/12</div>
      </header>
      <main className="stage">
        <div className="game" ref={gameRef} />
        <div className="hud zone"><small>ZONE {z.key} · {z.area}</small><strong>{z.title}</strong></div>
        {toast && !sheet && <div className="hud toast" role="status">{toast}</div>}
        {near && !sheet && (
          <button className="hud prompt" onClick={() => emit('input:talk')}>
            <kbd>SPACE</kbd>{near.name}와 대화하기
          </button>
        )}
        {!sheet && <TouchPad />}
        {sheet?.kind === 'npc' && <PlaceSheet talk={sheet.data} onClose={close} />}
        {sheet?.kind === 'resident' && <ResidentSheet talk={sheet.data} onClose={close} />}
        {sheet?.kind === 'bus' && <BusSheet from={sheet.data} onPick={pickZone} onClose={close} />}
        {showCompletePopup && (
          <StampCompleteSheet
            stampsCount={stamps.size}
            onClose={() => setShowCompletePopup(false)}
          />
        )}
      </main>
    </div>
  );
}

// On-screen arrows for phones. Hidden on devices with a mouse (see styles.css).
function TouchPad() {
  const press = (x, y) => (e) => { e.preventDefault(); emit('input:dir', { x, y }); };
  const release = (e) => { e.preventDefault(); emit('input:dir', { x: 0, y: 0 }); };
  const btn = (label, x, y, area) => (
    <button style={{ gridArea: area }} aria-label={label}
      onPointerDown={press(x, y)} onPointerUp={release} onPointerLeave={release} onPointerCancel={release}>{label}</button>
  );
  return (
    <div className="touch">
      <div className="pad">{btn('▲', 0, -1, '1/2')}{btn('◀', -1, 0, '2/1')}{btn('▶', 1, 0, '2/3')}{btn('▼', 0, 1, '3/2')}</div>
      <button className="talk" onClick={() => emit('input:talk')}>대화</button>
    </div>
  );
}