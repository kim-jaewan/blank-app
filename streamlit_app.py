import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

# 쿼리 파라미터에서 토큰 안전하게 추출
token = st.query_params.get("token", [None])[0]

st.write("✅ 토큰 수신 여부:", token is not None)
st.write("📦 토큰 길이:", len(token) if token else 0)

def redirect_to(url: str):
    html(f"<script>window.top.location.href = '{url}';</script>", height=0)

if token:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        st.success("유효한 토큰입니다!")
        st.json(payload)
        base_url = st.experimental_get_url().split("?")[0]
        redirect_to(base_url)
    except jwt.ExpiredSignatureError:
        st.error("❌ 만료된 토큰입니다.")
        redirect_to(A_LOGIN_URL)
    except jwt.InvalidTokenError:
        st.error("❌ 유효하지 않은 토큰입니다.")
        redirect_to(A_LOGIN_URL)
else:
    st.warning("⚠️ 토큰이 없습니다.")
    redirect_to(A_LOGIN_URL)
