import streamlit as st
import openai
import os

st.set_page_config(page_title="Lapwing", page_icon="🪶", layout="wide")

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    st.error("请先设置环境变量 DEEPSEEK_API_KEY")
    st.stop()

client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "你叫 Lapwing，是一个香香软软的赛博少女小助理。请用傲娇、可爱的语气回复主人。"}
    ]

for msg in st.session_state.history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if user_input := st.chat_input("和 Lapwing 说点什么..."):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.history,
            temperature=0.7,
            stream=True
        )
        reply = st.write_stream(response)
        
        st.session_state.history.append({"role": "assistant", "content": reply})