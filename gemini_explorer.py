import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "my-project-19409-radicalai"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)
# Load model with config
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

# Helper function to display and send streamlit messages


def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    output = f"{output}"

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
           "role": "user",
           "content": query
        }
     )

    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )


st.title("Gemini Explorer")


# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history and handle user input
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
    )
    if index > 0:  # Skip displaying the initial prompt (index 0)
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    chat.history.append(content)

if len(st.session_state.messages) == 0:
    st.session_state.user_name = st.text_input("Please enter your name")


if len(st.session_state.messages) == 0 and st.session_state.user_name:
    initial_prompt = f"Introduce yourself as ReX, an assistant powered by Google Gemini.use emojis.address the user with his name {st.session_state.user_name}"
    llm_function(chat, initial_prompt)  # Process initial prompt without adding to history

# For capturing user input
query = st.chat_input("Gemini Explorer")


if query and st.session_state.user_name:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
elif query and not st.session_state.user_name:
    with st.chat_message("model"):
        st.markdown("please enter your name in the box above")

# executed git push -u origin main --force
# testing the latest changes
# recording loom video


