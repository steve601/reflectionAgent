# app.py
import streamlit as st
from graph import run_agent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Reflection Agent", page_icon="🤖")
st.title("🧠 Reflection Agent: Funny X Post Generator")

user_input = st.text_input("Enter a topic for a funny Twitter post:")

if st.button("Generate") and user_input:
    with st.spinner("Thinking..."):
        output = run_agent(user_input)
        st.subheader("📝 Initial Post")
        st.write(output.get("post", "No post generated."))

        st.subheader("🧠 Suggested Improvements")
        st.write(output.get("improvements", "No improvements generated."))

        st.subheader("✨ Final Revised Post")
        st.success(output.get("ans", "No final answer generated."))
