import streamlit as st
import requests
import openai
from bs4 import BeautifulSoup
from collections import Counter
from PIL import Image

if 'message_list' not in st.session_state:
    st.session_state.message_list = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

if __name__ == "__main__":
    image = Image.open("pines.jpg")

    container = st.container()
    with container:
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image(image, width=100)
        with col2:
            st.markdown(f"""
            <style>
            .header {{
                text-align: center;
                color: #357b72;
                padding-top: 20px;
                margin-top: -40px; /* adjust the margin to align with the image */
            }}
            </style>
            """, unsafe_allow_html=True)
            st.markdown("<h1 class='header'>Pines International Academy Chatbot <br>  </h1>", unsafe_allow_html=True)

    # Scrape website content
    url = "https://pinesacademy.com/eng/index"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    website_content = soup.get_text()

    qa_dict = {}
    for sentence in website_content.split("."):
        sentence = sentence.strip()
        if sentence:
            words = sentence.split()
            key = " ".join(words[:5])
            qa_dict[key] = sentence

    chat_area = st.markdown(f"""
    <div style="overflow-y: auto; height: 300px; padding: 10px; border: 1px solid #ddd;">
    """, unsafe_allow_html=True)

    chat_history = ""
    for message in st.session_state.message_list:
        if message["role"] == "assistant":
            chat_history += f"<p><img src='https://cdn-icons-png.flaticon.com/512/1177/1177568.png' width='20' height='20'/> {message['content']}<br></p>\n"
        elif message["role"] == "user":
            chat_history += f"<p style='background-color: #f7f7f7; padding: 5px; border-radius: 10px;'><img src='https://cdn-icons-png.flaticon.com/512/1077/1077063.png' width='20' height='20'/> {message['content']}<br></p>\n"

    chat_area.markdown(chat_history, unsafe_allow_html=True)
    st.markdown(f"""
    </div>
    """, unsafe_allow_html=True)

with st.form("chat_form"):
    user_input = st.text_input("Ask a question", key="prompt")
    col1, col2 = st.columns([10, 2])
    with col1:
        clear_history = st.form_submit_button("Clear Chat History")
    with col2:
        send_button = st.form_submit_button("Send")

    if send_button or user_input:
        words = user_input.lower().split()
        word_count = len(words)
        keyword_count = 0
        for word in words:
            for key in qa_dict.keys():
                if word in key.lower().split():
                    keyword_count += 1
                    break
        if keyword_count / word_count >= 0.2:
            with st.spinner('Thinking...'):
                st.session_state.message_list.append({"role": "user", "content": user_input})
                for key, value in qa_dict.items():
                    if all(word in key.lower().split() for word in words):
                        st.session_state.message_list.append({"role": "assistant", "content": value})
                        break
                else:
                    # If no exact match, use the AI model to generate a response
                    client = openai.OpenAI(
                        base_url='http://localhost:11434/v1',
                        api_key='sk-proj-y96mIkXQE1t1Cdfefa2FT3BlbkFJ8XasSBLZE2KQo58SAAqm',  # api_key is required, but unused for local models
                    )
                    response = client.chat.completions.create(
                        model="llama3",
                        messages=st.session_state.message_list + [{"role": "user", "content": user_input}]
                    )
                    st.session_state.message_list.append({"role": "assistant", "content": response.choices[0].message.content})
        else:
            st.session_state.message_list.append({"role": "assistant", "content": "I didn't understand that. Please try rephrasing your question."})

        chat_history = ""
        for message in st.session_state.message_list:
                if message["role"] == "assistant":
                    chat_history += f"<p><img src='https://cdn-icons-png.flaticon.com/512/1177/1177568.png' width='20' height='20'/> {message['content']}<br></p>\n"
                elif message["role"] == "user":
                    chat_history += f"<p style='background-color: #f7f7f7; padding: 5px; border-radius: 10px;'><img src='https://cdn-icons-png.flaticon.com/512/1077/1077063.png' width='20' height='20'/> {message['content']}<br></p>\n"

        chat_area.markdown(chat_history, unsafe_allow_html=True)
        user_input = ""

if clear_history:
    st.session_state.message_list = [{"role": "system", "content": "You are a helpful assistant."}]
    st.experimental_rerun()