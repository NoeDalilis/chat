import streamlit as st
import replicate
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

# Replicate Credentials
with st.sidebar:
    st.title('Campus Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!',)
        else:
            st.success('Proceed to entering your prompt message!',)
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    return output

# Add a dictionary to store questions and answers
questions_answers = {

    "vision of Pines International Academy": "Pines International Academy has 4 visions: \n 1. English learning is a gateway toward international carrier person. \n"
    "2. Achieving greater english proficiency in a shorter time. \n"
    "3. No longer delaying overseas studies due to high costs. \n"
    "4. Distinctive learning programs at Pines International Academy.",

    "history of Pines": "**2001**: \n\n • Humble beginning of Pines Green Valley Campus. \n\n "
    "• Establishment of Pines International Academy in Baguio City, Philippines \n\n"
    "• TESDA Certification \n\n"
    "• SSP Certification by the Philippine Bureau of Immigration \n\n"
    "**2003** \n\n"
    "• Opening of various regular courses \n\n"
    "**2005**\n\n"
    "• Opening of Pines Cooyeesan Campus \n\n"
    "• Opening of Advanced Course Campus at Summer Place Hotel \n\n"
    "**2006** \n\n"
    "• Launch of Junior Camp \n\n"
    "• Expansion of Pines 4th flr.Cooyeesan Campus \n\n"
    "• Opening of Star Mountain Campus \n\n"
    "**2007** \n\n"
    "• Outstanding beginning of KIPILSUNG Program \n\n"
    "• Peak student count at 300 \n\n"
    "**2008** \n\n"
    "• Opening of Romel Suite Campus as a training center for students \n\n"
    "**2009** \n\n"
    "• Peak student count at 500 \n\n"
    "• Launch of WYM Camp for EFL Learners \n\n"
    "• Opening of Pines Clark Campus \n\n"
    "**2010** \n\n"
    "• Acting as an intermediary for University of Cordilleras and Sunmoon University \n\n"
    "• Launch of English Rush Hour Program \n\n"
    "• Hosting of the 1st ESLympics for Baguio university students \n\n"
    "• Program Launch for Korean University Students \n\n"
    "**2011** \n\n"
    "• Signing of MOU with University of Cordilleras \n\n"
    "• Signing of MOU with Yonam Digital Institute and College \n\n"
    "• Hosting of the 3rd ESLympics \n\n"
    "**2012**\n\n"
    "• Winter Vacation Camps for Hanyang University and Yonam Institute\n\n"
    "• Technology collaboration with Cheonam Yonam College, Kookje College, and Osan University\n\n"
    "• Successful hosting of the 4th ESLympics\n\n"
    "• Establishment of MOU with IVY Stewardess Academy\n\n"
    "• Celebration of the 100th Batch of Students\n\n"
    "**2013**\n\n"
    "• Opening of Chapis Advanced Course Campus\n\n"
    "• Launch of Choice Golf Academy`s Golf and English Camp\n\n"
    "**2014**\n\n"
    "• Summer Vacation Camps from Yonam College, Sunmoon University, Sunchonhyang University, Indook University, and Yamaguchi University\n\n"
    "• Launch of Intensive Sparta EFL Program\n\n"
    "• Successful hosting of the 6th ESLympics\n\n"
    "**2015**\n\n"
    "• Opening of Cebu Blue Ocean Academy (CBOA) sister school\n\n"
    "• Hosting of the 7th ESLympic\n\n"
    "**2016**\n\n"
    "• Successful hosting of the 8th ESLympics\n\n"
    "• Launch of University Students Chonbuk Buddy Program\n\n"
    "• Launch of University Students Inje Buddy Program\n\n"
    "• Conducting Summer & Winter Vacation Camps for juniors from Hanwha\n\n"
    "**2017**\n\n"
    "• Winter Vacation Camps from Chonbuk University, Sunmoon University, Kyeongnam National University, Inje University, and Daejin University\n\n"
    "• Winter Vacation Camp for juniors from Hanwha\n\n"
    "**2018**\n\n"
    "• Opening of the Main Campus\n\n"
    "• Registration of students from seven major Korean Universities\n\n"
    "• Successful hosting of winter and summer junior camps\n\n"
    "• Hosting of the 8th ESLympics\n\n"
    "**2019**\n\n"
    "• Participation in the Indonesian World Education Expo 2019\n\n"
    "• Recipient of the Galing TVI Award from TESDA\n\n"
    "• Recognition for the school`s contribution to language training\n\n"
    "• Acknowledgment by the British Council as a top-performing test partner (2018-2019)\n\n"
    "• Conducting Department of Tourism`s inter-school familiarization tours\n\n"
    "• Collaboration with renowned bloggers and YouTubers\n\n"
    "• Promotion of Baguio as an education destination\n\n"
    "• Modernization of Chapis accommodations\n\n"
    "• Hosting the inaugural Taiwanese Global English Camp\n\n"
    "• Korean Internship programs with the Department of Tourism, Philippine Information Agency, and Baguio City Mayor`s Office\n\n"
    "**2020**\n\n"
    "• Temporary closure of offline classes due to Covid-19\n\n"
    "• Hosting of the Korean Global Junior Camp\n\n"
    "• Organization of language training for Gyeongnam University\n\n"
    "• Organization of language training for Hanseo University\n\n"
    "**2021**\n\n"
    "• Development of the 11talk 4-step learning system\n\n"
    "• Introduction of the IELTS Training Program\n\n"
    "• Training of additional teachers for online teaching\n\n"
    "• Collaboration programs with the Department of Tourism\n\n"
    "• Collaboration programs with the Philippine Information Agency\n\n"
    "**2022**\n\n"
    "• Establishment of Pines English Center Japan\n\n"
    "• Name change from Chapis to Test Campus\n\n"
    "• Name change from Main to Speaking Campus\n\n"
    "• Maintenance of 200 Online Teachers\n\n"
    "• Summer Camp for Mongolian Juniors\n\n"
    "• Upgradation of Pines Portal features\n\n"
    "• Reopening of Pines International Academy\n\n"
    "• Reopening of Cebu Blue Ocean Academy\n\n"
    "• Sharing academy updates with BESA\n\n"
    "• Resumption of face-to-face classes in March\n\n"
    "• Language training for Gyeongnam University\n\n"
    "• Language training for Daejin University\n\n"
    "• Language training for Hanseo University\n\n"
    "**2023**\n\n"
    "• Opening of the IELTS Guarantee 7.0 Course\n\n"
    "• Signing of MOU with Easter College\n\n"
    "• Launch of Pines IELTS Specialized Campus\n\n"
    "• Integration of Pines Family Course Launch\n\n"
    "• Implementation of Mandatory Enhanced Spartan Programn\n",

    "Why does Pines have CEFR?\n\n": "To provide quality English Education.\n\n"
    "To further strengthen the teaching-learning process and produce good results.\n\n"
    "To have specific and measurable objectives in each class through target goals.\n\n"
    "To avoid wasting time in achieving a certain English proficiency level.",

    "Pines ESL Curriculum": "Sparta Speaking Program/Power ESL\n\n"
    "Intensive ESL\n\n"
    "Premium ESL",

    "What will be Given to students when they graduate": "A report card will be given to the student when he/she graduates. It contains the following:\n\n"
    "General information about the student\n\n"
    "Pines test score (PEPT)\n\n"
    "CEFR Equivalent of the PEPT\n\n"
    "Score meter of PEPT",

    "who are the Partners of Pines": "TESDA\n\n"
    "Bureau of Immigration\n\n"
    "Department of Tourism\n\n"
    "Security and Exchange Commission\n\n"
    "Baguio City Hall\n\n"
    "**Schools**\n\n"
    "Easter College\n\n"
    "British Council IELTS\n\n"
    "ETS TOEIC\n\n"

    "**Academy**\n\n"
    "11Talk\n\n"
    "Cebu Blue Ocean\n\n"
    "Pines Portal",

    "what is power speaking": "Power Speaking, also known as the “Spartan Speaking” program, is an upgraded version of General ESL."
    "It is ideal for all students from beginner to advanced levels. This program has a balanced distribution of 4on1 and 1on1 classes. "
    "It exposes students to the real English language and provides maximum opportunities for students to use authentic English in speaking, listening, reading, and writing."
    "This program follows many approaches to achieving its goals. However, the Communicative Language Teaching (CLT) approach is mainly used."
    "CLT gives students real life communication lessons which are more fun, more useful, and more relevant to real world situations rather than in the classroom.",

    "what is the program structure of Pines": "**Regular Class (8)** \n\n"
    "1:1 class (4 sessions)\n\n"
    "4:1 class (4 sessions)\n\n"
    "**Elective Class (3)**\n\n"
    "Morning Class(1 session)\n\n"
    "Evening Class(2 sessions)\n\n"
    "\n\n"
    "Catering to students from Levels 1-10 (Beginner to Advanced Levels)\n\n"
    "Preparatory ESL course for test module courses\n\n"
    "A total of 8 interactive regular 1on1 and 4on1 classes with different teachers\n\n"
    "Systematic classes based on a curriculum which is a product of more than 17 years of operation\n\n"
    "If group class is not available, 2 4:1 classes will be changed to 1 1:1 class.",

}
# Function to generate response to user's question
def generate_response(prompt_input):
    prompt_input = prompt_input.lower()
    for question, answer in questions_answers.items():
        keywords = question.lower().split()
        matches = sum(1 for keyword in keywords if keyword in prompt_input.split())
        if matches / len(keywords) >= 0.6:
            return answer
    return generate_llama2_response(prompt_input)

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
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
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)