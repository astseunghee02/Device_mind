# 안드로이드 → 윈도우 소켓 통신 모니터링 시스템

Termux를 사용하여 안드로이드 기기의 시스템 정보를 수집하고 윈도우 PC로 실시간 전송하는 시스템입니다.

## 📋 필요 사항

### 안드로이드 (Termux)
- Termux 앱 설치 (Play Store 또는 F-Droid)
- Termux:API 앱 설치 (배터리 정보 수집용)

### 윈도우
- Python 3.x 설치
- 방화벽에서 9999 포트 허용

## 🚀 설치 및 실행 방법

### 1️⃣ Termux 설정 (안드로이드)

```bash
# Termux 업데이트
pkg update && pkg upgrade

# 필요한 패키지 설치
pkg install termux-api netcat-openbsd python

# 스크립트 다운로드 (또는 직접 복사)
# collect_android_data.sh
# send_to_windows.py
# auto_monitor.sh

# 실행 권한 부여
chmod +x collect_android_data.sh
chmod +x send_to_windows.py
chmod +x auto_monitor.sh

# IP 주소 설정 (중요!)
# send_to_windows.py와 auto_monitor.sh 파일에서
# WINDOWS_IP를 자신의 윈도우 PC IP로 변경
nano send_to_windows.py
nano auto_monitor.sh
```

**윈도우 IP 확인 방법:**
- 윈도우에서 `cmd` 실행 → `ipconfig` 입력
- IPv4 주소 확인 (예: 192.168.0.100)

### 2️⃣ 윈도우 설정

```bash
# 윈도우에서 Python 서버 실행
python windows_server.py
```

서버가 시작되면 다음과 같이 표시됩니다:
```
============================================================
안드로이드 로그 수신 서버
============================================================
서버 시작됨: 0.0.0.0:9999
안드로이드 기기로부터 데이터를 기다리는 중...
```

### 3️⃣ Termux에서 모니터링 시작

**방법 1: 자동 모니터링 (추천)**
```bash
# 5분마다 자동으로 데이터 수집 및 전송
bash auto_monitor.sh
```

**방법 2: 수동 실행**
```bash
# 데이터 수집
bash collect_android_data.sh

# 윈도우로 전송
python send_to_windows.py
```

## 📊 수집되는 데이터

1. **배터리 정보**
   - 배터리 잔량 (%)
   - 충전 상태
   - 배터리 온도
   - 건강 상태

2. **CPU 사용량**
   - 전체 CPU 사용률
   - 코어별 사용률

3. **메모리 정보**
   - 총 메모리
   - 사용 중인 메모리
   - 여유 메모리

4. **프로세스 정보**
   - CPU 사용률 높은 프로세스 Top 10

5. **네트워크 정보**
   - IP 주소
   - 네트워크 인터페이스 상태

6. **저장공간 정보**
   - 전체 용량
   - 사용 중인 용량
   - 남은 용량

7. **시스템 가동 시간**

## 📁 파일 구조

```
Termux (안드로이드):
├── collect_android_data.sh    # 데이터 수집 스크립트
├── send_to_windows.py          # 소켓 클라이언트
├── auto_monitor.sh             # 자동화 스크립트
└── android_log.txt             # 수집된 로그 (임시)

Windows:
├── windows_server.py           # 소켓 서버
└── android_logs/               # 수신된 로그 저장 폴더
    ├── android_log_20241105_143022.txt
    ├── android_log_20241105_143522.txt
    └── ...
```

## 🔧 설정 변경

### 수집 주기 변경
`auto_monitor.sh` 파일에서:
```bash
INTERVAL=300  # 초 단위 (기본값: 300초 = 5분)
```

### 포트 번호 변경
모든 파일에서 `9999`를 원하는 포트로 변경:
- `send_to_windows.py`
- `auto_monitor.sh`
- `windows_server.py`

## ⚠️ 문제 해결

### "연결 거부됨" 오류
1. 윈도우 서버가 실행 중인지 확인
2. 윈도우 방화벽 설정 확인
3. IP 주소가 올바른지 확인
4. 안드로이드와 윈도우가 같은 네트워크에 있는지 확인

### 배터리 정보가 수집되지 않음
```bash
# Termux:API 앱 설치 확인
pkg install termux-api
# Play Store에서도 Termux:API 앱 별도 설치 필요
```

### 백그라운드 실행
```bash
# Termux Wake Lock 활성화
termux-wake-lock

# 백그라운드 실행
nohup bash auto_monitor.sh > monitor.log 2>&1 &
```

## 🛑 중지 방법

### Termux에서
```bash
# Ctrl+C 또는 프로세스 종료
pkill -f auto_monitor.sh
```

### 윈도우에서
```bash
# Ctrl+C
```

## 💡 추가 기능 아이디어

- 웹 대시보드로 실시간 모니터링
- 데이터베이스에 저장하여 통계 분석
- 알림 기능 (배터리 낮음, CPU 과부하 등)
- 암호화 통신 추가 (TLS/SSL)

## 📝 라이선스

자유롭게 사용 및 수정 가능합니다.
