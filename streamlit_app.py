import streamlit as st
import requests
import base64
from Crypto.Cipher import AES
import json

# 🔐 설정
APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="
DEBUG_MODE = True

# 🔓 복호화 함수
def decrypt_token(encrypted_token_b64, app_key_b64):
    key = base64.b64decode(app_key_b64.split(":")[1])
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

# ✅ Query 파라미터 추출
params = st.query_params
token_encrypted = params.get("token", [None])[0]
redirect_to = params.get("redirect_to", ["/"])[0]  # 옵션: A에서 redirect_to도 함께 넘겼을 경우

st.title("🔐 SSO 인증 처리 중...")

if not token_encrypted:
    st.error("❌ 토큰 없음 – 인증 실패")
    st.stop()

# 🔍 토큰 출력
if DEBUG_MODE:
    st.subheader("🔒 Encrypted Token")
    st.code(token_encrypted)

# 🔓 복호화
try:
    jwt_token = decrypt_token(token_encrypted, APP_KEY)

    if DEBUG_MODE:
        st.subheader("🔓 Decrypted JWT")
        st.code(jwt_token)
        try:
            payload = json.loads(jwt_token)
            st.subheader("🧾 JWT Payload")
            st.json(payload)
        except:
            st.warning("⚠️ JSON 파싱 실패")
except Exception as e:
    st.error(f"❌ 복호화 실패: {str(e)}")
    st.stop()

# ✅ 인증 성공 처리
st.success("✅ 인증 성공! 잠시 후 이동합니다.")
st.markdown(f"[👉 수동 이동하기]({redirect_to})")

# 🔄 ✅ <meta> 대신 <script> 사용한 리디렉션
st.markdown(
    f"""
    <script>
        setTimeout(function() {{
            window.location.href = "{redirect_to}";
        }}, 3000);
    </script>
    """,
    unsafe_allow_html=True
)

)
