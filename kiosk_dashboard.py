import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from io import BytesIO

# 설정
API_COMMANDS = "http://127.0.0.1:8000/commands"
API_STATUS_LOGS = "http://127.0.0.1:8000/status-logs"

st.set_page_config(page_title="S-kiosk 관리자 대시보드", layout="wide")
st.title("🛠️ S-kiosk 관리자 대시보드")

# 명령 필터
st.subheader("📋 명령 히스토리")
kiosk_filter = st.text_input("🔍 키오스크 ID로 필터 (예: KIOSK-001)")
status_filter = st.selectbox("📌 상태 필터", ["", "pending", "success", "failed"])

cmd_df = pd.DataFrame()

if st.button("🔄 새로고침") or True:
    params = {}
    if kiosk_filter:
        params["kiosk_id"] = kiosk_filter
    if status_filter:
        params["result"] = status_filter

    try:
        response = requests.get(API_COMMANDS, params=params)
        if response.status_code == 200:
            data = response.json()
            cmd_df = pd.DataFrame(data, columns=["ID", "키오스크 ID", "명령", "결과", "시간"])
            st.success(f"총 {len(cmd_df)}건 조회됨")
            st.dataframe(cmd_df, use_container_width=True)
        else:
            st.error("명령 데이터를 가져오지 못했습니다.")
    except Exception as e:
        st.error(f"명령 조회 실패: {e}")

if not cmd_df.empty:
    csv = cmd_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📁 명령 이력 CSV로 저장",
        data=csv,
        file_name="command_history.csv",
        mime="text/csv"
    )

    st.subheader("📊 명령 성공/실패 차트")
    bar_data = cmd_df.groupby(["키오스크 ID", "결과"]).size().reset_index(name="건수")
    bar_fig = px.bar(bar_data, x="키오스크 ID", y="건수", color="결과", barmode="group",
                     title="키오스크별 명령 결과 통계")
    st.plotly_chart(bar_fig, use_container_width=True)

    pie_data = cmd_df["결과"].value_counts().reset_index()
    pie_data.columns = ["결과", "건수"]
    pie_fig = px.pie(pie_data, values="건수", names="결과", title="전체 명령 결과 비율")
    st.plotly_chart(pie_fig, use_container_width=True)

# 상태 로그 표시
st.subheader("📡 키오스크 상태 로그")
status_df = pd.DataFrame()
try:
    response = requests.get(API_STATUS_LOGS)
    if response.status_code == 200:
        status_data = response.json()
        status_df = pd.DataFrame(status_data, columns=["ID", "키오스크 ID", "상태 코드", "상세 내용", "시간"])
        st.dataframe(status_df, use_container_width=True)
    else:
        st.warning("상태 로그 데이터를 가져오지 못했습니다.")
except Exception as e:
    st.error(f"상태 로그 조회 실패: {e}")

if not status_df.empty:
    csv_status = status_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📁 상태 로그 CSV로 저장",
        data=csv_status,
        file_name="status_logs.csv",
        mime="text/csv"
    )
