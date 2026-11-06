import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import 'galmuri/dist/galmuri.css';
import '@fontsource/gowun-dodum';
import './styles.css';

// document.fonts.load를 이용해 폰트 로딩이 완료된 후 React/Phaser 렌더링 시작
Promise.all([
  document.fonts.load('12px "Galmuri11"'),
  document.fonts.load('14px "Gowun Dodum"')
]).then(() => {
  createRoot(document.getElementById('root')).render(<App />);
}).catch(() => {
  // 폰트 로드 실패 시에도 폴백 폰트로 렌더링 보장
  createRoot(document.getElementById('root')).render(<App />);
});
