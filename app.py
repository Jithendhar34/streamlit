import streamlit as st
from openai import OpenAI
import os

# ✅ Load API key (works for both local & Streamlit Cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load from .env if present
except ImportError:
    pass

# First check Streamlit secrets, then fallback to .env
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("❌ No API key found. Please set OPENAI_API_KEY in Streamlit Secrets or .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="🤖 Chatbot", page_icon="🤖")
st.title("⚡ GPT-4o-mini Chatbot")

# Store conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
