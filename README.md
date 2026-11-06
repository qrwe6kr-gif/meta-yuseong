# 메타-대전 유성 편 · 시작용 프로젝트

유성구 숨은 명소 12곳을 걷는 2D 픽셀 메타버스입니다. 지금은 **구역 A(온천과 장터)**와 **구역 B(과학로 박물관길)** 두 맵이 동작합니다. 걸어 다니고, NPC와 대화하면 콘텐츠랩 사진과 관광정보 팝업이 뜨고, 스탬프가 쌓이고, 버스 정류장에서 노선표가 열립니다.

## 실행하기

1. [Node.js](https://nodejs.org) 18 이상을 설치합니다. (LTS 버전 권장)
2. 이 폴더에서 터미널을 열고 아래를 입력합니다.

```
npm install      # 처음 한 번만
npm run dev      # 개발 서버 실행 → 브라우저에서 http://localhost:5173
```

- 조작: 방향키·WASD 이동, Space 대화, Esc 닫기. 휴대폰에서는 화면 방향 버튼과 '대화' 버튼.
- 맵 전체 보기: 주소 끝에 `?zoom=1` 또는 `?zoom=2`를 붙이면 맵 전체를 한 화면에서 볼 수 있습니다. 배치 확인이나 캡처할 때 쓰세요.
- 배포용 파일 만들기: `npm run build` → `dist/` 폴더를 그대로 웹에 올리면 됩니다 (GitHub Pages, Netlify 등).

## 폴더 구조

```
public/
  assets/
    tiles/pogeun-tiles.png     바닥 타일 7종 (16×16): 잔디·꽃잔디·흙길·물·온천물·나무데크·돌바닥
    sprites/*.png              플레이어·NPC(16×24), 나무(32×32), 덤불, 버스 정류장
    maps/zone-a.json           구역 A 맵 (Tiled로 열어서 수정)
    maps/zone-b.json           구역 B 맵
    boards/*.png               제1유형 사진을 변환한 픽셀 간판 5개 (구역 B는 액자 간판 sign-*.png로 사용 중, valley는 구역 C용)
    pogeun-26.gpl/.png/.hex    포근 26 팔레트
  photos/<장소ID>/              팝업에 쓰는 콘텐츠랩 사진 (장소별 추천 사진만)
  photos/credits.csv           사진별 공공누리 유형·출처
src/
  App.jsx                      화면 전체: 게임 + 상단바 + 팝업 + 휴대폰 버튼
  ui/Sheets.jsx                장소 팝업, 주민 대화, 버스 노선표
  game/scenes/WorldScene.js    맵 불러오기, 이동·충돌, NPC, 정류장
  game/scenes/BootScene.js     그림·맵 불러오기
  data/places.json             12곳 장소 데이터 (콘텐츠랩 엑셀 원문)
  data/zones.js                구역 목록 (맵이 준비된 구역만 ready: true)
  bus.js                       게임과 화면(React)을 잇는 이벤트 통로
scripts/pixelate.py            사진 → 포근 26 픽셀 간판 변환
scripts/draw_zone_a_props.py   구역 A 건물·소품 예시 그림 생성 (호텔·아치·그늘막·정자·물레방아·좌판)
scripts/draw_zone_b_props.py   구역 B 박물관 3곳·로켓·암석원·가로등·엑스포다리·액자 간판·NPC 생성
scripts/draw_zone_c_props.py   구역 C 감나무집·장수오리·폭포·감나무·보훈둘레길 안내판·액자 간판·NPC 생성
```

## 맵 수정하기 (Tiled)

1. [Tiled](https://www.mapeditor.org)를 설치하고 `public/assets/maps/zone-a.json`을 엽니다.
2. **ground** 레이어: 타일을 칠하는 바닥입니다. 물·온천물 타일은 `collides` 속성이 켜져 있어서 못 지나갑니다.
3. **objects** 레이어: 아래 '종류(Class)'를 가진 점·사각형을 놓으면 코드가 알아서 읽습니다.

| 종류 | 무엇 | 필요한 사용자 속성 |
| --- | --- | --- |
| spawn | 플레이어 시작 위치 | 없음 |
| arrive | 버스를 타고 왔을 때 나타나는 위치 (정류장 옆에 두기) | 없음 |
| npc | 장소 안내 NPC (대화하면 장소 팝업 + 스탬프) | placeId (예: footbath), sprite, greeting |
| resident | 주민 NPC (꿀팁 한 줄) | sprite, line |
| tree, bush | 나무·덤불 (밑동에 부딪힘) | 없음 |
| building | 건물·좌판처럼 부딪히는 그림 | sprite, footW·footH (밑동 크기, 정수) |
| decor | 아치·그늘막처럼 지나갈 수 있는 그림 | sprite |
| bus | 버스 정류장 (사각형) | 없음 |
| label | 지도 위 이름표 | text |

4. 저장할 때 형식은 **JSON**, 타일셋은 맵에 포함(Embed)된 상태를 유지하세요.

## 구역 B·C 추가하기

1. Tiled에서 `zone-b.json`을 다른 이름으로 저장해 `zone-c.json`을 만들고 맵을 새로 그립니다. `spawn`·`arrive`·`bus` 오브젝트는 꼭 남겨 두세요.
2. NPC의 `placeId`를 `geo`, `money`, `science`, `bridge` (구역 C는 `valley`, `kam`, `duck`, `trail`)로 바꿉니다.
3. `src/data/zones.js`에서 해당 구역을 `ready: true`로 바꾸면 버스 노선표에서 갈 수 있습니다.
4. NPC 그림을 새로 그렸다면 `public/assets/sprites/`에 넣고 `BootScene.js`의 `SPRITES` 목록에 이름을 추가합니다.

## 그림 바꾸기

- 지금 들어 있는 타일·캐릭터는 포근 26 스타일 예시입니다. 같은 파일 이름으로 덮어쓰면 바로 반영됩니다.
- 규칙: 타일 16×16, 캐릭터 16×24, 외곽선은 #3b2f3a 한 색, 빛은 왼쪽 위, 한 타일에 4~5색.
- 플레이어 걷기 애니메이션(4방향 × 3프레임)을 그리면 `WorldScene.js`의 player를 스프라이트 시트로 바꿔 연결하면 됩니다.

## 사진 사용 규칙 (중요)

| 공공누리 | 할 수 있는 것 | 하면 안 되는 것 |
| --- | --- | --- |
| 제1유형 | 출처 표시 후 사용, 자르기, 픽셀아트 변환 | 출처 빼기 |
| 제3유형 | 출처 표시 후 **원본 그대로** 보여 주기 | 자르기·변환·합성 |

- 팝업 사진은 `object-fit: contain`으로 잘리지 않게 보여 줍니다. 이 설정을 유지하세요.
- 픽셀 간판은 제1유형 사진으로만 만드세요.

```
pip install pillow
python scripts/pixelate.py public/photos/geo/geo_hq_06_type1.jpg public/assets/boards/geo.png 60 36
```

## 다음 할 일 (4~9일차)

- [x] 구역 A 꾸미기: 온천호텔 2채, 유성온천 아치, 족욕장 그늘막·세족대·안내판, 정자·물레방아, 장터 좌판 8개 배치 (11/7)
- [ ] 한글 픽셀 폰트 넣기 (`src/styles.css`의 @font-face 주석 참고, 라이선스 확인)
- [x] 구역 B 꾸미기: 지질·화폐·과학관 건물, 로켓, 암석원, 가로등, 갑천과 엑스포다리, 픽셀 액자 간판 4개, NPC 4명·주민 2명, 버스 도착 위치 (11/7)
- [x] 구역 C(수통골 숲길) 맵 그리기 및 소품·NPC 배치 완료 (11/7)
- [ ] 플레이어 걷기 애니메이션

데이터 제공: 한국관광공사 한국관광콘텐츠랩

## 폰트 라이선스

- **Galmuri11**: Created by quiple (SIL Open Font License 1.1)
- **Gowun Dodum**: Created by Yanghee Ryu (SIL Open Font License 1.1)
