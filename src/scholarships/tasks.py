from celery import shared_task
from .models import Scholarship
from reviews.models import Review
from .utils import extract_key_points_from_tips

@shared_task
def update_all_scholarships_gpt_tips():
    scholarships = Scholarship.objects.all()

    for scholarship in scholarships:
        reviews = Review.objects.filter(scholarship=scholarship)

        if reviews.exists():
            advice_tips = "\n".join([review.advice for review in reviews])
            interview_tips = "\n".join([review.interviewTip for review in reviews])

            # GPT로 팁 추출
            tips = f"합격 팁: {advice_tips}\n면접 팁: {interview_tips}"
            gpt_tips = extract_key_points_from_tips(tips)

            # GPT 팁을 저장
            success_tips = gpt_tips.split("면접 팁:")[0].strip()
            interview_tips = gpt_tips.split("면접 팁:")[1].strip()

            scholarship.gpt_success_tips = success_tips
            scholarship.gpt_interview_tips = interview_tips
            scholarship.save()
