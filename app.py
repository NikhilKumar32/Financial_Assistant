# Import necessary libraries to use their functions
import os
import streamlit as st
from openai import OpenAI

# Get the API key from the environment settings

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now retrieve the API key
api_key_nvidia = os.getenv("api_key_nvidia")

api_key_nvidia = os.environ.get("api_key_nvidia")

# If there is no API key, show an error message and stop the program
if not api_key_nvidia:
    st.error("NVIDIA API key not found. Please set the `api_key_nvidia` environment variable.")
    st.stop()

# Add custom design for a finance theme
st.markdown("""
<style>
/* Set background color for the main section */
.main {
    background-color: #f4f9f9; /* Light teal for a professional look */
    color: #000000; /* Black text for readability */
}
/* Set background color for the sidebar */
.sidebar .sidebar-content {
    background-color: #d1e7dd; /* Slightly darker teal */
}
/* Set text color for input fields */
.stTextInput textarea {
    color: #000000 !important;
}
/* Change styles for dropdown menu */
.stSelectbox div[data-baseweb="select"] {
    color: black !important;
    background-color: #d1e7dd !important;
}
/* Change color of dropdown icons */
.stSelectbox svg {
    fill: black !important;
}
/* Change background and text color for dropdown options */
.stSelectbox option {
    background-color: #d1e7dd !important;
    color: black !important;
}
/* Change background and text color for dropdown items */
div[role="listbox"] div {
    background-color: #d1e7dd !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# Set the title of the app
st.title("💰 Financial Assistant")
# Add a small description under the title
st.caption("🌟 Your AI-Powered Financial Advisor")

# Create the sidebar with options
with st.sidebar:
    # Add a dividing line
    st.divider()
    # Display a section for assistant features
    st.markdown("### Assistant Capabilities")
    st.markdown("""
    - 📊 Investment Analysis
    - 💳 Budgeting Advice
    - 🏦 Loan Guidance
    - 💡 Retirement Planning
    """)
    # Add another dividing line
    st.divider()
        # Show a small footer message
    st.markdown("Built with NVIDIA API | LangChain ")
    st.markdown("Created with ❤ by Nikhil Kumar")

# Start the AI client using the API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key_nvidia
)

# Define a message that tells the AI how to respond
system_prompt_template = (
    "I am an expert AI financial assistant. Provide accurate, concise, and empathetic responses "
    "to user queries related to investments, budgeting, loans, retirement planning, and other financial matters. "
    "Always respond in English."
)

# Initialize chat history if it doesn't exist
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {"role": "assistant", "content": "Hi! I'm your Finance Assistant. How can I assist you today? 💰"}
    ]

# Create a container to display chat messages
chat_container = st.container()

# Show chat messages inside the container
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input field for user to type questions
user_query = st.chat_input("Type your finance-related question here...")

# Function to get a response from the AI
def generate_ai_response(messages):
    """
    Sends the conversation to the AI model and processes the response.
    """
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1",
        messages=messages,
        temperature=0.5,  # Controls randomness of responses
        top_p=0.5,  # Helps control diversity of responses
        max_tokens=1000,  # Maximum length of response
        stream=True  # Enables streaming of responses
    )

    # Process the AI response piece by piece
    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content
    return response

# Handle user input and generate AI responses
if user_query:
    # Save the user's message in chat history
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Create a list of messages to send to AI
    messages = [
        {"role": "system", "content": system_prompt_template},  # First message that tells AI how to behave
    ]

    # Add all previous messages to the conversation
    for msg in st.session_state.message_log:
        role = msg["role"]
        if role == "ai":
            role = "assistant"
        messages.append({"role": role, "content": msg["content"]})

    # Show a loading spinner while AI is thinking
    with st.spinner("🧠 Processing..."):
        # Get the AI response
        ai_response = generate_ai_response(messages)

    # Save the AI's response in chat history
    st.session_state.message_log.append({"role": "assistant", "content": ai_response})

    # Refresh the page to show the new chat messages
    st.rerun()