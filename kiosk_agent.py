
import time
import requests

KIOSK_ID = "KIOSK-001"
SERVER_URL = "http://127.0.0.1:8000"

def get_pending_commands():
    response = requests.get(f"{SERVER_URL}/commands", params={"kiosk_id": KIOSK_ID, "result": "pending"})
    if response.status_code == 200:
        return response.json()
    return []

def report_command_result(command_id, result="success"):
    payload = {"id": command_id, "result": result}
    response = requests.patch(f"{SERVER_URL}/update-command", json=payload)
    return response.status_code == 200

def run_kiosk_loop():
    print(f"[{KIOSK_ID}] 키오스크 명령 수신 대기 시작")
    while True:
        commands = get_pending_commands()
        if commands:
            for cmd in commands:
                cmd_id = cmd[0]
                command_text = cmd[2]
                print(f"🛠️ 명령 수신: [{cmd_id}] → '{command_text}' 실행 중...")

                # 실제 명령 실행 시뮬레이션
                time.sleep(2)  # 실행 시간 가정
                print(f"✅ 명령 [{cmd_id}] 실행 완료 → 결과 보고")

                # 서버에 실행 결과 보고
                report_command_result(cmd_id, result="success")
        else:
            print("📭 대기 중... 새로운 명령 없음.")
        
        time.sleep(5)  # 5초마다 서버 확인

if __name__ == "__main__":
    run_kiosk_loop()
