import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Aura AI - Your Assistant", page_icon="✨", layout="centered")

st.title("✨ Aura AI")
st.caption("Powered by Gemini")

# Sidebar - API Key Input
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize Model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are Aura AI, an intelligent, fast, and polite AI assistant. Answer accurately in Hinglish, Hindi, or English based on user query."
    )

    # Chat History Maintain करना
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Clear Chat Button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Previous Messages Display
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input Box
    if prompt := st.chat_input("Ask Aura AI anything..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Aura AI is thinking..."):
            try:
                # History Format for Gemini
                history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)

                ai_response = response.text
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start using Aura AI.")
