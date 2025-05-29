import streamlit as st
import requests
import base64
from Crypto.Cipher import AES

A_SITE_URL = "https://kitchen-portal.dev.amuz.kr/api/sso"
APP_KEY = "base64:gEl/34nLR6mc2OhlbWsmZvu5rPVGWZLaDQinl/2GqhI="

def decrypt_token(encrypted_token_b64, app_key_b64):
    key = base64.b64decode(app_key_b64.split(":")[1])
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

# ✅ 리스트에서 첫 값을 꺼냄
token_encrypted = st.query_params.get("token", [None])

if not token_encrypted:
    st.error("❌ 토큰 없음 – 인증 실패")
    st.stop()

try:
    jwt_token = decrypt_token(token_encrypted, APP_KEY)
except Exception as e:
    st.error(f"❌ 복호화 실패: {str(e)}")
    st.stop()

try:
    response = requests.post(
        A_SITE_URL,
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"redirect_to": "https://blank-app-2mgkkp65p39.streamlit.app"}
    )
    if response.status_code == 200:
        st.success("✅ 인증 성공: A에서 로그인 처리됨")
    else:
        st.error(f"❌ 인증 실패: {response.status_code}")
except Exception as e:
    st.error(f"❌ POST 실패: {str(e)}")
