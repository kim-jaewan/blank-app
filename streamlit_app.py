import streamlit as st
import requests
import base64
from Crypto.Cipher import AES

# ------------------------
# 설정
# ------------------------
A_SITE_URL = "http://kip.lge.com/api/sso"
JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="  # A 사이트 JWT 검증용
APP_KEY = "base64:gEl/34nLR6mc2OhlbWsmZvu5rPVGWZLaDQinl/2GqhI="  # A 사이트 Laravel의 .env의 APP_KEY 값 (base64: 로 시작)

# ------------------------
# Laravel AES 복호화 함수
# ------------------------
def get_aes_key(app_key_base64):
    return base64.b64decode(app_key_base64.split(":")[1])

def decrypt_laravel_token(encrypted_token_b64: str, app_key_b64: str) -> str:
    key = get_aes_key(app_key_b64)
    raw = base64.b64decode(encrypted_token_b64)
    iv = raw[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(raw[16:])
    padding_len = decrypted[-1]
    return decrypted[:-padding_len].decode("utf-8")

# ------------------------
# 토큰 추출 및 복호화
# ------------------------
token_encrypted = st.query_params.get("token", [None])

if not token_encrypted or token_encrypted == "None":
    st.error("❌ URL에 토큰 없음 – 인증 실패")
    st.stop()

try:
    decrypted_jwt = decrypt_laravel_token(token_encrypted, APP_KEY)
    st.code(decrypted_jwt, language="text")
except Exception as e:
    st.error(f"❌ 토큰 복호화 실패: {str(e)}")
    st.stop()

# ------------------------
# A 사이트로 POST (JWT 인증)
# ------------------------
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
    st.error(f"❌ POST 요청 실패: {str(e)}")
