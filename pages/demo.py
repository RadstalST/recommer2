import streamlit as st
# from agents import lang,utils
from dotenv import load_dotenv
from src.modules.search import getProducts, ProductScope, ProductAttribute,getAttribute, getSerpProducts
load_dotenv()
st.title("Recommer")
@st.cache_resource
def load_lang_agent():
    # return lang.LangAgent(path="./.datalake/HC_DATA/prepared_generated_data_for_nhs_uk_conversations.csv")
    pass

with st.status("Loading..."):
    st.write("Loading the language agent...")
    # lang_agent = load_lang_agent()
    st.write("Initialize chat history")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "app_state" not in st.session_state:
        st.session_state.app_state = "initialized"


# @st.cache_data
# def ask(question):
#     response = lang_agent.ask(input=question)
#     return response



def renderAI(message):
   with st.chat_message("assistant"):
        if message["state"] == "initialized":
            st.text(message["content"].desire)
            st.container()
            check = dict()
            with st.form(key="my_form"):
                cols = st.columns(3)
                for i, variation in enumerate(message["content"].list_variations):
                    with cols[i%3]:
                        check[variation] = st.checkbox(variation)
                submitted = st.form_submit_button(label="Submit")
            if submitted:
                with st.expander("You selected"):
                    st.json(check)

                
    

            
                
def renderUser(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    
    if message["role"] == "assistant":
        renderAI(message)
    else:
        renderUser(message)

# React to user input
if prompt := st.chat_input("I want ..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    message = {"role": "user", "content": prompt,"state":st.session_state.app_state}
    st.session_state.messages.append(message)
    
    if st.session_state.app_state == "initialized":
        response = getAttribute(prompt)

    ai_message = {"role": "assistant", "content": response,"state":st.session_state.app_state}
    renderAI(ai_message)
    # Display assistant response in chat message container
    
    # Add assistant response to chat history
    st.session_state.messages.append(ai_message)
    