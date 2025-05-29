# 새로 고침 후에도 query_params에 남아있을 경우 직접 redirect 처리
import streamlit as st
import jwt

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
JWT_ALGORITHM = "HS256"
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

query_params = st.query_params
token = query_params.get("token")

if token:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # 직접 URL을 바꿔주는 방식
        base_url = st.experimental_get_url().split("?")[0]
        st.markdown(f"<meta http-equiv='refresh' content='0;url={base_url}'>", unsafe_allow_html=True)

    except jwt.ExpiredSignatureError:
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
    except jwt.InvalidTokenError:
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
else:
    st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
