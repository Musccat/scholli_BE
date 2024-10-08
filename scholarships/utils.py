import openai
from django.conf import settings

# GPT로 팁을 추출하는 공통 함수
def extract_key_points_from_tips(tips):
    openai.api_key = settings.OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who responds in Korean."},
            {"role": "user", "content": f"""
            아래는 장학금 수혜자들이 합격과 면접에 성공하기 위한 팁들입니다.
            이 팁들로부터 가장 중요한 핵심 포인트를 두 개씩만 추출하여 '합격 팁'과 '면접 팁' 카테고리로 구분해주세요.
             
            {tips}

            출력 예시는 다음과 같아야 합니다:
            합격 팁:
            1. ~한 사람들이 많았어요. ~요.
            2. ~할 수록 수혜확률이 높아져요.~요.

            면접 팁:
            1. ~한 사람들이 많았어요. ~요.
            2. ~할 수록 수혜확률이 높아져요.~요.
            """}
        ],
        max_tokens=1500,
        temperature=0.5,
    )

    return response['choices'][0]['message']['content']