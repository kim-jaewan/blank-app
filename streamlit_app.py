import streamlit as st
import requests
import base64
from Crypto.Cipher import AES
import json

A_SITE_URL = "https://kitchen-portal.dev.amuz.kr/api/sso"
APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="

def decrypt_token(encrypted_token_b64, app_key_b64):
    key = base64.b64decode(app_key_b64.split(":")[1])
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

# ✅ 리스트에서 첫 번째 값만 추출해야 복호화 가능
token_encrypted = st.query_params.get("token", [None])[0]

# 🔎 토큰 표시
st.subheader("🔐 Encrypted Token (Base64)")
st.code(token_encrypted or "None", language="text")

st.success("로그인 완료! 잠시 후 자동 이동합니다.")
st.markdown("Redirecting...")

st.experimental_rerun()
if not token_encrypted:
    st.error("❌ 토큰 없음 – 인증 실패")
    st.stop()

# 🔓 복호화
try:
    jwt_token = decrypt_token(token_encrypted, APP_KEY)
    st.subheader("🔓 Decrypted JWT")
    st.code(jwt_token, language="text")
except Exception as e:
    st.error(f"❌ 복호화 실패: {str(e)}")
    st.stop()

# ✅ A 서버에 POST 요청
try:
    response = requests.post(
        A_SITE_URL,
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"redirect_to": "https://blank-app-2mgkkp65p39.streamlit.app"}
    )
    st.subheader("📡 A 사이트 인증 응답")
    if response.status_code == 200:
        st.success("✅ 인증 성공: A에서 로그인 처리됨")
        try:
            st.json(response.json())
        except:
            st.code(response.text)
    else:
        st.error(f"❌ 인증 실패: {response.status_code}")
        st.code(response.text)
except Exception as e:
    st.error(f"❌ POST 실패: {str(e)}")
