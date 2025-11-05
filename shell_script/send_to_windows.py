#!/data/data/com.termux/files/usr/bin/python
# -*- coding: utf-8 -*-

"""
Windows 서버로 JSON 로그 전송 스크립트
Termux에서 실행
"""

import socket
import os
import json
import time
import shutil
from datetime import datetime
from typing import Dict, Any, Optional


class LogSender:
    """로그 전송 클래스"""

    def __init__(self, config_path: str = "config.json"):
        """
        초기화

        Args:
            config_path: 설정 파일 경로
        """
        self.config = self._load_config(config_path)
        self.server_host = self.config['server']['host']
        self.server_port = self.config['server']['port']
        self.timeout = self.config['server']['timeout']
        self.log_file = self.config['paths']['log_file']
        self.backup_dir = self.config['paths']['backup_dir']
        self.retry_attempts = self.config['collection']['retry_attempts']
        self.retry_delay = self.config['collection']['retry_delay']

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"경고: 설정 파일을 찾을 수 없습니다. 기본값을 사용합니다.")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """기본 설정값 반환"""
        return {
            'server': {
                'host': '192.168.0.100',
                'port': 9999,
                'timeout': 10
            },
            'paths': {
                'log_file': '/data/data/com.termux/files/home/android_logs.json',
                'backup_dir': '/data/data/com.termux/files/home/backups'
            },
            'collection': {
                'retry_attempts': 3,
                'retry_delay': 5
            }
        }

    def _load_log_file(self) -> Optional[Dict[str, Any]]:
        """
        로그 파일 로드

        Returns:
            로그 데이터 (실패시 None)
        """
        if not os.path.exists(self.log_file):
            print(f"오류: 로그 파일이 존재하지 않습니다: {self.log_file}")
            return None

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            print(f"로그 파일 로드 완료: {self.log_file}")
            return log_data

        except json.JSONDecodeError as e:
            print(f"오류: JSON 파싱 실패 - {e}")
            return None
        except Exception as e:
            print(f"오류: 파일 읽기 실패 - {e}")
            return None

    def _send_data(self, data: Dict[str, Any]) -> bool:
        """
        데이터 전송

        Args:
            data: 전송할 데이터

        Returns:
            성공 여부
        """
        client_socket = None

        try:
            # JSON 문자열로 변환
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            data_bytes = json_data.encode('utf-8')

            # 데이터 크기 정보 추가 (4바이트 빅엔디안)
            data_size = len(data_bytes)
            size_header = data_size.to_bytes(4, byteorder='big')

            # 소켓 생성 및 연결
            print(f"윈도우 서버 연결 중... {self.server_host}:{self.server_port}")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(self.timeout)

            client_socket.connect((self.server_host, self.server_port))
            print("서버 연결 성공!")

            # 데이터 크기 전송
            client_socket.sendall(size_header)

            # 데이터 전송
            client_socket.sendall(data_bytes)
            print(f"데이터 전송 완료 ({data_size:,} bytes)")

            # 서버 응답 받기
            try:
                response = client_socket.recv(1024).decode('utf-8')
                print(f"서버 응답: {response}")
            except socket.timeout:
                print("경고: 서버 응답 타임아웃 (데이터는 전송됨)")

            return True

        except socket.timeout:
            print("오류: 서버 연결 시간 초과")
            return False
        except ConnectionRefusedError:
            print("오류: 서버가 응답하지 않습니다. 윈도우 서버가 실행 중인지 확인하세요.")
            return False
        except Exception as e:
            print(f"오류: 데이터 전송 실패 - {e}")
            return False
        finally:
            if client_socket:
                client_socket.close()

    def _backup_log_file(self) -> bool:
        """
        로그 파일 백업

        Returns:
            성공 여부
        """
        try:
            # 백업 디렉토리 생성
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir, exist_ok=True)

            # 백업 파일명 생성
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"android_logs_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)

            # 파일 이동
            shutil.move(self.log_file, backup_path)
            print(f"로그 백업됨: {backup_path}")

            # 오래된 백업 파일 정리 (최근 10개만 유지)
            self._cleanup_old_backups(max_backups=10)

            return True

        except Exception as e:
            print(f"경고: 백업 실패 - {e}")
            return False

    def _cleanup_old_backups(self, max_backups: int = 10):
        """
        오래된 백업 파일 정리

        Args:
            max_backups: 유지할 최대 백업 파일 수
        """
        try:
            if not os.path.exists(self.backup_dir):
                return

            # 백업 파일 목록 가져오기 (수정 시간 기준 정렬)
            backup_files = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('android_logs_') and filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    mtime = os.path.getmtime(filepath)
                    backup_files.append((filepath, mtime))

            # 수정 시간 기준 내림차순 정렬
            backup_files.sort(key=lambda x: x[1], reverse=True)

            # 오래된 파일 삭제
            for filepath, _ in backup_files[max_backups:]:
                os.remove(filepath)
                print(f"오래된 백업 파일 삭제: {filepath}")

        except Exception as e:
            print(f"경고: 백업 정리 실패 - {e}")

    def send_log_with_retry(self) -> bool:
        """
        재시도 로직을 포함한 로그 전송

        Returns:
            성공 여부
        """
        print("=" * 60)
        print("로그 전송 시작")
        print("=" * 60)
        print()

        # 로그 파일 로드
        log_data = self._load_log_file()
        if not log_data:
            return False

        # 재시도 로직
        for attempt in range(1, self.retry_attempts + 1):
            if attempt > 1:
                print(f"\n재시도 {attempt}/{self.retry_attempts}...")
                time.sleep(self.retry_delay)

            # 데이터 전송
            if self._send_data(log_data):
                print("\n전송 성공!")

                # 백업
                self._backup_log_file()

                print()
                print("=" * 60)
                print("완료!")
                print("=" * 60)
                return True

        print(f"\n오류: {self.retry_attempts}번 시도 후 전송 실패")
        return False


def main():
    """메인 함수"""
    sender = LogSender()
    success = sender.send_log_with_retry()

    # 종료 코드 반환
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
