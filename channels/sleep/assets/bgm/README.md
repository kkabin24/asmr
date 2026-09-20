# BGM (나레이션 밑에 까는 음악)

| 파일 | 곡 | 라이선스 | 출처 |
|---|---|---|---|
| `scott_buckley_reverie.mp3` | Reverie — Scott Buckley | CC BY 4.0 | https://www.scottbuckley.com.au/library/reverie/ |

**영상 설명란에 반드시 아래 크레딧을 넣는다** (없으면 저작권 클레임이 걸린다고 작곡가가 명시):

```
'Reverie' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
```

- 벤치마크 에일린 2020(TRQV5h0XMns)이 실제로 쓴 곡 (docs/bodyscan-benchmark.md).
- 렌더: `sleep_render.py --bgm channels/sleep/assets/bgm/scott_buckley_reverie.mp3` — 나레이션 구간 동안 루프, 나레이션 끝나면 페이드아웃하며 백색소음으로 넘어간다. 게인은 settings.json `video.bgm_gain_db`.
- 다른 후보(잔잔한 피아노, 전부 CC BY 4.0): In This Moment · Meanwhile · The Long Dark · Midvinter · The Long Way Home · Adrift Among Infinite Stars — https://www.scottbuckley.com.au/library/instrumentation/piano/
