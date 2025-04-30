import requests

# 결제 샘플 데이터 목록
payments = [
    {"kiosk_id": "kiosk_001", "amount": 12000, "method": "카드", "timestamp": "2025-04-30T10:30:00"},
    {"kiosk_id": "kiosk_002", "amount": 7500, "method": "현금", "timestamp": "2025-04-30T11:00:00"},
    {"kiosk_id": "kiosk_001", "amount": 30000, "method": "간편결제", "timestamp": "2025-04-29T14:15:00"},
    {"kiosk_id": "kiosk_003", "amount": 18500, "method": "카드", "timestamp": "2025-04-30T12:45:00"},
    {"kiosk_id": "kiosk_002", "amount": 15000, "method": "현금", "timestamp": "2025-04-28T09:10:00"}
]

# 서버 주소
url = "http://localhost:8000/payment"

# 반복하면서 POST 요청 전송
for payment in payments:
    response = requests.post(url, json=payment)
    if response.status_code == 200:
        print("✅ 전송 성공:", response.json())
    else:
        print("❌ 전송 실패:", response.status_code, response.text)
