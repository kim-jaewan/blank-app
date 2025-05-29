import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

token = st.query_params.get("token", [None])
token = token[0] if isinstance(token, list) else token

def redirect_js(url: str):
    html(f"""
        <script>
            window.location.href = "{url}";
        </script>
    """, height=0)

# 토큰 없는 경우 즉시 JS 리디렉션
if not token or token == "None":
    st.warning("🔁 로그인 페이지로 리디렉션 중입니다...")
    redirect_js(A_LOGIN_URL)
    st.stop()

# 토큰 검증
try:
    jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    st.success("토큰 유효 ✅")
except jwt.ExpiredSignatureError:
    st.error("토큰 만료 ❌")
    redirect_js(A_LOGIN_URL)
    st.stop()
except jwt.InvalidTokenError:
    st.error("잘못된 토큰 ❌")
    redirect_js(A_LOGIN_URL)
    st.stop()

# 정상 페이지 출력
st.write("🔓 인증된 사용자 페이지입니다.")
