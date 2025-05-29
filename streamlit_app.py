import streamlit as st
import base64
from Crypto.Cipher import AES
import json
from html import escape

APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="
DEBUG_MODE = True

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
redirect_to = params.get("redirect_to", ["/"])[0]
safe_redirect = escape(redirect_to, quote=True)

st.title("🔐 SSO 인증 처리 중...")

if not token_encrypted:
    st.error("❌ 토큰 없음 – 인증 실패")
    st.stop()

if DEBUG_MODE:
    st.subheader("🔒 Encrypted Token")
    st.code(token_encrypted)

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

st.success("✅ 인증 성공! 잠시 후 이동합니다.")
st.markdown(f"[👉 수동 이동하기]({safe_redirect})")

st.markdown(
    f"""
    <script>
        setTimeout(function() {{
            window.location.href = "{safe_redirect}";
        }}, 3000);
    </script>
    """,
    unsafe_allow_html=True
)
