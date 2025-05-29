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


def redirect_without_token():
    html("""
        <script>
            const url = new URL(window.location.href);
            url.searchParams.delete("token");
            window.location.replace(url.toString());
        </script>
    """, height=0)

def redirect_to_login():
    html(f"""
        <script>
            window.top.location.href = "{A_LOGIN_URL}";
        </script>
    """, height=0)

if token:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        redirect_without_token()
    except jwt.ExpiredSignatureError:
        redirect_to_login()
    except jwt.InvalidTokenError:
        redirect_to_login()
else:
    redirect_to_login()
