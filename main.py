from datetime import datetime, timedelta, timezone
import os
import requests

# 1. GitHub Secrets에서 디스코드 웹후크 URL을 안전하게 가져옵니다.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

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
# 게임 내 실제 전장 날짜에 맞추어 수정해주세요!
ANCHOR_DATE = datetime(2026, 7, 27).date()

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

today_str = today.strftime("%Y-%m-%d")

message_content = (
    f"⚔️ **[FF14] 오늘의 전장 안내 ({today_str})** ⚔️\n\n"
    f"오늘의 전장: 🔥 **`{today_frontline}`** 🔥\n\n"
    f"```text\n"
    f"[ 8일 로테이션 표 ]\n"
    f"{rotation_text}\n"
    f"```"
)

# 7. 디스코드 웹후크 전송
if not WEBHOOK_URL:
    print("에러: DISCORD_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
    exit(1)

payload = {"content": message_content}
response = requests.post(WEBHOOK_URL, json=payload)

if response.status_code in [200, 204]:
    print("메시지 전송 성공!")
else:
    print(
        f"전송 실패: 상태 코드 {response.status_code}, 응답 내용: {response.text}"
    )
