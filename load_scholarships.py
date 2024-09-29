import os
import django
import json

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholli.settings')
django.setup()
from scholarships.models import Scholarship

# JSON 파일들이 있는 디렉토리 설정
json_directory = './' 
json_files = ['response5.json', 'response6.json', 'response7.json', 'response8.json']

for json_file in json_files:
    file_path = os.path.join(json_directory, json_file)
    with open(file_path, 'r', encoding='utf-8') as file:
        scholarships_data = json.load(file)

    # JSON 파일 구조에 맞게 'data' 키 아래 있는 데이터를 가져옴
    scholarship_list = scholarships_data.get('data', [])

    for item in scholarship_list:
        Scholarship.objects.create(
            university_type=item.get("대학구분"),
            recruitment_start=item.get("모집시작일"),
            recruitment_end=item.get("모집종료일"),
            product_id=item.get("번호"),
            product_type=item.get("상품구분"),
            name=item.get("상품명"),
            selection_method_details=item.get("선발방법 상세내용"),
            number_of_recipients_details=item.get("선발인원 상세내용"),
            grade_criteria_details=item.get("성적기준 상세내용"),
            income_criteria_details=item.get("소득기준 상세내용"),
            managing_organization_type=item.get("운영기관구분"),
            foundation_name=item.get("운영기관명"),
            eligibility_restrictions=item.get("자격제한 상세내용"),
            required_documents_details=item.get("제출서류 상세내용"),
            residency_requirement_details=item.get("지역거주여부 상세내용"),
            support_details=item.get("지원내역 상세내용"),
            recommendation_required=item.get("추천필요여부"),
            specific_qualification_details=item.get("특정자격 상세내용"),
            major_field_type=item.get("학과구분"),
            academic_year_type=item.get("학년구분"),
            financial_aid_type=item.get("학자금유형구분"),
            website_url=item.get("홈페이지 주소"),
        )
