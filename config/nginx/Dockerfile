# # Use an official Nginx image as the base image
# FROM nginx:latest
# # Remove any existing config files
# RUN rm /etc/nginx/conf.d/*
# # Copy the custom Nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/
# # Expose port 80 for Nginx
# EXPOSE 80

# nginx/Dockerfile
FROM nginx:alpine

# 기본 설정 파일 삭제 (*)
RUN rm /etc/nginx/conf.d/default.conf

# GeoIP 관련 패키지 설치
RUN apk add --no-cache \
    libmaxminddb \
    geoip \
    geoip-dev \
    geoip-database \
    geoipupdate \
    && mkdir -p /usr/share/GeoIP \
    && geoipupdate

# GeoIP2 데이터베이스 변환 스크립트 설치
RUN apk add --no-cache python3 git \
    && pip3 install pygeoip ipaddr \
    && git clone https://github.com/sherpya/geolite2legacy /opt/geolite2legacy

# MaxMind GeoLite2 데이터베이스 다운로드 및 변환
WORKDIR /opt/geolite2legacy
RUN wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key=${MAXMIND_LICENSE_KEY}&suffix=zip" -O ./GeoLite2-Country-CSV.zip \
    && ./geolite2legacy.py -i ./GeoLite2-Country-CSV.zip -f ./geoname2fips.csv -o /usr/share/GeoIP/GeoIP.dat


# nginx 설정 파일 복사 (*)
COPY nginx.conf /etc/nginx/conf.d

# Nginx의 GeoIP 모듈 활성화를 위해 설정 파일 복사 (필요시 추가)
COPY geoip.conf /etc/nginx/conf.d/

# Nginx의 기본 명령 실행
# CMD ["nginx", "-g", "daemon off;"]