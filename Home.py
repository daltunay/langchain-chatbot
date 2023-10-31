import streamlit as st

from utils.api_manager import APIKeyManager
from utils.logging import configure_logger
from utils.logo import generate_logo

logger = configure_logger(__file__)

st.set_page_config(page_title="chat-o-sophy", page_icon="💭", layout="wide")


def initialize_api_key_manager():
    if "api_key_manager" not in st.session_state:
        st.session_state.clear()
        st.session_state.api_key_manager = APIKeyManager()


initialize_api_key_manager()


def main():
    logger.info("Running home")
    st.session_state.api_key_manager.display()

    col1, col2 = st.columns(spec=[1, 0.5], gap="large")
    with col1:
        st.title("💭 chat-o-sophy", anchor=None)
        st.write(
            "[![source code](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/)"
        )
        st.header("Chat with your favorite philosophers!", divider="gray", anchor=False)
        st.markdown(
            """
        _chat-o-sophy_ lets you engage in enlightening conversations with famous philosophers.
        
        Choose from two modes:
        - **single mode**: have a one-on-one conversation with a chosen philosopher and explore their unique perspectives.
        - **multi mode**: ask a question and get answers from multiple philosophers, gaining a well-rounded perspective.
        """
        )

    st.header("How it works", anchor=False, divider="gray")
    _col1, _col2 = st.columns(2)
    with _col1:
        st.subheader("Single mode", anchor=False)
        st.markdown(
            """
            1. **Choose a philosopher**: Select from renowned philosophers.
            2. **Have them welcome you**: Read about their topics of interest.
            3. **Chat with them**: Start a conversation with anything you want.
            """
        )
    with _col2:
        st.subheader("Multi mode", anchor=False)
        st.markdown(
            """
            1. **Choose several philosophers**: Select from renowned philosophers.
            2. **Ask a question**: Ask about anything you want to learn about.
            3. **Receive responses**: Enjoy thought-provoking answers from them.
            """
        )

    st.header("About", anchor=False, divider="gray")
    st.markdown(
        """
        _chat-o-sophy_ harnesses the power of _Large Language Models_ (LLM) to allow you to chat with your favorite philosophers.  
        Using the OpenAI API, this app employs GPT-3.5 via the `langchain` library, as well as DALL·E image generator.
        """
    )

    with col2:
        logo = generate_logo()
        st.image(logo, use_column_width=True, caption="generated by DALL·E")
        st.button(
            label="Generate new logo",
            use_container_width=True,
            on_click=generate_logo.clear,
            help="How it works: https://openai.com/dall-e-2",
        )


if __name__ == "__main__":
    main()
