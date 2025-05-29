import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

# query_params는 딕셔너리지만 내부값이 리스트이므로 [0]으로 가져옴
query_params = st.query_params
token = query_params.get("token", [None])[0]

def redirect_to(url: str):
    html(f"""
        <script>
            window.parent.location.href = "{url}";
        </script>
    """, height=0)

if token:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        base_url = st.experimental_get_url().split("?")[0]
        redirect_to(base_url)
    except jwt.ExpiredSignatureError:
        redirect_to(A_LOGIN_URL)
    except jwt.InvalidTokenError:
        redirect_to(A_LOGIN_URL)
else:
    redirect_to(A_LOGIN_URL)
