# Nginx의 기본 Ubuntu 이미지 사용
FROM nginx:latest

# 기본 설정 파일 삭제
RUN rm /etc/nginx/conf.d/default.conf



# # 가상 환경 생성 및 활성화
# RUN python3 -m venv /opt/venv

# # 가상 환경에 필요한 Python 패키지 설치
# RUN /opt/venv/bin/pip install pygeoip ipaddr

# # GeoLite2 데이터베이스 변환 스크립트 설치
# RUN git clone https://github.com/sherpya/geolite2legacy /opt/geolite2legacy

# # GeoLite2 데이터베이스 다운로드 (라이센스 키를 환경 변수로 설정하여 사용)
# WORKDIR /opt/geolite2legacy/maxmind-geo
# RUN wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key=${MAXMIND_LICENSE_KEY}&suffix=zip" -O ./GeoLite2-Country-CSV.zip

# # GeoLite2 CSV 파일을 .dat 파일로 변환 (가상 환경의 Python 사용)
# WORKDIR /opt/geolite2legacy
# RUN /opt/venv/bin/python ./geolite2legacy.py -i ./maxmind-geo/GeoLite2-Country-CSV.zip -f ./geoname2fips.csv -o ./maxmind-geo/GeoIP.dat

# # 변환된 GeoIP.dat 파일을 Nginx가 사용할 수 있는 디렉터리로 이동
# RUN mv ./maxmind-geo/GeoIP.dat /usr/share/GeoIP/GeoIP.dat

RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libpcre3 \
    libpcre3-dev \
    zlib1g-dev \
    libssl-dev \
    libgeoip-dev \
    geoip-database \
    unzip \
    curl \
    gnupg2 \
    ca-certificates \
    libssl-dev

# Nginx 소스 다운로드 및 GeoIP 모듈을 포함하여 컴파일
WORKDIR /usr/src
RUN wget http://nginx.org/download/nginx-1.22.1.tar.gz && \
    tar -zxvf nginx-1.22.1.tar.gz && \
    cd nginx-1.22.1 && \
    ./configure --with-http_geoip_module --prefix=/etc/nginx && \
    make && \
    make install

# GeoIP Legacy 데이터 다운로드 및 압축 해제
# 압축 해제 시 기존 파일이 있으면 삭제 후 덮어쓰는 방식으로 수정
RUN mkdir -p /usr/share/GeoIP && \
    wget https://centminmod.com/centminmodparts/geoip-legacy/GeoIP.dat.gz -O /usr/share/GeoIP/GeoIP.dat.gz && \
    rm -f /usr/share/GeoIP/GeoIP.dat && \
    gunzip /usr/share/GeoIP/GeoIP.dat.gz


# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 기본 명령 실행
#CMD ["nginx", "-g", "daemon off;"]
