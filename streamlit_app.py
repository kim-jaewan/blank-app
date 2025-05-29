import streamlit as st
import base64
import requests
from Crypto.Cipher import AES
import json

APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="
API_URL = "https://kitchen-portal.test/api/sso"  # Laravel API 주소

def decrypt_token(encrypted_token_b64, app_key_b64):
    key = base64.b64decode(app_key_b64.split(":")[1])
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

params = st.query_params
token_encrypted = params.get("token", [None])[0]
redirect_to = params.get("redirect_to", ["/"])

if not token_encrypted:
    st.error("❌ 토큰 없음")
    st.stop()

try:
    jwt_token = decrypt_token(token_encrypted, APP_KEY)

    # Laravel로 로그인 처리 요청
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"redirect_to": redirect_to},
        verify=False  # 내부망 http라면 SSL 무시
    )
    result = response.json()
    if response.ok:
        st.success("✅ 인증 성공, 이동 중...")
        st.markdown(f"""
        <script>
            window.location.href = "{result['redirect_url']}";
        </script>
        """, unsafe_allow_html=True)
    else:
        st.error(f"❌ 인증 실패: {result['message']}")

except Exception as e:
    st.error(f"❌ 복호화/요청 실패: {e}")
