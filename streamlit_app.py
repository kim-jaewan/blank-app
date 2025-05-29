import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "..."  # 실제 시크릿 키 입력
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
    html(f"<script>window.location.href = '{A_LOGIN_URL}';</script>", height=0)

if token:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        st.success("✅ 유효한 토큰입니다.")
        st.json(payload)
        redirect_without_token()
    except jwt.ExpiredSignatureError:
        st.error("❌ 만료된 토큰입니다.")
        redirect_to_login()
    except jwt.InvalidTokenError:
        st.error("❌ 유효하지 않은 토큰입니다.")
        redirect_to_login()
else:
    st.warning("⚠️ 토큰이 없습니다.")
    redirect_to_login()
