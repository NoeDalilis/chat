import streamlit as st
import openai
import os

# App title
st.set_page_config(page_title="Pines International Academy Chatbot")

# Add a header with a logo
header_cols = st.columns([1, 4])  # adjust the column widths as needed
with header_cols[0]:
    logo_image = "pines.jpg"  # replace with your logo image file
    st.image(logo_image, width=100)  # adjust the width as needed
with header_cols[1]:
    st.markdown("<h1 style='margin-top: -20px; color: #3e7f7f;'>Pines International Academy Chatbot</h1>", unsafe_allow_html=True)

# OpenAI Credentials
with st.sidebar:
    st.title('Campus Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter OpenAI API key:', type='password')
        if not openai_api_key:
            st.warning('Please enter your OpenAI API key!',)
        else:
            st.success('Proceed to entering your prompt message!',)
    openai.api_key = openai_api_key

    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a model', ['gpt-3.5-turbo', 'text-curie-001', 'text-babbage-001'], key='selected_model')

    temperature = st.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('max_length', min_value=64, max_value=4096, value=512, step=8)

# Store OpenAI generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating OpenAI response
def generate_openai_response(prompt_input):
    response = openai.Completion.create(
        engine=selected_model,
        prompt=prompt_input,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_length,
        stop=None
    )
    return response.choices[0].text

# Add a dictionary to store questions and answers
questions_answers = {
    # add your questions and answers here
}

# Function to generate response to user's question
def generate_response(prompt_input):
    prompt_input = prompt_input.lower()
    for question, answer in questions_answers.items():
        keywords = question.lower().split()
        matches = sum(1 for keyword in keywords if keyword in prompt_input.split())
        if matches / len(keywords) >= 0.6:
            return answer
    return generate_openai_response(prompt_input)

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"]!= "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            full_response += response
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    #aaaa