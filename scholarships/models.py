from django.db import models

class Scholarship(models.Model):
    # 기존 필드들
    university_type = models.CharField(max_length=255, null=True)  # 대학구분
    recruitment_start = models.DateField(null=True)  # 모집시작일
    recruitment_end = models.DateField(null=True)  # 모집종료일
    product_id = models.CharField(max_length=50, null=True)  # 번호
    product_type = models.CharField(max_length=50, null=True)  # 상품구분
    name = models.CharField(max_length=255, null=True)  # 상품명
    selection_method_details = models.TextField(null=True)  # 선발방법 상세내용
    number_of_recipients_details = models.TextField(null=True)  # 선발인원 상세내용
    grade_criteria_details = models.TextField(null=True)  # 성적기준 상세내용
    income_criteria_details = models.TextField(null=True)  # 소득기준 상세내용
    managing_organization_type = models.CharField(max_length=100, null=True)  # 운영기관구분
    foundation_name = models.CharField(max_length=255, null=True)  # 운영기관명
    eligibility_restrictions = models.TextField(null=True)  # 자격제한 상세내용
    required_documents_details = models.TextField(null=True)  # 제출서류 상세내용
    residency_requirement_details = models.TextField(null=True)  # 지역거주여부 상세내용
    support_details = models.TextField(null=True)  # 지원내역 상세내용
    recommendation_required = models.TextField(null=True)  # 추천필요여부 상세내용
    specific_qualification_details = models.TextField(null=True)  # 특정자격 상세내용
    major_field_type = models.CharField(max_length=255, null=True)  # 학과구분
    academic_year_type = models.CharField(max_length=255, null=True)  # 학년구분

    # 학자금유형구분 선택지 
    FINANCIAL_AID_CHOICES = [
        ('지역연고', '지역연고'), # (value, display_name): db 저장 값, 관리자 페이지 표시 값
        ('성적우수', '성적우수'),
        ('소득구분', '소득구분'),
        ('특기자', '특기자'),
        ('기타', '기타'),
    ]
    financial_aid_type = models.CharField(max_length=20, choices=FINANCIAL_AID_CHOICES, null=True)  # 학자금유형구분

    website_url = models.URLField(max_length=500, null=True)  # 홈페이지 주소
    gpt_success_tips = models.TextField(null=True, blank=True)  # GPT 합격 팁
    gpt_interview_tips = models.TextField(null=True, blank=True)  # GPT 면접 팁
    def __str__(self):
        return f"{self.name} ({self.foundation_name})"
