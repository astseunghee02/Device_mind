#!/data/data/com.termux/files/usr/bin/bash

# 안드로이드 데이터 수집 및 윈도우 전송 자동화 스크립트 (JSON 버전)
# Termux에서 실행

# 스크립트 디렉토리로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# 설정 파일 로드
CONFIG_FILE="config.json"

# config.json에서 설정 읽기 (jq 사용)
if command -v jq &> /dev/null && [ -f "$CONFIG_FILE" ]; then
    WINDOWS_IP=$(jq -r '.server.host' "$CONFIG_FILE")
    WINDOWS_PORT=$(jq -r '.server.port' "$CONFIG_FILE")
    INTERVAL=$(jq -r '.collection.interval' "$CONFIG_FILE")
else
    # 기본값
    WINDOWS_IP="192.168.0.100"
    WINDOWS_PORT="9999"
    INTERVAL=300
fi

# 로그 파일
LOG_FILE="$SCRIPT_DIR/auto_monitor.log"

# 로그 함수
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 시작 메시지
echo "======================================"
echo "Android 데이터 수집 & 전송 (JSON)"
echo "======================================"
log "스크립트 시작"
log "설정 - 윈도우 서버: $WINDOWS_IP:$WINDOWS_PORT"
log "설정 - 수집 주기: $INTERVAL 초"
echo ""

# 필요한 패키지 확인
check_packages() {
    log "필요한 패키지 확인 중..."

    local packages_to_install=()

    # termux-api 확인
    if ! command -v termux-battery-status &> /dev/null; then
        log "termux-api 필요"
        packages_to_install+=("termux-api")
    fi

    # python 확인
    if ! command -v python &> /dev/null; then
        log "python 필요"
        packages_to_install+=("python")
    fi

    # jq 확인 (JSON 파싱용)
    if ! command -v jq &> /dev/null; then
        log "jq 필요 (JSON 파싱용)"
        packages_to_install+=("jq")
    fi

    # 패키지 설치
    if [ ${#packages_to_install[@]} -gt 0 ]; then
        log "다음 패키지 설치 중: ${packages_to_install[*]}"
        pkg install "${packages_to_install[@]}" -y

        if [ $? -eq 0 ]; then
            log "패키지 설치 완료"
        else
            log "오류: 패키지 설치 실패"
            return 1
        fi
    else
        log "모든 필수 패키지가 설치되어 있습니다"
    fi

    return 0
}

# 데이터 수집 함수
collect_data() {
    log "데이터 수집 시작"

    if ! python "$SCRIPT_DIR/collect_android_data.py"; then
        log "오류: 데이터 수집 실패"
        return 1
    fi

    log "데이터 수집 완료"
    return 0
}

# 데이터 전송 함수
send_data() {
    log "데이터 전송 시작"

    if ! python "$SCRIPT_DIR/send_to_windows.py"; then
        log "오류: 데이터 전송 실패"
        return 1
    fi

    log "데이터 전송 완료"
    return 0
}

# 서버 연결 확인 함수
check_server() {
    log "서버 연결 확인: $WINDOWS_IP:$WINDOWS_PORT"

    # nc 명령어로 포트 확인
    if command -v nc &> /dev/null; then
        if nc -z -w 3 "$WINDOWS_IP" "$WINDOWS_PORT" 2>/dev/null; then
            log "서버 연결 가능"
            return 0
        else
            log "경고: 서버에 연결할 수 없습니다"
            return 1
        fi
    else
        log "경고: nc 명령어를 찾을 수 없습니다. 서버 확인 건너뜀"
        return 0
    fi
}

# 신호 처리 (Ctrl+C)
trap 'log "스크립트 종료 신호 받음"; log "자동 모니터링 종료"; exit 0' INT TERM

# 패키지 확인
if ! check_packages; then
    log "오류: 패키지 확인 실패. 스크립트 종료"
    exit 1
fi

echo ""
log "자동 모니터링 시작"
echo ""

# 실행 횟수
run_count=0
success_count=0
fail_count=0

# 무한 루프로 주기적 실행
while true; do
    ((run_count++))

    echo ""
    echo "========================================"
    log "실행 #$run_count"
    echo "========================================"

    # 1. 서버 연결 확인 (선택사항)
    check_server

    # 2. 데이터 수집
    if collect_data; then
        # 3. 윈도우로 전송
        sleep 2

        if send_data; then
            ((success_count++))
            log "성공: 데이터 수집 및 전송 완료"
        else
            ((fail_count++))
            log "실패: 데이터 전송 실패"
        fi
    else
        ((fail_count++))
        log "실패: 데이터 수집 실패"
    fi

    # 통계 출력
    echo ""
    log "통계 - 총: $run_count, 성공: $success_count, 실패: $fail_count"

    # 다음 수집까지 대기
    echo ""
    log "다음 수집까지 $INTERVAL 초 대기..."
    echo "----------------------------------------"

    sleep "$INTERVAL"
done
