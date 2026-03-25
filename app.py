# 📦 Import tools
import streamlit as st
import requests
import json

# 🔑 Your Together API Key
api_key = "8332a4e7ca135b9a7be92e939a40830ad90dc4474a68cb1885bbc8afec736d44"  # Replace with your actual key

# 🧠 Initialize session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 App UI title
st.title("Chat with Me")

# 💬 Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 💡 User input
prompt = st.chat_input("Type your message...")

# ✅ When user sends a message
if prompt:
    # 1. Show user's message in chat
    st.chat_message("user").markdown(prompt)

    # 2. Add to session memory
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Prepare Together API call
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": st.session_state.messages,
        "max_tokens": 100,
        "temperature": 0.7
    }

    # 4. Send request to Together.ai
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # 5. Get assistant’s reply
    # 5. Get assistant’s reply (FIXED)
    st.write(response_json)

    if 'choices' in response_json and len(response_json['choices']) > 0:
        reply = response_json['choices'][0]['message']['content']
    else:
        reply = "⚠️ API Error: " + str(response_json)

    # 6. Show assistant’s reply in chat
    st.chat_message("assistant").markdown(reply)

    # 7. Save assistant’s reply to memory
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 8. 📝 Save to local file
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {prompt}\n")
        f.write(f"Assistant: {reply}\n\n")
