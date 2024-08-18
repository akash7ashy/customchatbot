import streamlit as st

def homepage():
    st.title("Welcome to Your Custom Chatbot")

    st.markdown(
        """
        <style>
        .homepage-container {
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #fbc2eb, #a6c0fe);
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin: 50px;
        }
        .description {
            font-size: 1.2em;
            margin: 20px;
            color: #333;
        }
        .start-button {
            background-color: #007bff;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            border: none;
            font-size: 1.2em;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .start-button:hover {
            background-color: #0056b3;
        }
        .image {
            width: 100%;
            max-width: 600px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='homepage-container'>", unsafe_allow_html=True)
    st.markdown("<img src='https://via.placeholder.com/600x400.png' class='image' alt='Interactive Chatbot Interface'/>", unsafe_allow_html=True)
    st.markdown("<div class='description'>Welcome to the most interactive and intelligent chatbot! Click below to start your conversation.</div>", unsafe_allow_html=True)
    
    if st.button("Start Now"):
        st.session_state.page = "chatbot"
        st.experimental_rerun()  # Refresh the app to load the chatbot page

    st.markdown("</div>", unsafe_allow_html=True)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "homepage"

    if st.session_state.page == "homepage":
        homepage()
    elif st.session_state.page == "chatbot":
        from chatbot import chatbot_page
        chatbot_page()

if __name__ == "__main__":
    main()
