import { useEffect, useRef, useState } from 'react';
import { PLACES, CREDIT, photoUrl, popupPhotos, marketInfo } from '../data/places.js';
import { ZONES, ZONE_KEYS } from '../data/zones.js';

const spriteUrl = (key) => `${import.meta.env.BASE_URL}assets/sprites/${key || 'player'}.png`;

// Types a line one character at a time, like an RPG dialogue box. Click or Space to skip.
function useTyping(text) {
  const [n, setN] = useState(0);
  const done = n >= text.length;
  useEffect(() => {
    if (done) return undefined;
    const t = setTimeout(() => setN((v) => v + 1), 24);
    return () => clearTimeout(t);
  }, [n, done]);
  return [text.slice(0, n), done, () => setN(text.length)];
}

// Shared frame for every popup: focus, Esc to close.
function Sheet({ label, onClose, small, children }) {
  const ref = useRef(null);
  useEffect(() => {
    ref.current?.focus({ preventScroll: true });
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);
  return (
    <section className={`sheet${small ? ' small' : ''}`} role="dialog" aria-label={label} tabIndex={-1} ref={ref}>
      {children}
    </section>
  );
}

function Speaker({ sprite, name, role, text, onClose }) {
  const [shown, done, skip] = useTyping(text);
  return (
    <header className="speaker">
      <div className="portrait"><img src={spriteUrl(sprite)} alt="" /></div>
      <div className="who">
        <div className="name">{name}</div>
        {role && <div className="role">{role}</div>}
        <p className="line" onClick={skip}>{shown}{!done && <span className="caret" />}</p>
      </div>
      <button className="close" onClick={onClose} aria-label="닫기">X</button>
    </header>
  );
}

export function PlaceSheet({ talk, onClose }) {
  const place = PLACES[talk.placeId];
  const photos = popupPhotos(place);
  const [index, setIndex] = useState(0);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const touchStartXRef = useRef(null);

  const photo = photos[index];
  const market = place.marketDays ? marketInfo() : null;
  const info = Object.entries(place.info).filter(([k]) => !['대표메뉴', '취급메뉴', '인허가번호', '상세정보'].includes(k));

  const nextPhoto = () => setIndex((i) => (i + 1) % photos.length);
  const prevPhoto = () => setIndex((i) => (i - 1 + photos.length) % photos.length);

  // Keyboard navigation & prev/next handling (Preventing game player movement)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') {
        e.stopPropagation();
        if (photos.length > 1) prevPhoto();
      } else if (e.key === 'ArrowRight') {
        e.stopPropagation();
        if (photos.length > 1) nextPhoto();
      }
    };
    window.addEventListener('keydown', handleKeyDown, true);
    return () => window.removeEventListener('keydown', handleKeyDown, true);
  }, [photos.length]);

  // Touch Swipe Handlers for Mobile
  const handleTouchStart = (e) => {
    touchStartXRef.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e) => {
    if (touchStartXRef.current === null || photos.length <= 1) return;
    const diffX = touchStartXRef.current - e.changedTouches[0].clientX;
    if (Math.abs(diffX) > 40) {
      if (diffX > 0) nextPhoto();
      else prevPhoto();
    }
    touchStartXRef.current = null;
  };

  return (
    <Sheet label={`${talk.name} 대화`} onClose={onClose}>
      <Speaker sprite={talk.sprite} name={talk.name} role={`${ZONES[place.zone].title} · ${place.name}`} text={talk.greeting} onClose={onClose} />
      <div className="body">
        <figure className="photo">
          <div
            className="photo-frame"
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
          >
            {photo && (
              <img
                src={photoUrl(photo.file)}
                alt={`${place.name} 사진`}
                onClick={() => setLightboxOpen(true)}
                title="클릭하여 크게 보기"
              />
            )}
            {photos.length > 1 && (
              <>
                <button className="nav-btn prev" onClick={prevPhoto} aria-label="이전 사진">‹</button>
                <button className="nav-btn next" onClick={nextPhoto} aria-label="다음 사진">›</button>
                <div className="counter">{index + 1} / {photos.length}</div>
              </>
            )}
          </div>
          {photos.length > 1 && (
            <div className="dots">
              {photos.map((p, i) => (
                <button key={p.file} className={i === index ? 'on' : ''} onClick={() => setIndex(i)} aria-label={`사진 ${i + 1}`} />
              ))}
            </div>
          )}
          {/* 제3유형은 변형 금지: 자르지 않고 원본 비율 그대로 보여 준다 (CSS object-fit: contain) */}
          {photo && <figcaption>사진: {CREDIT.replace('데이터 제공: ', '')}{photo.photographer ? ` · ${photo.photographer}` : ''} · {photo.license}</figcaption>}
        </figure>
        <div className="info">
          <h2>{place.name} {market && <span className={`chip${market.today ? ' hot' : ''}`}>{market.label}</span>}</h2>
          <p className="overview">{place.overview}</p>
          {place.menu && (
            <ul className="tags">
              {place.menu.main.map((m) => <li key={m} className="main">{m} <small>대표</small></li>)}
              {place.menu.more.map((m) => <li key={m}>{m}</li>)}
            </ul>
          )}
          <dl className="facts">
            {info.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}
            <div><dt>주소</dt><dd>{place.address}</dd></div>
          </dl>
          <a className="btn" href={`https://map.naver.com/p/search/${encodeURIComponent(place.name)}`} target="_blank" rel="noopener noreferrer">네이버 지도 길찾기 ↗</a>
          <p className="credit">{CREDIT}</p>
        </div>
      </div>

      {/* Lightbox / Modal view */}
      {lightboxOpen && photo && (
        <div className="lightbox-backdrop" onClick={() => setLightboxOpen(false)}>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setLightboxOpen(false)} aria-label="닫기">X</button>
            <div className="lightbox-image-wrap" onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>
              <img src={photoUrl(photo.file)} alt={`${place.name} 확대 사진`} />
              {photos.length > 1 && (
                <>
                  <button className="nav-btn prev" onClick={prevPhoto} aria-label="이전 사진">‹</button>
                  <button className="nav-btn next" onClick={nextPhoto} aria-label="다음 사진">›</button>
                  <div className="counter">{index + 1} / {photos.length}</div>
                </>
              )}
            </div>
            <figcaption>사진: {CREDIT.replace('데이터 제공: ', '')}{photo.photographer ? ` · ${photo.photographer}` : ''} · {photo.license}</figcaption>
          </div>
        </div>
      )}
    </Sheet>
  );
}

export function ResidentSheet({ talk, onClose }) {
  return (
    <Sheet label={`${talk.name} 대화`} onClose={onClose} small>
      <Speaker sprite={talk.sprite} name={talk.name} role="주민 · 꿀팁" text={talk.line} onClose={onClose} />
    </Sheet>
  );
}

export function BusSheet({ from, onPick, onClose }) {
  return (
    <Sheet label="버스 노선" onClose={onClose} small>
      <header className="speaker">
        <div className="who"><div className="name">유성 순환버스</div><p className="line">어디로 갈까요?</p></div>
        <button className="close" onClick={onClose} aria-label="닫기">X</button>
      </header>
      <div className="routes">
        {ZONE_KEYS.filter((k) => k !== from).map((k) => (
          <button key={k} className="route" disabled={!ZONES[k].ready} onClick={() => onPick(k)}>
            <b>{ZONES[k].title}</b>
            <small>{ZONES[k].ready ? ZONES[k].area : '맵 준비 중'}</small>
          </button>
        ))}
      </div>
    </Sheet>
  );
}