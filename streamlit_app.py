import streamlit as st
import requests
import base64
from Crypto.Cipher import AES

A_SITE_URL = "https://kitchen-portal.test/api/sso"
APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="

def get_aes_key(app_key_base64: str) -> bytes:
    return base64.b64decode(app_key_base64.split(":")[1])

def decrypt_laravel_token(encrypted_token_b64: str, app_key_b64: str) -> str:
    key = get_aes_key(app_key_b64)
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]

    # AES 복호화
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)

    # PKCS7 패딩 제거
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

# 토큰 추출
token_encrypted = st.query_params.get("token", [None])

if not token_encrypted or token_encrypted == "None":
    st.error("❌ URL에 토큰 없음 – 인증 실패")
    st.stop()

try:
    decrypted_jwt = decrypt_laravel_token(token_encrypted, APP_KEY)
    st.code(decrypted_jwt, language="text")
except Exception as e:
    st.error(f"❌ 복호화 실패: {str(e)}")
    st.stop()

# A 사이트에 인증 요청
try:
    response = requests.post(
        A_SITE_URL,
        headers={"Authorization": f"Bearer {decrypted_jwt}"}
    )
    if response.status_code == 200:
        user = response.json().get("user_data")
        st.success("✅ 인증 성공")
        st.json(user)
    else:
        st.error(f"❌ 인증 실패: {response.status_code}")
except Exception as e:
    st.error(f"❌ POST 실패: {str(e)}")
