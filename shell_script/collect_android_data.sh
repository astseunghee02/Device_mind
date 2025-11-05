#!/data/data/com.termux/files/usr/bin/bash

# 안드로이드 데이터 수집 스크립트
# Termux에서 실행

LOG_FILE="/data/data/com.termux/files/home/android_log.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "수집 시간: $TIMESTAMP" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 1. 배터리 정보
echo -e "\n[배터리 정보]" >> "$LOG_FILE"
termux-battery-status >> "$LOG_FILE" 2>&1

# 2. CPU 사용량
echo -e "\n[CPU 사용량]" >> "$LOG_FILE"
top -bn1 | grep "CPU:" >> "$LOG_FILE" 2>&1
echo "CPU 코어별 사용률:" >> "$LOG_FILE"
grep 'cpu ' /proc/stat >> "$LOG_FILE" 2>&1

# 3. 메모리 사용량
echo -e "\n[메모리 정보]" >> "$LOG_FILE"
free -h >> "$LOG_FILE" 2>&1

# 4. 실행중인 프로세스 (상위 10개)
echo -e "\n[CPU 사용률 높은 프로세스 Top 10]" >> "$LOG_FILE"
ps aux | sort -rn -k 3 | head -10 >> "$LOG_FILE" 2>&1

# 5. 네트워크 정보
echo -e "\n[네트워크 정보]" >> "$LOG_FILE"
ifconfig 2>/dev/null >> "$LOG_FILE" || ip addr >> "$LOG_FILE" 2>&1

# 6. 저장공간 정보
echo -e "\n[저장공간 정보]" >> "$LOG_FILE"
df -h >> "$LOG_FILE" 2>&1

# 7. 시스템 가동 시간
echo -e "\n[시스템 가동시간]" >> "$LOG_FILE"
uptime >> "$LOG_FILE" 2>&1

echo -e "\n데이터 수집 완료\n" >> "$LOG_FILE"
