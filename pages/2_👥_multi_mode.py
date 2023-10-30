import streamlit as st

from chatbot import AssistantChatbot, PhilosopherChatbot
from utils.logging import configure_logger

logger = configure_logger(__file__)

st.set_page_config(page_title="chat-o-sophy", page_icon="💭")


PHILOSOPHERS = [
    "Plato",
    "Aristotle",
    "Socrates",
    "Confucius",
    "Immanuel Kant",
    "René Descartes",
    "David Hume",
    "John Locke",
    "Friedrich Nietzsche",
    "Thomas Aquinas",
    "Jean-Jacques Rousseau",
    "Baruch Spinoza",
    "Ludwig Wittgenstein",
    "Søren Kierkegaard",
    "Voltaire",
    "John Stuart Mill",
    "Karl Marx",
    "George Berkeley",
    "Arthur Schopenhauer",
    "G.W.F. Hegel",
]


@st.cache_resource
def initialize_multi_mode():
    logger.info("Initializing multi mode")
    multi_mode = {
        "header_container": st.empty(),
        "current_choices": [],
        "history": [],
    }

    return multi_mode


st.session_state.multi_mode = initialize_multi_mode()


def main():
    logger.info("Running multi mode")

    if api_key_manager := st.session_state.get("api_key_manager"):
        api_key_manager.display_api_form()

    with st.session_state.multi_mode["header_container"].container():
        st.title("Multi mode", anchor=False)
        st.caption("Ask a question to several philosophers!")

        st.session_state.multi_mode["current_choices"] = st.multiselect(
            label="Philosophers:",
            placeholder="Choose several philosophers",
            options=PHILOSOPHERS,
            max_selections=5,
            default=None,
            disabled=st.session_state.get("OPENAI_API_KEY") is None,
        )

    if prompt := st.chat_input(
        placeholder="What is your question?",
        disabled=not (
            st.session_state.multi_mode["current_choices"]
            and st.session_state.get("OPENAI_API_KEY")
        ),
    ):
        history = st.session_state.multi_mode["history"]
        history.append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)
        for philosopher in st.session_state.multi_mode["current_choices"]:
            st.header(philosopher, divider="gray", anchor=False)
            chatbot = PhilosopherChatbot(philosopher)
            with st.chat_message("ai"):
                answer = chatbot.chat(prompt=prompt)
                history.append({"role": philosopher, "content": answer})

        st.divider()
        st.header("Summary", anchor=False, help="Generated by an AI assistant.")
        assistant = AssistantChatbot(history)
        assistant.summarize_responses()
        with st.spinner("Generating summary table..."):
            assistant.create_markdown_table()


if __name__ == "__main__":
    main()
