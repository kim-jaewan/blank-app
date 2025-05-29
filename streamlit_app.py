import streamlit as st
import jwt

# JWT 시크릿키 (A 사이트와 동일하게)
JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
JWT_ALGORITHM = "HS256"

# A 사이트 로그인 URL
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

# 최신 방식으로 쿼리 파라미터 가져오기
query_params = st.query_params
token = query_params.get("token")

# 토큰이 있는 경우
if token:
    try:
        # 디코딩 및 검증
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # 유효한 경우: 토큰 제거 후 홈으로 새로고침
        st.query_params.clear()
        st.experimental_rerun()

    except jwt.ExpiredSignatureError:
        # 만료된 토큰
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)

    except jwt.InvalidTokenError:
        # 잘못된 토큰
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)

# 토큰이 없는 경우
else:
    st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
