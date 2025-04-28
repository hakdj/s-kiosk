import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from config.config import SERVER_URL

# ✅ 페이지 기본 설정
st.set_page_config(
    page_title="S-kiosk 관리자 대시보드",
    layout="wide"
)

st.title("S-kiosk 관리자 대시보드 📊")

# ✅ 공통 API 데이터 가져오기 함수
def fetch_data(endpoint):
    try:
        response = requests.get(f"{SERVER_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"서버 오류: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"서버 연결 실패: {e}")
        return []

# ✅ 결제 내역 페이지
def show_payments():
    st.subheader("💳 결제 내역")
    payments = fetch_data("/payments")
    if payments:
        df = pd.DataFrame(payments, columns=["ID", "Kiosk ID", "금액", "결제 방법", "시간"])
        st.dataframe(df)
        fig = px.bar(df, x="Kiosk ID", y="금액", title="키오스크별 결제 금액", text_auto=True)
        st.plotly_chart(fig)
    else:
        st.info("표시할 결제 데이터가 없습니다.")

# ✅ 상태 로그 페이지
def show_status_logs():
    st.subheader("🖥️ 장비 상태 로그")
    logs = fetch_data("/status-logs")
    if logs:
        df = pd.DataFrame(logs, columns=["ID", "Kiosk ID", "상태", "메시지", "시간"])
        st.dataframe(df)
    else:
        st.info("표시할 상태 로그가 없습니다.")

# ✅ 명령어 관리 페이지
def show_commands():
    st.subheader("🛠️ 원격 명령 관리")
    commands = fetch_data("/commands?kiosk_id=KIOSK-001")
    if commands:
        df = pd.DataFrame(commands, columns=["ID", "Kiosk ID", "명령어", "결과", "시간"])
        st.dataframe(df)
    else:
        st.info("표시할 명령어가 없습니다.")

# ✅ 사이드바 메뉴
menu = st.sidebar.selectbox(
    "메뉴를 선택하세요",
    ("결제 내역", "상태 로그", "원격 명령 관리")
)

# ✅ 메뉴에 따라 페이지 이동
if menu == "결제 내역":
    show_payments()
elif menu == "상태 로그":
    show_status_logs()
elif menu == "원격 명령 관리":
    show_commands()
