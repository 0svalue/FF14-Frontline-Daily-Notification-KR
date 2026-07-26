from datetime import datetime, timedelta, timezone
import os
import random
import requests

# 1. GitHub Secrets에서 디스코드 웹후크 URL을 가져옵니다.
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

# 각 전장별 랜덤 멘트 목록 (원하는 문구로 자유롭게 변경 가능!)
CUSTOM_MESSAGES = {
    "봉인된 바위섬(쟁탈전)": [
        "\u001b[31m🔥 \u001b[33m봉\u001b[32m바!\u001b[34m봉\u001b[35m바!\u001b[36m봉바! \u001b[31m🔥",
        "\u001b[36m🏝️ 오늘은 \u001b[33m봉바 타임! \u001b[32m거점 점령하러 \u001b[35m가자! 🏝️",
        "\u001b[35m⚔️ 봉인된 바위섬 개장! \u001b[33m바위 치러 \u001b[32m갑시다! ⚔️",
    ],
    "영광의 평원(쇄빙전)": [
        "\u001b[34m🧊 얼음 깰 시간이다! \u001b[36m쇄빙전 \u001b[33m출발! 🧊",
        "\u001b[36m❄️ 영광의 평원! \u001b[35m오늘 대형 얼음은 \u001b[32m우리 거! ❄️",
        "\u001b[33m⛏️ 쇄빙쇄빙! \u001b[31m얼음 쾅쾅 \u001b[34m깨러 가요! ⛏️",
    ],
    "온살 하카이르(계절끝 합전)": [
        "\u001b[31m⛺ 온살! \u001b[33m온살! \u001b[32m센언 폭파점 \u001b[35m제발! ⛺",
        "\u001b[32m🐎 온살 하카이르! \u001b[36m땅따먹기 \u001b[33m대작전! 🐎",
        "\u001b[33m🏹 오늘은 온살! \u001b[31m달려라 \u001b[35m달려! 🏹",
    ],
    "외곽 유적지대(제압전)": [
        "\u001b[35m🏛️ 추억의 제압전! \u001b[33m외곽 \u001b[32m유적지대! 🏛️",
        "\u001b[31m💥 제압전이다! \u001b[36m기지 점령하고 \u001b[33m가실게요! 💥",
        "\u001b[34m🛡️ 외곽 유적지대 오픈! \u001b[32m거점을 \u001b[35m지켜라! 🛡️",
    ],
    "워코 치테(연습전)": [
        "\u001b[32m⚔️ 연습전 워코 치테! \u001b[33m가볍게 \u001b[35m즐겨볼까요? ⚔️",
        "\u001b[36m🎯 워코 치테! \u001b[31m스킬 연습하기 \u001b[33m좋은 날! 🎯",
        "\u001b[33m🥊 연습전 개장! \u001b[35m오늘도 즐거운 \u001b[32m전장 되세요! 🥊",
    ],
}

# 3. 기준일 설정 (예: 기준일이 '봉인된 바위섬(쟁탈전)'인 날짜 YYYY, MM, DD)
ANCHOR_DATE = datetime(2026, 7, 29).date()

# 4. 한국 시간(KST) 기준 오늘 날짜 및 요일 구하기
kst = timezone(timedelta(hours=9))
today = datetime.now(kst).date()

weekdays = ["월", "화", "수", "목", "금", "토", "일"]
weekday_str = weekdays[today.weekday()]

# 5. 오늘 전장 계산 (기준일과의 차이 % 8)
days_diff = (today - ANCHOR_DATE).days
today_index = days_diff % 8
today_frontline = ROTATION[today_index]

# 오늘의 랜덤 멘트 뽑기 (설정된 목록이 없으면 기본 이름 출력)
messages = CUSTOM_MESSAGES.get(
    today_frontline, [f"🔥 **`{today_frontline}`** 🔥"]
)
today_custom_message = random.choice(messages)

# 6. 디스코드 전송 메시지 구성
rotation_text = "\n".join(
    [
        f"{'👉 ' if i == today_index else '  '} {i+1}. {map_name}"
        for i, map_name in enumerate(ROTATION)
    ]
)

today_str = today.strftime("%Y-%m-%d")

message_content = (
    f"`[FF14] 오늘의 전장 안내 ({today_str} {weekday_str}요일)`\n\n"
    f"## 오늘은 {today_custom_message}\n\n"
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
