import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

token = st.query_params.get("token", [None])
token = token[0] if isinstance(token, list) else token

st.write("✅ 토큰:", token)
st.write("✅ 수신 여부:", token is not None)
st.write("📦 길이:", len(token) if token else 0)


def redirect_to(url: str):
    html(f"""
        <meta http-equiv="refresh" content="0;url={url}">
    """, height=0)

if token:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # 토큰 제거 후 리디렉션
        current_url = st.experimental_get_query_params()
        base_url = st.experimental_get_url().split("?")[0]
        redirect_to(base_url)
    except jwt.ExpiredSignatureError:
        redirect_to(A_LOGIN_URL)
    except jwt.InvalidTokenError:
        redirect_to(A_LOGIN_URL)
else:
    redirect_to(A_LOGIN_URL)
