import streamlit as st
import jwt

# JWT 시크릿키 (A 사이트와 동일하게)
JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
JWT_ALGORITHM = "HS256"

# A 사이트 로그인 URL
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

# 최신 Streamlit 방식: 쿼리 파라미터 가져오기
query_params = st.query_params
token = query_params.get("token")

# 토큰 유무 확인
if token:
    try:
        # 디코드 및 검증
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # 토큰이 유효한 경우: URL에서 토큰 제거 (query 비우기)
        st.query_params.clear()
        st.experimental_rerun()

    except jwt.ExpiredSignatureError:
        # 만료된 토큰
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
    except jwt.InvalidTokenError:
        # 잘못된 토큰
        st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
else:
    # 토큰 없음: 로그인 페이지로 이동
    st.markdown(f"<meta http-equiv='refresh' content='0;url={A_LOGIN_URL}'>", unsafe_allow_html=True)
