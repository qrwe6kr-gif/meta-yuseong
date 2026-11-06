// Place data downloaded from 한국관광콘텐츠랩 (관광정보 텍스트·이미지 다운로드). No API calls.
import data from './places.json';

export const CREDIT = data.credit;
export const PLACES = Object.fromEntries(data.places.map((p) => [p.id, p]));

// Photos live in public/, so prefix them with Vite's base URL.
export const photoUrl = (file) => `${import.meta.env.BASE_URL}${file}`;

// Photos to show in the place popup: the recommended picks first.
export function popupPhotos(place) {
  return place.photos.filter((p) => p.recommended).concat(place.photos.filter((p) => !p.recommended && !p.recommendedForPixelArt)).slice(0, 3);
}

// 유성장 opens on dates ending in 4 or 9.
export function marketInfo(now = new Date()) {
  const day = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const isMarket = (d) => d.getDate() % 5 === 4;
  if (isMarket(day)) return { today: true, label: '오늘은 유성장 장날!' };
  for (let i = 1; i < 12; i += 1) {
    const next = new Date(day);
    next.setDate(day.getDate() + i);
    if (isMarket(next)) return { today: false, label: `다음 장날 ${next.getMonth() + 1}월 ${next.getDate()}일` };
  }
  return { today: false, label: '4·9로 끝나는 날' };
}
