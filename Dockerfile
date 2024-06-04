# 공식 Python 런타임 이미지를 베이스 이미지로 사용
FROM python:3.10-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /usr/src/app

# 현재 디렉토리의 requirements.txt 파일을 컨테이너 내 /usr/src/app 디렉토리로 복사
COPY ./requirements.txt ./

# requirements.txt에 명시된 필요한 패키지들 설치
RUN pip install --no-cache-dir -r requirements.txt

# 호스트의 나머지 소스 코드를 이미지 파일 시스템의 /usr/src/app 디렉토리로 복사
COPY . .

# 컨테이너 외부로 포트 8003을 열어둠
EXPOSE 8003

# 환경 변수 설정
ENV GUIDE_PORT=8003

# 컨테이너가 시작될 때 실행할 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
