import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

token = st.query_params.get("token", [None])
token = token[0] if isinstance(token, list) else token

def force_redirect(url: str):
    html(f"""
        <script>
            window.top.location.replace("{url}");
        </script>
    """, height=0)

# 토큰 없는 경우
if not token or token == "None":
    st.warning("🔁 로그인 페이지로 리디렉션 중입니다...")
    force_redirect(A_LOGIN_URL)
    st.stop()

# 토큰 검증
try:
    jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    st.success("✅ 유효한 토큰입니다.")
except jwt.ExpiredSignatureError:
    st.error("❌ 토큰 만료")
    force_redirect(A_LOGIN_URL)
    st.stop()
except jwt.InvalidTokenError:
    st.error("❌ 유효하지 않은 토큰")
    force_redirect(A_LOGIN_URL)
    st.stop()

# 인증 성공 시
st.write("✅ 인증된 사용자 페이지입니다.")
