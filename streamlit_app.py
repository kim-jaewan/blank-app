import streamlit as st
import jwt

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
JWT_ALGORITHM = "HS256"
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

query_params = st.query_params
token = query_params.get("token", [None])[0]

st.write("✅ 토큰 수신 여부:", token is not None)
st.write("📦 토큰 길이:", len(token) if token else "없음")
st.code(token or "None", language="text")

if token:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        st.success("✅ JWT 유효함")
        st.json(payload)
    except jwt.ExpiredSignatureError as e:
        st.error("⏰ 만료된 토큰")
        st.exception(e)
    except jwt.InvalidTokenError as e:
        st.error("❌ 유효하지 않은 토큰")
        st.exception(e)
else:
    st.warning("🚫 토큰 없음")
