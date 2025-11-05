#!/data/data/com.termux/files/usr/bin/python

import socket
import os
from datetime import datetime

# 설정
WINDOWS_IP = "192.168.0.100"  # 윈도우 PC IP로 변경
WINDOWS_PORT = 9999
LOG_FILE = "/data/data/com.termux/files/home/android_log.txt"

def send_log_to_windows():
    try:
        # 로그 파일 읽기
        if not os.path.exists(LOG_FILE):
            print(f"로그 파일이 존재하지 않습니다: {LOG_FILE}")
            return False
        
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = f.read()
        
        # 소켓 생성 및 연결
        print(f"윈도우 서버 연결 중... {WINDOWS_IP}:{WINDOWS_PORT}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # 10초 타임아웃
        
        client_socket.connect((WINDOWS_IP, WINDOWS_PORT))
        print("서버 연결 성공!")
        
        # 데이터 전송
        client_socket.sendall(log_data.encode('utf-8'))
        print(f"데이터 전송 완료 ({len(log_data)} bytes)")
        
        # 서버 응답 받기 (선택사항)
        response = client_socket.recv(1024).decode('utf-8')
        print(f"서버 응답: {response}")
        
        # 소켓 종료
        client_socket.close()
        
        # 전송 성공 후 백업
        backup_name = f"{LOG_FILE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(LOG_FILE, backup_name)
        print(f"로그 백업됨: {backup_name}")
        
        return True
        
    except socket.timeout:
        print("오류: 서버 연결 시간 초과")
        return False
    except ConnectionRefusedError:
        print("오류: 서버가 응답하지 않습니다. 윈도우 서버가 실행 중인지 확인하세요.")
        return False
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

if __name__ == "__main__":
    send_log_to_windows()
