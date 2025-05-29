import streamlit as st
import jwt
from streamlit.components.v1 import html

JWT_SECRET = "y2KvwnjAMbv4dwrNl8uCRreJjF5Q60ptqK1w5X3AT/SxfJdIRb6TPIve7lAM85klcpWmod8TPNM9ePXS6Z4rkA=="
A_LOGIN_URL = "https://kitchen-portal.test/auth/login"

query_params = st.query_params
token = query_params.get("token")

if token:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        base_url = st.experimental_get_url().split("?")[0]
        html(f"<script>window.location.href='{base_url}';</script>", height=0)
    except jwt.ExpiredSignatureError:
        html(f"<script>window.location.href='{A_LOGIN_URL}';</script>", height=0)
    except jwt.InvalidTokenError:
        html(f"<script>window.location.href='{A_LOGIN_URL}';</script>", height=0)
else:
    html(f"<script>window.location.href='{A_LOGIN_URL}';</script>", height=0)
