from datetime import datetime, timedelta, timezone
import requests

# 1. 디스코드 웹후크 URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1530962165299941568/GIO4r1bf3bt-PXbz34r7fJgt50E2wszhuarSPyEmd0qZKEtra-odsIYVFxx0p-kYbKYu"

# 2. 전장 로테이션 목록 (총 8일 주기)
ROTATION = [
    "봉인된 바위섬(쟁탈전)",
    "영광의 평원(쇄빙전)",
    "온살 하카이르(계절끝 합전)",
    "워코 치테(연습전)",
    "봉인된 바위섬(쟁탈전)",
    "외곽 유적지대(제압전)",
    "온살 하카이르(계절끝 합전)",
    "워코 치테(연습전)",
]

# 3. 기준일 설정 (예: 기준일이 '봉인된 바위섬(쟁탈전)'인 날짜 YYYY, MM, DD)
# 실제 게임 내 해당 날짜로 변경해주세요!
ANCHOR_DATE = datetime(2026, 7, 29).date()

# 4. 한국 시간(KST) 기준 오늘 날짜 구하기
kst = timezone(timedelta(hours=9))
today = datetime.now(kst).date()

# 5. 오늘 전장 계산 (기준일과의 차이 % 8)
days_diff = (today - ANCHOR_DATE).days
today_index = days_diff % 8
today_frontline = ROTATION[today_index]

# 6. 디스코드 전송 메시지 구성
rotation_text = "\n".join(
    [
        f"{'👉 ' if i == today_index else '  '} {i+1}. {map_name}"
        for i, map_name in enumerate(ROTATION)
    ]
)

message_content = f"""⚔️ **[FF14] 오늘의 전장 안내 ({today.strftime('%Y-%m-%d')})** ⚔️

**오늘의 전장:** 🔥 **`{today_frontline}`** 🔥

```text
[ 8일 로테이션 표 ]
{rotation_text}