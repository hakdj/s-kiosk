# --- [1] 기본 import ---
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import hashlib
import sys
import os




# --- [2] 경로 및 서버 설정 ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config.config import SERVER_URL

# --- [3] 무조건 제일 먼저 페이지 설정 ---
st.set_page_config(page_title="S-kiosk 관리자 대시보드", layout="wide")

# --- [4] 🌐 언어 선택 + 번역 사전 ---
LANGUAGE = st.sidebar.selectbox("🌐 언어 선택 / Language", ("한국어", "English"))

from app.utils.utils import init_db
init_db()  # ✅ DB 테이블 생성


translations = {
    "dashboard_title": {
        "한국어": "S-kiosk 관리자 대시보드 📊",
        "English": "S-kiosk Admin Dashboard 📊"
    },
    "login_title": {
        "한국어": "🔒 관리자 로그인",
        "English": "🔒 Admin Login"
    },
    "username_input": {
        "한국어": "아이디 입력",
        "English": "Enter Username"
    },
    "password_input": {
        "한국어": "비밀번호 입력",
        "English": "Enter Password"
    },
    "login_button": {
        "한국어": "로그인",
        "English": "Login"
    },
    "menu_select": {
        "한국어": "메뉴를 선택하세요",
        "English": "Select a menu"
    },
    "logout_button": {
        "한국어": "🔒 로그아웃",
        "English": "🔒 Logout"
    },
    "logged_in_as": {
        "한국어": "👤 관리자: {username}님 접속 중입니다.",
        "English": "👤 Admin: {username} logged in."
    },
    # --- 기존 translations에 이어서 추가 ---
    "payment_header": {
        "한국어": "💳 결제 내역 조회",
        "English": "💳 View Payment Records"
    },
    "search_filter": {
        "한국어": "🔎 검색 및 필터",
        "English": "🔎 Search & Filter"
    },
    "search_kiosk_id": {
        "한국어": "키오스크 ID 검색",
        "English": "Search Kiosk ID"
    },
    "select_payment_method": {
        "한국어": "결제 방법 선택",
        "English": "Select Payment Method"
    },
    "select_date_range": {
        "한국어": "결제 날짜 범위 선택",
        "English": "Select Payment Date Range"
    },
    "select_amount_range": {
        "한국어": "결제 금액 범위 선택 (원)",
        "English": "Select Payment Amount Range (KRW)"
    },
    "no_payment_data": {
        "한국어": "표시할 결제 데이터가 없습니다.",
        "English": "No payment data to display."
    },
    "total_payment_amount": {
        "한국어": "💰 총 결제 금액:",
        "English": "💰 Total Payment Amount:"
    },
    "select_status": {
        "한국어": "상태 필터 선택",
        "English": "Select Status"
    },
    "search_command": {
        "한국어": "명령어 검색",
        "English": "Search Command"
    },
    "select_result": {
        "한국어": "결과 필터 (성공/실패)",
        "English": "Result Filter (Success/Fail)"
    },
    "select_command_date_range": {
        "한국어": "명령 실행 날짜 범위 선택",
        "English": "Select Command Execution Date Range"
    },
    "unit_won": {
        "한국어": "원",
        "English": "KRW"
    },
    "kiosk_payment_chart_title": {
        "한국어": "📊 키오스크별 결제 금액",
        "English": "📊 Payment by Kiosk"
    },
    "kiosk_payment_chart_subtitle": {
        "한국어": "키오스크별 결제 금액 합계",
        "English": "Total Payment Amount by Kiosk"
    },
    "total_payment_amount_unit": {
        "한국어": "원",
        "English": "KRW"
    },
    "payment_chart_header": {
        "한국어": "📊 키오스크별 결제 금액",
        "English": "📊 Payment Amount by Kiosk"
    },
    "payment_chart_title": {
        "한국어": "키오스크별 결제 금액 합계",
        "English": "Total Payment per Kiosk"
    },
    "status_log_header": {
    "한국어": "🖥️ 장비 상태 로그",
    "English": "🖥️ Device Status Logs"
    },
    "search_filter": {  # 이미 있으면 생략
        "한국어": "🔎 검색 및 필터",
        "English": "🔎 Search & Filter"
    },
    "search_columns_placeholder": {
        "한국어": "검색어 입력 (Kiosk ID, 상태, 메시지)",
        "English": "Enter search term (Kiosk ID, Status, Message)"
    },
    "select_status": {
        "한국어": "상태 필터 선택",
        "English": "Select Status"
    },
    "select_date_range": {  # 이미 있으면 생략
        "한국어": "날짜 범위 선택",
        "English": "Select Date Range"
    },
    "no_status_log_data": {
        "한국어": "표시할 상태 로그가 없습니다.",
        "English": "No status logs to display."
    },
    "status_chart_header": {
        "한국어": "📊 상태별 비율",
        "English": "📊 Status Distribution"
    },
    "status_chart_pie_title": {
        "한국어": "상태별 비율",
        "English": "Status Distribution"
    },
    "status_chart_bar_title": {
        "한국어": "상태별 건수 막대그래프",
        "English": "Status Count Bar Chart"
    }

                
}

# --- [5] 로그인 관리 코드 ---
admin_accounts = {
    "admin": hashlib.sha256("1234".encode()).hexdigest(),
    "superuser": hashlib.sha256("abcd".encode()).hexdigest()
}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'login_attempts' not in st.session_state:
    st.session_state['login_attempts'] = 0

def login_page():
    st.title(translations["login_title"][LANGUAGE])

    username = st.text_input(translations["username_input"][LANGUAGE])
    password = st.text_input(translations["password_input"][LANGUAGE], type="password")

    if st.button(translations["login_button"][LANGUAGE]):
        if st.session_state['login_attempts'] >= 5:
            st.error("로그인 5회 실패. 더 이상 접근할 수 없습니다.")
            st.stop()

        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username in admin_accounts and input_password_hash == admin_accounts[username]:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"환영합니다, {username}님!")
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
            st.session_state['login_attempts'] += 1

# --- [6] 로그인 상태 확인 ---
if not st.session_state['logged_in']:
    login_page()
    st.stop()

# --- [7] 로그인 통과한 사람만 대시보드 시작 ---
st.title(translations["dashboard_title"][LANGUAGE])
st.info(translations["logged_in_as"][LANGUAGE].format(username=st.session_state['username']))

# --- [8] fetch_data 함수 ---
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

from app.utils.utils import DB_PATH  # 이건 이미 있을 수도 있음
st.write(f"📁 Streamlit이 사용 중인 DB 경로: {DB_PATH}")


# --- [9-1] 결제 내역 조회 (show_payments) ---
def show_payments():
    st.subheader(translations["payment_header"][LANGUAGE])
    payments = fetch_data("/payments")

    if not payments:
        st.info(translations["no_payment_data"][LANGUAGE])
        return

    df = pd.DataFrame(payments, columns=["ID", "Kiosk ID", "금액", "결제 방법", "시간"])
    df['시간'] = pd.to_datetime(df['시간'])

    min_date = df['시간'].min().date()
    max_date = df['시간'].max().date()
    if df['금액'].dropna().empty:
        st.warning("💳 유효한 결제 금액 데이터가 없습니다.")
        return

    min_amount = int(df['금액'].min())
    max_amount = int(df['금액'].max())

    # 🔎 검색 및 필터 영역
    st.markdown(f"### {translations['search_filter'][LANGUAGE]}")
    search_text = st.text_input(translations["search_kiosk_id"][LANGUAGE])
    payment_methods = df['결제 방법'].dropna().unique().tolist()
    selected_payment_methods = st.multiselect(translations["select_payment_method"][LANGUAGE], options=payment_methods)

    start_date, end_date = st.date_input(
        translations["select_date_range"][LANGUAGE],
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if min_amount == max_amount:
        amount_range = (min_amount, max_amount)
        st.info(f"{min_amount:,}{translations['total_payment_amount_unit'][LANGUAGE]} 결제 금액만 존재합니다.")
    else:
        amount_range = st.slider(
            translations["select_amount_range"][LANGUAGE],
            min_value=min_amount,
            max_value=max_amount,
            value=(min_amount, max_amount),
            step=1000
        )

    # 🔍 필터링 적용
    filtered_df = df.copy()

    if search_text:
        filtered_df = filtered_df[filtered_df['Kiosk ID'].str.contains(search_text, case=False)]

    if selected_payment_methods:
        filtered_df = filtered_df[filtered_df['결제 방법'].isin(selected_payment_methods)]

    filtered_df = filtered_df[
        (filtered_df['시간'].dt.date >= start_date) & (filtered_df['시간'].dt.date <= end_date)
    ]

    filtered_df = filtered_df[
        (filtered_df['금액'] >= amount_range[0]) & (filtered_df['금액'] <= amount_range[1])
    ]

    # 📄 테이블 출력
    st.dataframe(filtered_df, use_container_width=True)

    # 💰 총 금액 표시
    st.markdown(
        f"### {translations['total_payment_amount'][LANGUAGE]} "
        f"**{filtered_df['금액'].sum():,} {translations['total_payment_amount_unit'][LANGUAGE]}**"
    )

    # 💾 CSV 다운로드
    csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="💾 CSV 다운로드",
        data=csv,
        file_name="filtered_payment_records.csv",
        mime="text/csv",
    )

    # 📊 차트
    if not filtered_df.empty:
        st.subheader(translations["payment_chart_header"][LANGUAGE])
        chart_df = filtered_df.groupby('Kiosk ID')['금액'].sum().reset_index()
        fig = px.bar(
            chart_df,
            x="Kiosk ID",
            y="금액",
            text_auto=True,
            title=translations["payment_chart_title"][LANGUAGE]
        )
        st.plotly_chart(fig, use_container_width=True)


# --- [9-2] 장비 상태 로그 (show_status_logs) ---
def show_status_logs():
    st.subheader(translations["status_log_header"][LANGUAGE])

    logs = fetch_data("/status-logs")
    if not logs:
        st.info(translations["no_status_log_data"][LANGUAGE])
        return

    df = pd.DataFrame(logs, columns=["ID", "Kiosk ID", "상태", "메시지", "시간"])
     # 🔴 수정: 오류 방지용으로 errors='coerce' 추가
    df['시간'] = pd.to_datetime(df['시간'], errors='coerce')  # 🔴

    # 🔎 검색 및 필터
    st.markdown(f"### {translations['search_filter'][LANGUAGE]}")

    search_columns = ["Kiosk ID", "상태", "메시지"]
    search_text = st.text_input(translations["search_columns_placeholder"][LANGUAGE])

    status_options = df['상태'].dropna().unique().tolist()
    selected_status = st.multiselect(translations["select_status"][LANGUAGE], options=status_options)

    # 🔴 추가: 유효한 시간값이 없으면 종료
    if df['시간'].dropna().empty:  # 🔴
        st.warning("⏱️ 유효한 시간 데이터가 없습니다.")  # 🔴
        return  # 🔴

    min_date = df['시간'].min().date()
    max_date = df['시간'].max().date()
    start_date, end_date = st.date_input(
        translations["select_date_range"][LANGUAGE],
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 🔍 필터 적용
    filtered_df = df.copy()

    if search_text:
        search_text_lower = search_text.lower()
        mask = filtered_df[search_columns].apply(
            lambda x: x.astype(str).str.lower().str.contains(search_text_lower)
        ).any(axis=1)
        filtered_df = filtered_df[mask]

    if selected_status:
        filtered_df = filtered_df[filtered_df['상태'].isin(selected_status)]

    filtered_df = filtered_df[
        (filtered_df['시간'].dt.date >= start_date) & (filtered_df['시간'].dt.date <= end_date)
    ]

    # 📄 필터링된 테이블 출력
    st.dataframe(filtered_df, use_container_width=True)

    # 💾 CSV 다운로드
    csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="💾 CSV 다운로드",
        data=csv,
        file_name="filtered_status_logs.csv",
        mime="text/csv",
    )

    # 📊 차트
    if not filtered_df.empty:
        st.subheader(translations["status_chart_header"][LANGUAGE])

        status_counts = filtered_df['상태'].value_counts().reset_index()
        status_counts.columns = ['상태', '건수']

        pie_fig = px.pie(
            status_counts,
            names='상태',
            values='건수',
            title=translations["status_chart_pie_title"][LANGUAGE],
            hole=0.4
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        bar_fig = px.bar(
            status_counts,
            x='상태',
            y='건수',
            text_auto=True,
            title=translations["status_chart_bar_title"][LANGUAGE]
        )
        st.plotly_chart(bar_fig, use_container_width=True)


# --- [9-3] 원격 명령 관리 (show_commands) ---
def show_commands():
    # --- 🛠️ 새 명령어 직접 입력해서 전송하기 ---
    st.subheader("📝 새 명령어 직접 입력")

    with st.form("send_new_command"):
        new_kiosk_id = st.text_input("Kiosk ID", placeholder="예: kiosk_001")
        new_command_text = st.text_input("명령어", placeholder="예: reboot")

        submitted = st.form_submit_button("🚀 명령어 전송")

        if submitted:
            if not new_kiosk_id or not new_command_text:
                st.warning("Kiosk ID와 명령어를 모두 입력해주세요.")
            else:
                new_payload = {
                    "kiosk_id": new_kiosk_id,
                    "command": new_command_text,
                    "result": "pending",
                    "timestamp": datetime.now().isoformat()
                }
                response = requests.post(f"{SERVER_URL}/remote-command", json=new_payload)

                if response.status_code == 200:
                    st.success("✅ 명령어 전송 완료!")
                else:
                    st.error(f"❌ 전송 실패: {response.status_code}")

    st.subheader("🛠️ 원격 명령 관리")

    # --- 🛠️ 새 명령어 전송 섹션 ---
    #send_command_section()

    # --- 📥 데이터 가져오기 ---
    commands = fetch_data("/remote-commands")

    if not commands:
        st.info("표시할 명령어가 없습니다.")
        return

    # --- 📄 데이터프레임 변환 ---
    df = pd.DataFrame(commands, columns=["id", "kiosk_id", "command", "result", "timestamp"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- 📊 명령어 성공률 카드 ---
    total_count = len(df)
    success_count = (df['result'] == "성공").sum()
    success_rate = (success_count / total_count) * 100 if total_count else 0

    st.metric(label="📈 명령어 성공률", value=f"{success_rate:.1f}%")

    # --- 🎨 테이블 색상 적용 (성공 초록, 실패 빨강) ---
    def color_result(val):
        color = 'green' if val == "성공" else 'red'
        return f'color: {color}'

    #st.dataframe(df.style.applymap(color_result, subset=['result']), use_container_width=True)

    # (임시 교체)
    st.dataframe(df, use_container_width=True)

    # --- 🔥 실패한 명령어 재전송 기능 ---
    st.subheader("🔄 실패한 명령어 재전송")

    failed_df = df[df['result'] == "실패"]

    if not failed_df.empty:
        selected_ids = st.multiselect(
            "재전송할 실패 명령어 선택 (ID 기준)",
            options=failed_df['id'].tolist()
        )

        if st.button("🚀 선택한 명령어 재전송"):
            if selected_ids:
                for selected_id in selected_ids:
                    # 선택된 ID의 명령어 가져오기
                    cmd_row = failed_df[failed_df['id'] == selected_id].iloc[0]
                    payload = {
                        "kiosk_id": cmd_row['kiosk_id'],
                        "command": cmd_row['command'],
                        "result": "pending",  # 다시 전송하니까 상태 pending
                        "timestamp": datetime.now().isoformat()
                    }
                    response = requests.post(f"{SERVER_URL}/remote-command", json=payload)

                    if response.status_code == 200:
                        st.success(f"ID {selected_id} 명령어 재전송 성공!")
                    else:
                        st.error(f"ID {selected_id} 명령어 재전송 실패: {response.status_code}")

            else:
                st.warning("재전송할 실패 명령어를 선택하세요.")
    else:
        st.info("실패한 명령어가 없습니다.")

    # --- 📊 명령별 실행 통계 차트 ---
    st.subheader("📊 명령어별 실행 통계")

    if not df.empty:
        command_stats = df.groupby(["command", "result"]).size().reset_index(name="count")

        # Pie Chart
        pie_fig = px.pie(
            command_stats,
            names="command",
            values="count",
            title="명령어별 실행 비율",
            hole=0.4
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        # Bar Chart
        bar_fig = px.bar(
            command_stats,
            x="command",
            y="count",
            color="result",
            text_auto=True,
            title="명령어별 성공/실패 건수"
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    else:
        st.info("통계 분석할 명령어 데이터가 없습니다.")




# --- [10] 메뉴 선택 + [11] 로그아웃 버튼 ---
menu = st.sidebar.selectbox(
    translations["menu_select"][LANGUAGE],
    ("결제 내역", "상태 로그", "원격 명령 관리")
)

if menu == "결제 내역":
    show_payments()
elif menu == "상태 로그":
    show_status_logs()
elif menu == "원격 명령 관리":
    show_commands()

if st.sidebar.button(translations["logout_button"][LANGUAGE]):
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['login_attempts'] = 0
    st.success("로그아웃되었습니다. 다시 로그인 해주세요.")
    st.experimental_rerun()
