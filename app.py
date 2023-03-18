import openai
import streamlit as st

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n\n".join(messages_str)), height=400)

BASE_PROMPT = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": "对于提问的语言，你将偏向相同的语言的文化思维进行回答."},
    {"role": "system", "content": "适当多给出一些建议."}
]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.subheader("ChatGPT @OneSun Personal Public Platform")

openai.api_key = st.text_input("Paste your OpenAI Key here",value="", type ="password")
prompt = st.text_input("Prompt",value = "Enter your message here...")


if st.button("Send"):
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"],
            temperature =1,
            max_tokens=1000,
            top_p=1.0,
            n=1,
            presence_penalty=0,
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system","content": message_response}
        ]
if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT

text = st.empty()
show_messages(text)