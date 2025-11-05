#!/data/data/com.termux/files/usr/bin/bash

# 안드로이드 데이터 수집 및 윈도우 전송 자동화 스크립트
# Termux에서 실행

# 설정
WINDOWS_IP="192.168.0.100"  # 윈도우 IP로 변경하세요
WINDOWS_PORT="9999"
INTERVAL=300  # 수집 주기 (초) - 5분마다

echo "======================================"
echo "안드로이드 데이터 수집 & 전송 시작"
echo "======================================"
echo "윈도우 서버: $WINDOWS_IP:$WINDOWS_PORT"
echo "수집 주기: $INTERVAL 초"
echo ""

# 필요한 패키지 확인
check_packages() {
    echo "필요한 패키지 확인 중..."
    
    if ! command -v termux-battery-status &> /dev/null; then
        echo "termux-api 설치 중..."
        pkg install termux-api -y
    fi
    
    if ! command -v nc &> /dev/null; then
        echo "netcat 설치 중..."
        pkg install netcat-openbsd -y
    fi
    
    if ! command -v python &> /dev/null; then
        echo "python 설치 중..."
        pkg install python -y
    fi
    
    echo "패키지 확인 완료!"
}

# 패키지 확인
check_packages

# 무한 루프로 주기적 실행
while true; do
    echo ""
    echo "----------------------------------------"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 데이터 수집 시작"
    echo "----------------------------------------"
    
    # 1. 데이터 수집
    bash collect_android_data.sh
    
    # 2. 윈도우로 전송
    sleep 2
    python send_to_windows.py
    
    echo ""
    echo "다음 수집까지 $INTERVAL 초 대기..."
    sleep $INTERVAL
done
