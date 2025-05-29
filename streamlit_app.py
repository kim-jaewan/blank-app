import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

query_params = st.query_params
token = query_params.get("token", [None])[0]

# 디버깅 로그
st.write("토큰 있음?", token is not None)
st.write("토큰 값:", token)

def redirect_to(url: str):
    html(f"""
        <script>
            window.top.location.href = "{url}";
        </script>
    """, height=0)

if token:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        st.write("JWT payload:", payload)
        base_url = st.experimental_get_url().split("?")[0]
        redirect_to(base_url)
    except jwt.ExpiredSignatureError as e:
        st.error("만료된 토큰입니다.")
        redirect_to(A_LOGIN_URL)
    except jwt.InvalidTokenError as e:
        st.error("유효하지 않은 토큰입니다.")
        redirect_to(A_LOGIN_URL)
else:
    st.warning("토큰이 없습니다.")
    redirect_to(A_LOGIN_URL)
