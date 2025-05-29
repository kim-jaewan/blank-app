import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

# 쿼리 파라미터 가져오기
token = st.query_params.get("token", [None])
token = token[0] if isinstance(token, list) else token

st.write("✅ 토큰:", token)
st.write("✅ 수신 여부:", token is not None)
st.write("📦 길이:", len(token) if token else 0)

def redirect_to(url: str):
    html(f"""
        <script>
            const url = new URL(window.location.href);
            url.searchParams.delete("token");
            window.location.replace("{url}");
        </script>
    """, height=0)

if token:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # 토큰이 유효하면 현재 URL에서 제거한 후 이동
        redirect_to(window.location.origin + window.location.pathname)
    except jwt.ExpiredSignatureError:
        redirect_to(A_LOGIN_URL)
    except jwt.InvalidTokenError:
        redirect_to(A_LOGIN_URL)
else:
    redirect_to(A_LOGIN_URL)
