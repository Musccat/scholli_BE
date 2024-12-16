# Musccat_Project_BE
24-1 이화여자대학교 캡스톤디자인과창업프로젝트 스타트 06팀 머스캣 BE

<br>

## 📍 프로젝트명: SCHOLLI
자신에게 적합한 장학금을 찾는 대학생을 위해 생성형 AI를 이용하여 각 사용자에게 맞는 장학금을 추천하고 <br>이전 수혜자들의 조언을 바탕으로 장학금 수혜 팁을 제공해주는 서비스
<br>
<img src="https://github.com/judymoody59/Musccat_Example/assets/108432112/b8bf2704-748e-4b22-9140-5c4692dd2db9" width="250" height="250" />
<br>
[SCHOLLI 사이트](https://www.schollli.site/)

## 👩‍💻 팀원
<table>
    <tr>
        <!-- 첫 번째 팀원 -->
        <td align="center" width="50%">
            <img src="https://avatars.githubusercontent.com/SeoYeomm" alt="Avatar" width="100px"/><br/>
            <a href="https://github.com/SeoYeomm">이서연</a>
            <br/>
            <img src="https://github-readme-stats.vercel.app/api?username=SeoYeomm&show_icons=true&theme=transparent" alt="Minju's GitHub stats" width="350px"/>
        </td>
        <!-- 두 번째 팀원 -->
        <td align="center" width="50%">
            <img src="https://avatars.githubusercontent.com/hayong39" alt="Avatar" width="100px"/><br/>
            <a href="https://github.com/hayong39">변하영</a>
            <br/>
            <img src="https://github-readme-stats.vercel.app/api?username=SeoYeomm&show_icons=true&theme=transparent" alt="Hayeong's GitHub stats" width="350px"/>
        </td>
    </tr>
</table>
<br/>

## 🛠️ 기술 스택

### 배포
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white"> <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=Amazon%20EC2&logoColor=white"> <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=Gunicorn&logoColor=white">

### 데이터베이스
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white"> <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white">

### 개발
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white">

### AI
<img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white">

<br/>

## 📂 프로젝트 아키텍처

```
📦scholli_BE
 ┣ 📂payment                                  # 구독권 결제 
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜iamport.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜utils.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂reviews                                  # 수혜자 조언 
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂scholarships                             # 장학금 조회
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜filters.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜pagination.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tasks.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜utils.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂userInfo                                 # 사용자 프로필 (사용자 상세 정보/추천장학금/마이페이지/관심목록)
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tasks.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜utils.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂users                              력
   ```
    # 아임포트 결제 시스템 
    IMP_KEY = env("IMP_KEY")
    IMP_SECRET = env("IMP_SECRET")
    MERCHANT_CODE = env("MERCHANT_CODE")
    
    # Celery 설정 
    CELERY_BROKER_URL =
    CELERY_RESULT_BACKEND =
    
    # OPENAI API 키 
    OPENAI_API_KEY = env("OPENAI_API_KEY")
    
    # 데이터베이스 설정
    DATABASES = {
        'default': {
            'ENGINE': 
            'NAME': env("DATABASE_NAME"),
            'USER': env("DATABASE_USER"),
            'PASSWORD': env("DATABASE_PASSWORD"),
            'HOST': env("DATABASE_HOST"),
            'PORT': env("DATABASE_PORT"),
        }
    }
    
    #JWT 토큰 
    SIMPLE_JWT = {
        'ALGORITHM': env("JWT_ALGORITHM"),
    }
    
    # 이메일 
    EMAIL_HOST_USER = env("EMAIL_HOST")
    EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
   ```
**4. 패키지 설치**
   ```
   pip install -r requirements.txt 
   ```
**5. 장학금 데이터 불러오기**
   ```
   python load_scholarships.py
   ```
**6. 실행**
   ```
   python manage.py runserver
   ```
