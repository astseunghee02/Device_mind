# -*- coding: utf-8 -*-

"""
Windows 서버 - Android JSON 로그 수신
"""

import socket
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from pathlib import Path


class LogServer:
    """로그 수신 서버 클래스"""

    def __init__(self, config_path: str = "config.json"):
        """
        초기화

        Args:
            config_path: 설정 파일 경로
        """
        self.config = self._load_config(config_path)
        self.host = '0.0.0.0'  # 모든 인터페이스에서 수신
        self.port = self.config['server']['port']
        self.save_dir = Path(self.config['paths']['windows_save_dir'])
        self.server_socket = None

        # 로깅 설정
        self._setup_logging()

        # 저장 디렉토리 생성
        self._create_save_directory()

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
                'port': 9999
            },
            'paths': {
                'windows_save_dir': 'android_logs'
            }
        }

    def _setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def _create_save_directory(self):
        """저장 디렉토리 생성"""
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"저장 디렉토리: {self.save_dir.absolute()}")
        except Exception as e:
            self.logger.error(f"디렉토리 생성 실패: {e}")
            raise

    def _receive_data(self, client_socket: socket.socket) -> Optional[bytes]:
        """
        데이터 수신 (크기 헤더 포함)

        Args:
            client_socket: 클라이언트 소켓

        Returns:
            수신된 데이터 (실패시 None)
        """
        try:
            # 데이터 크기 수신 (4바이트 빅엔디안)
            size_header = client_socket.recv(4)
            if not size_header or len(size_header) < 4:
                self.logger.warning("크기 헤더 수신 실패")
                return None

            data_size = int.from_bytes(size_header, byteorder='big')
            self.logger.info(f"예상 데이터 크기: {data_size:,} bytes")

            # 데이터 수신
            data = b''
            remaining = data_size

            while remaining > 0:
                chunk_size = min(4096, remaining)
                chunk = client_socket.recv(chunk_size)

                if not chunk:
                    self.logger.warning("데이터 수신 중단")
                    break

                data += chunk
                remaining -= len(chunk)

            if len(data) != data_size:
                self.logger.warning(
                    f"데이터 크기 불일치 (예상: {data_size}, 수신: {len(data)})"
                )

            return data if data else None

        except Exception as e:
            self.logger.error(f"데이터 수신 오류: {e}")
            return None

    def _parse_json_data(self, data: bytes) -> Optional[Dict[str, Any]]:
        """
        JSON 데이터 파싱

        Args:
            data: 바이트 데이터

        Returns:
            파싱된 JSON 데이터 (실패시 None)
        """
        try:
            json_str = data.decode('utf-8')
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 파싱 실패: {e}")
            return None
        except UnicodeDecodeError as e:
            self.logger.error(f"UTF-8 디코딩 실패: {e}")
            return None
        except Exception as e:
            self.logger.error(f"데이터 파싱 오류: {e}")
            return None

    def _save_log_file(self, log_data: Dict[str, Any]) -> Optional[Path]:
        """
        로그 파일 저장

        Args:
            log_data: 저장할 로그 데이터

        Returns:
            저장된 파일 경로 (실패시 None)
        """
        try:
            # 파일명 생성
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'android_log_{timestamp}.json'
            filepath = self.save_dir / filename

            # JSON 파일로 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"로그 저장됨: {filepath}")

            # 추가로 요약 정보 저장
            self._save_summary(log_data, timestamp)

            return filepath

        except Exception as e:
            self.logger.error(f"파일 저장 오류: {e}")
            return None

    def _save_summary(self, log_data: Dict[str, Any], timestamp: str):
        """
        로그 요약 정보 저장

        Args:
            log_data: 로그 데이터
            timestamp: 타임스탬프
        """
        try:
            summary_file = self.save_dir / f'summary_{timestamp}.txt'

            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("Android 로그 요약\n")
                f.write("=" * 60 + "\n\n")

                # 수집 시간
                if 'collection_time' in log_data:
                    f.write(f"수집 시간: {log_data['collection_time']}\n\n")

                data = log_data.get('data', {})

                # 배터리 정보
                if 'battery' in data:
                    battery = data['battery']
                    f.write("--- 배터리 ---\n")
                    if 'percentage' in battery:
                        f.write(f"  배터리 잔량: {battery['percentage']}%\n")
                    if 'temperature' in battery:
                        f.write(f"  온도: {battery['temperature']}°C\n")
                    if 'status' in battery:
                        f.write(f"  상태: {battery['status']}\n")
                    f.write("\n")

                # 메모리 정보
                if 'memory' in data:
                    memory = data['memory']
                    if 'details' in memory:
                        mem_details = memory['details']
                        f.write("--- 메모리 ---\n")
                        if 'MemTotal' in mem_details:
                            f.write(f"  전체: {mem_details['MemTotal']}\n")
                        if 'MemAvailable' in mem_details:
                            f.write(f"  사용 가능: {mem_details['MemAvailable']}\n")
                        f.write("\n")

                # 저장공간 정보
                if 'storage' in data and 'filesystems' in data['storage']:
                    f.write("--- 저장공간 ---\n")
                    for fs in data['storage']['filesystems'][:3]:  # 상위 3개만
                        f.write(
                            f"  {fs['mounted_on']}: {fs['used']}/{fs['size']} "
                            f"({fs['use_percent']})\n"
                        )
                    f.write("\n")

                # 시스템 정보
                if 'system' in data:
                    system = data['system']
                    f.write("--- 시스템 ---\n")
                    if 'device_manufacturer' in system:
                        f.write(f"  제조사: {system['device_manufacturer']}\n")
                    if 'device_model' in system:
                        f.write(f"  모델: {system['device_model']}\n")
                    if 'android_version' in system:
                        f.write(f"  안드로이드 버전: {system['android_version']}\n")
                    if 'uptime' in system:
                        f.write(f"  가동시간: {system['uptime']}\n")

            self.logger.info(f"요약 파일 저장됨: {summary_file}")

        except Exception as e:
            self.logger.warning(f"요약 파일 저장 실패: {e}")

    def _handle_client(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        """
        클라이언트 처리

        Args:
            client_socket: 클라이언트 소켓
            client_address: 클라이언트 주소
        """
        self.logger.info(f"연결됨: {client_address[0]}:{client_address[1]}")

        try:
            # 데이터 수신
            data = self._receive_data(client_socket)

            if not data:
                self.logger.warning("데이터 수신 실패")
                return

            self.logger.info(f"수신된 데이터 크기: {len(data):,} bytes")

            # JSON 파싱
            log_data = self._parse_json_data(data)

            if not log_data:
                self.logger.warning("JSON 파싱 실패")
                client_socket.sendall("오류: JSON 파싱 실패".encode('utf-8'))
                return

            # 파일 저장
            saved_path = self._save_log_file(log_data)

            # 클라이언트에게 응답
            if saved_path:
                response = f"데이터 수신 완료 - {saved_path.name}"
                self.logger.info(f"처리 완료: {client_address[0]}")
            else:
                response = "오류: 파일 저장 실패"
                self.logger.error(f"파일 저장 실패: {client_address[0]}")

            client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            self.logger.error(f"클라이언트 처리 오류: {e}")

        finally:
            client_socket.close()
            self.logger.info(f"연결 종료: {client_address[0]}")

    def start(self):
        """서버 시작"""
        try:
            # 소켓 생성
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 바인드 및 리스닝
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            self.logger.info(f"서버 시작됨: {self.host}:{self.port}")
            self.logger.info("안드로이드 기기로부터 데이터를 기다리는 중...\n")

            # 클라이언트 연결 대기 루프
            while True:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    self._handle_client(client_socket, client_address)
                    print()  # 빈 줄 출력

                except Exception as e:
                    self.logger.error(f"클라이언트 연결 처리 오류: {e}")

        except KeyboardInterrupt:
            self.logger.info("\n\n서버 종료 중...")

        except Exception as e:
            self.logger.error(f"서버 오류: {e}")

        finally:
            if self.server_socket:
                self.server_socket.close()
            self.logger.info("서버가 종료되었습니다.")


def main():
    """메인 함수"""
    print("=" * 60)
    print("Android 로그 수신 서버 (JSON)")
    print("=" * 60)
    print()

    server = LogServer()
    server.start()


if __name__ == "__main__":
    main()
