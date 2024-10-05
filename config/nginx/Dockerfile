# # Use an official Nginx image as the base image
# FROM nginx:latest
# # Remove any existing config files
# RUN rm /etc/nginx/conf.d/*
# # Copy the custom Nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/
# # Expose port 80 for Nginx
# EXPOSE 80

# nginx/Dockerfile
FROM nginx:latest

# 기본 설정 파일 삭제 (*)
RUN rm /etc/nginx/conf.d/default.conf

# 필요한 패키지 설치 (python-pip, wget, git 등)
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    git \
    && pip3 install pygeoip ipaddr

# GeoLite2 데이터베이스 변환 스크립트 설치
RUN git clone https://github.com/sherpya/geolite2legacy /opt/geolite2legacy

# GeoLite2 데이터베이스 다운로드 (라이센스 키를 환경 변수로 설정하여 사용)
WORKDIR /opt/geolite2legacy/maxmind-geo
RUN wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key=${MAXMIND_LICENSE_KEY}&suffix=zip" -O ./GeoLite2-Country-CSV.zip

# GeoLite2 CSV 파일을 .dat 파일로 변환
WORKDIR /opt/geolite2legacy
RUN ./geolite2legacy.py -i ./maxmind-geo/GeoLite2-Country-CSV.zip -f ./geoname2fips.csv -o ./maxmind-geo/GeoIP.dat

# 변환된 GeoIP.dat 파일을 Nginx가 사용할 수 있는 디렉터리로 이동
RUN mv ./maxmind-geo/GeoIP.dat /usr/share/GeoIP/GeoIP.dat

# nginx 설정 파일 복사 (*)
COPY nginx.conf /etc/nginx/conf.d


# Nginx의 기본 명령 실행
# CMD ["nginx", "-g", "daemon off;"]