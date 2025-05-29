import streamlit as st
import requests
import base64
from Crypto.Cipher import AES
import json

# 🔐 설정
A_SITE_URL = "https://kitchen-portal.dev.amuz.kr/api/sso"
APP_KEY = "base64:X06Qj5yQdp+WViPbjbvdWLcCvHz0lBvoCEGkT6mxmGM="
DEBUG_MODE = True  # 배포 시 False로 전환

# 🔓 복호화 함수
def decrypt_token(encrypted_token_b64, app_key_b64):
    key = base64.b64decode(app_key_b64.split(":")[1])
    raw = base64.b64decode(encrypted_token_b64)
    iv, encrypted = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")

# ✅ Query 파라미터에서 token 추출
token_encrypted = st.query_params.get("token", [None])

st.title("🔐 SSO 인증 처리 중...")

if not token_encrypted:
    st.error("❌ 토큰 없음 – 인증 실패")
    st.stop()

# 🔍 디버그용: 암호화된 토큰 출력
if DEBUG_MODE:
    st.subheader("🔒 Encrypted Token (Base64)")
    st.code(token_encrypted, language="text")

# 🔓 복호화 → JWT
try:
    jwt_token = decrypt_token(token_encrypted, APP_KEY)

    if DEBUG_MODE:
        st.subheader("🔓 Decrypted JWT")
        st.code(jwt_token, language="text")

        try:
            jwt_json = json.loads(jwt_token)
            st.subheader("🧾 Token Payload (parsed)")
            st.json(jwt_json)
        except:
            st.warning("⚠️ JWT JSON 파싱 실패")
except Exception as e:
    st.error(f"❌ 복호화 실패: {str(e)}")
    st.stop()

# 📡 A 서버에 POST 요청
try:
    response = requests.post(
        A_SITE_URL,
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={}  # redirect_to 없이 보내도 A에서 처리
    )

    st.subheader("📡 A 서버 응답")
    if response.status_code == 200:
        data = response.json()
        redirect_url = data.get("redirect_url", "/")
        st.success("✅ 인증 성공! 잠시 후 이동합니다.")
        st.markdown(f"[👉 수동 이동]({redirect_url})")

        # 🔄 3초 후 자동 리다이렉트
        st.markdown(
            f"""<meta http-equiv="refresh" content="3;url={redirect_url}" />""",
            unsafe_allow_html=True
        )
    else:
        st.error(f"❌ 인증 실패: {response.status_code}")
        st.code(response.text)
except Exception as e:
    st.error(f"❌ A 서버 요청 실패: {str(e)}")
