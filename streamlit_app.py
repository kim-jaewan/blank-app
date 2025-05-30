import streamlit as st
import streamlit.components.v1 as components
import base64
from Crypto.Cipher import AES
import jwt
from urllib.parse import unquote

JWT_SECRET= "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
APP_KEY = "base64:gEl/34nLR6mc2OhlbWsmZvu5rPVGWZLaDQinl/2GqhI="

def fix_padding(s: str) -> str:
    mod = len(s) % 4
    if mod == 1:
        # 길이 자체가 잘못된 경우
        raise ValueError("Invalid base64 string length: cannot be 1 mod 4")
    if mod in (2, 3):
        s += "=" * (4 - mod)
    return s


def decrypt_token_step_by_step(enc_b64, app_key):
    st.subheader("1️⃣ 원본 인코딩 토큰")
    st.code(enc_b64)

    # URL 디코딩
    enc_b64_unquoted = unquote(enc_b64)
    st.subheader("2️⃣ URL 디코딩 된 토큰")
    st.code(enc_b64_unquoted)

    # 패딩 보정
    enc_b64_padded = fix_padding(enc_b64_unquoted)
    st.subheader("3️⃣ Base64 패딩 보정")
    st.code(enc_b64_padded)

    # Base64 디코드 (raw = iv + ciphertext)
    raw = base64.urlsafe_b64decode(fix_padding(enc_b64_unquoted))
    st.subheader("4️⃣ Base64 디코딩 (raw bytes)")
    st.code(raw.hex(), language="plaintext")

    # IV / Ciphertext 분리
    iv = raw[:16]
    ct = raw[16:]
    st.subheader("5️⃣ IV (hex)")
    st.code(iv.hex())
    st.subheader("6️⃣ Ciphertext (hex)")
    st.code(ct.hex())

    # AES 복호화
    key = base64.b64decode(app_key.split(":",1)[1])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ct)
    st.subheader("7️⃣ 복호화된 원문 (decrypted raw bytes hex)")
    st.code(decrypted.hex())

    # 패딩 길이
    pad_len = decrypted[-1]
    st.subheader("8️⃣ 패딩 길이 (pad_len)")
    st.code(str(pad_len))

    # 패딩 제거 후 JWT
    jwt = decrypted[:-pad_len].decode("utf-8", errors="replace")
    st.subheader("9️⃣ 최종 JWT 문자열")
    st.code(jwt)

    return jwt

# --- Streamlit UI 시작 ---
params = st.query_params
raw_token = params.get("token", [None])
redirect_to = params.get("redirect_to", ["/"])[0]

st.title("🔐 SSO 토큰 디코딩 디버깅")

if not raw_token:
    st.error("❌ 토큰이 없습니다.")
    st.stop()

try:
    jwt_token = decrypt_token_step_by_step(raw_token, APP_KEY)

    # JWT 페이로드 JSON 파싱
    try:
        payload = jwt.decode(
            jwt_token,
            JWT_SECRET,
            algorithms=["HS256"],
            options={"require": ["exp"]},  
        )
        st.subheader("🔟 JWT Payload (검증 완료)")
        st.json(payload)
    except Exception:
        st.warning("⚠️ JWT가 JSON 포맷이 아닙니다.")

    # 실제 리디렉션 (디버깅 후에는 활성화)
    components.html(
    """
    <script>
      window.location.href = "/";
    </script>
    """,
    height=0,
)
except Exception as e:
    st.error(f"❌ 디코딩 과정 중 오류 발생: {e}")
