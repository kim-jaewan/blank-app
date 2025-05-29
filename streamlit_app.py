import streamlit as st
import requests

# 받은 토큰
token = st.query_params.get("token", [None])[0]

if not token:
    st.error("토큰 없음 – 인증 실패")
    st.stop()

# A 사이트로 POST 요청
response = requests.post(
    "http://kip.lge.com/api/sso",
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 200:
    user = response.json().get("user_data")
    st.success("인증 성공")
    st.json(user)
else:
    st.error("인증 실패 – 로그인 다시 시도")
