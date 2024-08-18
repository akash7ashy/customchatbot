import json
import streamlit as st
from difflib import get_close_matches
from datetime import datetime
import time

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def add_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: linear-gradient(135deg, #fbc2eb, #a6c0fe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        @keyframes gradient {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }
        .chat-header {
            background: linear-gradient(135deg, #a6c0fe, #fbc2eb);
            color: white;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-size: 1.5em;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        }
        .chat-bubble {
            max-width: 75%;
            padding: 10px;
            border-radius: 20px;
            margin: 5px 0;
            color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            position: relative;
            transition: background-color 0.3s, transform 0.3s;
        }
        .user-bubble {
            background-color: #007bff;
            align-self: flex-end;
        }
        .user-bubble:hover {
            background-color: #0056b3;
            transform: scale(1.02);
        }
        .bot-bubble {
            background-color: #28a745;
            align-self: flex-start;
        }
        .bot-bubble:hover {
            background-color: #1e7e34;
            transform: scale(1.02);
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            padding: 20px;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            max-height: 70vh;
            overflow-y: auto;
            scroll-behavior: smooth;
            margin: 10px;
        }
        .timestamp {
            font-size: 0.8em;
            color: gray;
            margin-top: -10px;
            margin-bottom: 10px;
        }
        .chat-input {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 10px;
        }
        .chat-input textarea {
            width: 80%;
            padding: 10px;
            border-radius: 20px;
            border: 1px solid #ccc;
            resize: none;
            transition: border-color 0.3s;
        }
        .chat-input textarea:focus {
            border-color: #007bff;
            outline: none;
        }
        .chat-input button {
            width: 15%;
            padding: 10px;
            border-radius: 20px;
            border: none;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .chat-input button:hover {
            background-color: #0056b3;
        }
        .loading {
            border: 4px solid #f3f3f3;
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 20px;
            height: 20px;
            -webkit-animation: spin 2s linear infinite;
            animation: spin 2s linear infinite;
            margin-left: 10px;
        }
        @-webkit-keyframes spin {
            0% { -webkit-transform: rotate(0deg); }
            100% { -webkit-transform: rotate(360deg); }
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.markdown(
        """
        <div class='chat-header'>
            Custom Chatbot
        </div>
        """,
        unsafe_allow_html=True
    )
    add_custom_css()

    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'loading' not in st.session_state:
        st.session_state.loading = False

    # Sidebar for conversation history
    with st.sidebar:
        st.markdown("## Conversation History")
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                st.markdown(f"{message}")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message.startswith("You:"):
                st.markdown(f"<div class='chat-bubble user-bubble'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble bot-bubble'>{message}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='timestamp'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # New input area for each question
    user_input = st.text_area("You: ", key="new_input", height=50)

    if st.button("Send", key="send_button"):
        if user_input:
            st.session_state.chat_history.append(f"You: {user_input}")
            st.session_state.loading = True
            st.experimental_rerun()

    if st.session_state.loading:
        with chat_container:
            st.markdown("<div class='chat-bubble bot-bubble'><div class='loading'></div></div>", unsafe_allow_html=True)
        time.sleep(2)  # Simulate thinking time

        best_match: str | None = find_best_match(st.session_state.new_input, [q['question'] for q in knowledge_base['questions']])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
        else:
            answer = "I don't know the answer. Can you teach me?"
            new_answer: str = st.text_area("Type the answer or 'skip' to skip: ", key="new_answer")
            if st.button("Submit", key="submit_button"):
                if new_answer:
                    if new_answer.lower() != 'skip':
                        knowledge_base["questions"].append({"question": st.session_state.new_input, "answer": new_answer})
                        save_knowledge_base('knowledge_base.json', knowledge_base)
                        answer = "Thank you! I learned a new response!"
                    else:
                        answer = "Skipped learning new response."

        st.session_state.chat_history.append(f"Bot: {answer}")
        st.session_state.loading = False
        st.experimental_rerun()  # Refresh the page to clear the text field

if __name__ == "__main__":
    main()
