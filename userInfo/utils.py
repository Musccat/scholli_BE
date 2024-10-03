import json
import openai
from django.conf import settings
from django.db import models
import re
from datetime import datetime

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY

# 소득분위와 중위소득 비율 매핑
income_brackets = {
    '1분위': '30%',
    '2분위': '50%',
    '3분위': '70%',
    '4분위': '90%',
    '5분위': '100%',
    '6분위': '130%',
    '7분위': '150%',
    '8분위': '200%',
    '9분위': '300%',
    '10분위': '300% 초과'
}

# 모집 날짜와 관련된 필터링 함수
def filter_scholarships_by_date(current_date, scholarships):
    return scholarships.filter(
        recruitment_start__lte=current_date,
        recruitment_end__gte=current_date
    )

# 대학구분, 학년구분, 학과구분에 따른 필터링
def filter_basic(scholarships, user_info): # 객체의 필드로 접근
    return scholarships.filter(
        models.Q(university_type__icontains=user_info.univ_category) |  
        models.Q(university_type__icontains='해당없음') |
        models.Q(university_type__icontains='특정대학')
    ).filter(
        models.Q(academic_year_type__icontains=user_info.semester) |  
        models.Q(academic_year_type__icontains='해당없음')
    ).filter(
        models.Q(major_field_type__icontains=user_info.major) |  
        models.Q(major_field_type__icontains='해당없음') |
        models.Q(major_field_type__icontains='특정학과')
    )

# '해당없음' 장학금과 그 외 장학금을 나누는 함수
def separate_scholarships(scholarships):
    no_criteria_scholarships = scholarships.filter(residency_requirement_details="해당없음")
    criteria_scholarships = scholarships.exclude(residency_requirement_details="해당없음")
    return no_criteria_scholarships, criteria_scholarships


# GPT로 지역 거주 조건 필터링
def gpt_filter_region(user_info, scholarships):
    user_info_text = f"학생의 거주지역: {user_info.residence}"  # 딕셔너리가 아니라 객체의 필드로 접근
    scholarships_text = "\n".join([
        f"번호: {scholarship.product_id}, 운영기관명: {scholarship.foundation_name}, 상품명: {scholarship.name}, 지역 거주 여부: {scholarship.residency_requirement_details}, 특정 자격: {scholarship.specific_qualification_details}"
        for scholarship in scholarships
    ])

    prompt = f"""
    {user_info_text}
    아래는 현재 모집 중인 장학금 목록입니다.
    이 목록에서 학생의 거주 지역 조건과 일치하는 장학금만 반환해 주세요.
    조건에 맞지 않는 장학금은 제외해 주세요.

    장학금 목록:
    {scholarships_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )

    remaining_scholarships_text = response['choices'][0]['message']['content'].strip()
    remaining_scholarships_ids = re.findall(r"번호: (\d+)", remaining_scholarships_text)

    return [int(scholarship_id) for scholarship_id in remaining_scholarships_ids]

# GPT 기반 추천 장학금 필터링
def recommend_scholarships(user_info, scholarships):
    middle_income_ratio = income_brackets.get(user_info.income, '알 수 없음')  # 필드로 접근

    user_info_text = f"""
    학생의 프로필:
    - 대학구분: {user_info.univ_category}
    - 성별: {user_info.gender}
    - 나이: {user_info.age}
    - 학년: {user_info.semester}
    - 학과: {user_info.major}
    - 성적: {user_info.totalGPA}
    - 소득분위: {user_info.income} (중위소득 비율: {middle_income_ratio})
    - 거주지역: {user_info.residence}
    """

    scholarships_text = "\n".join([
        f"번호: {scholarship.product_id}, 운영기관명: {scholarship.foundation_name}, 상품명: {scholarship.name}, 성적 기준: {scholarship.grade_criteria_details}, 소득 기준: {scholarship.income_criteria_details}, 지역 거주 여부: {scholarship.residency_requirement_details}, 특정 자격: {scholarship.specific_qualification_details}"
        for scholarship in scholarships
    ])

    prompt = f"""
    {user_info_text}
    위 학생의 조건에 맞는 장학금만 추천해 주세요.

    1. 성적 기준: 사용자의 성적이 장학금의 성적 기준보다 높거나 '기준 없음'인 장학금만 추천하세요.
    2. 소득 기준: 사용자의 소득분위가 장학금의 소득 기준보다 낮거나 '기준 없음'인 장학금만 추천하세요.
    3. 거주지역 요건: 사용자의 거주지역과 장학금의 거주지역 기준이 일치하거나 '기준 없음'인 장학금만 추천하세요.
    4. 전공 요건: 사용자의 전공과 일치하거나 '전공 불문'인 장학금만 추천하세요.
    5. 특정 자격 요건: 특정 자격을 요구하는 장학금은, 사용자가 해당 조건을 충족하지 않으면 제외하세요.

    장학금 목록:
    {scholarships_text}
    
    출력 형식은 아래와 같이 해줘
    (예시)
    1. **장학금 번호: 1,119**
    - 운영기관명:
    - 성적 기준:
    - 소득 기준:
    - 지역 거주 여부:
    - 특정 자격:

    2. **장학금 번호: 1,244**
    - 운영기관명:
    - 성적 기준:
    - 소득 기준:
    - 지역 거주 여부:
    - 특정 자격:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    recommended_scholarships_text = response['choices'][0]['message']['content'].strip()
    
    # GPT 응답 확인
    print(f"GPT 추천 응답: {recommended_scholarships_text}")

    scholarship_numbers = re.findall(r"장학금 번호: (\d+,\d+|\d+)", recommended_scholarships_text)
    print(f"GPT 추천된 장학금 번호: {scholarship_numbers}")

    return scholarship_numbers
