import streamlit as st
import jwt
import webbrowser

from urllib.parse import urlencode

# JWT 비밀 키 (A 사이트와 동일하게 설정되어야 함)
JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
JWT_ALGORITHM = "HS256"

# 현재 URL에서 토큰 가져오기
query_params = st.experimental_get_query_params()
token = query_params.get("token", [None])[0]

# 현재 페이지의 base URL (토큰 제거용)
base_url = st.request.url.split('?')[0]

# 조건 분기
if not token:
    # 토큰 없으면 A 사이트 로그인 페이지로 리디렉션
    st.markdown("""
        <meta http-equiv="refresh" content="0; url='https://kitchen-portal.test/auth/login'" />
    """, unsafe_allow_html=True)

else:
    try:
        # 토큰 디코딩 (유효성 및 만료 검증 포함)
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_data = decoded.get("user_data", {})

        # 토큰 유효 → 홈으로 리디렉션 (토큰 제거된 URL)
        st.markdown(f"""
            <meta http-equiv="refresh" content="0; url='{base_url}'" />
        """, unsafe_allow_html=True)

    except jwt.ExpiredSignatureError:
        # 만료된 토큰 → A 로그인 페이지로
        st.markdown("""
            <meta http-equiv="refresh" content="0; url='https://kitchen-portal.test/auth/login'" />
        """, unsafe_allow_html=True)

    except jwt.InvalidTokenError:
        # 잘못된 토큰 → A 로그인 페이지로
        st.markdown("""
            <meta http-equiv="refresh" content="0; url='https://kitchen-portal.test/auth/login'" />
        """, unsafe_allow_html=True)
