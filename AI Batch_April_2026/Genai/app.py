import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Chatbot using Agno + Groq")

# Create Agent
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True
)

# User input from screen
user_question = st.text_input(
    "Enter your question:",
    placeholder="Ask anything here..."
)

# Button click
if st.button("Submit"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
    
    else:
        with st.spinner("Generating response..."):

            # Get response from AI
            response = agent.run(user_question)

            # Display response
            st.subheader("Response:")
            st.write(response.content)