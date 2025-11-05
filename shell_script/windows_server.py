import socket
import os
from datetime import datetime

# 설정
HOST = '0.0.0.0'  # 모든 인터페이스에서 수신
PORT = 9999
SAVE_DIR = 'android_logs'  # 로그 저장 디렉토리

def start_server():
    # 저장 디렉토리 생성
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"디렉토리 생성됨: {SAVE_DIR}")
    
    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"서버 시작됨: {HOST}:{PORT}")
        print("안드로이드 기기로부터 데이터를 기다리는 중...\n")
        
        while True:
            # 클라이언트 연결 대기
            client_socket, client_address = server_socket.accept()
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 연결됨: {client_address}")
            
            try:
                # 데이터 수신
                data = b''
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                if data:
                    # 데이터 디코딩
                    log_content = data.decode('utf-8')
                    print(f"수신된 데이터 크기: {len(data)} bytes")
                    
                    # 파일로 저장
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = os.path.join(SAVE_DIR, f'android_log_{timestamp}.txt')
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(log_content)
                    
                    print(f"로그 저장됨: {filename}")
                    
                    # 클라이언트에게 응답
                    response = "데이터 수신 완료"
                    client_socket.sendall(response.encode('utf-8'))
                    
                    # 수신된 데이터 일부 출력
                    print("\n--- 수신된 데이터 미리보기 ---")
                    print(log_content[:500])  # 처음 500자만 출력
                    if len(log_content) > 500:
                        print("... (계속)")
                    print("--- 미리보기 끝 ---\n")
                
            except Exception as e:
                print(f"데이터 처리 중 오류: {e}")
            
            finally:
                client_socket.close()
                print(f"연결 종료: {client_address}")
    
    except KeyboardInterrupt:
        print("\n\n서버 종료 중...")
    
    finally:
        server_socket.close()
        print("서버가 종료되었습니다.")

if __name__ == "__main__":
    print("=" * 60)
    print("안드로이드 로그 수신 서버")
    print("=" * 60)
    start_server()
