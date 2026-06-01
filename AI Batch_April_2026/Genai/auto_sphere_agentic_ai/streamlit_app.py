import streamlit as st
from agents.orchestration_agent import run_orchestration_agent


st.set_page_config(
    page_title="AutoSphere Agentic AI",
    page_icon="🚗",
    layout="wide"
)


st.title("🚗 AutoSphere Agentic AI")
st.subheader("Smart Automotive Operations Assistant")

st.write(
    """
    This simple Agentic AI application uses one orchestration agent and four specialist agents:
    Production Agent, Quality Agent, Inventory Agent and Sales Agent.
    """
)

with st.expander("View Agent Details"):
    st.markdown(
        """
        ### Agents Used

        **1. Production Agent**  
        Handles manufacturing, plant, production target and completed units.

        **2. Quality Agent**  
        Handles inspection results, defects, severity and corrective action status.

        **3. Inventory Agent**  
        Handles stock availability, reserved units, low stock and dealer location.

        **4. Sales Agent**  
        Handles sales units, city-wise sales and revenue.

        **5. Orchestration Agent**  
        Understands the user question, routes it to the correct agents and prepares the final response.
        """
    )


sample_questions = [
    "Give me overall performance summary of Defender",
    "Which vehicle models have low stock?",
    "Show production status of Range Rover Sport",
    "Which model has highest sales revenue?",
    "Are there any quality issues in Jaguar I-PACE?",
    "How many EV vehicles are available?"
]

st.markdown("### Ask a Business Question")

selected_sample = st.selectbox(
    "Select a sample question or write your own below:",
    [""] + sample_questions
)

user_question = st.text_area(
    "Enter your question:",
    value=selected_sample,
    height=100,
    placeholder="Example: Give overall performance summary of Defender"
)

ask_button = st.button("Ask Agentic AI Assistant")

if ask_button:
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Agents are working on your question..."):
            try:
                result = run_orchestration_agent(user_question)

                selected_agents = result["selected_agents"]
                agent_outputs = result["agent_outputs"]
                final_response = result["final_response"]

                st.success("Response generated successfully.")

                st.markdown("### Selected Agents")
                cols = st.columns(4)

                agent_icons = {
                    "production": "🏭 Production Agent",
                    "quality": "✅ Quality Agent",
                    "inventory": "📦 Inventory Agent",
                    "sales": "📊 Sales Agent"
                }

                for index, agent in enumerate(selected_agents):
                    with cols[index % 4]:
                        st.info(agent_icons.get(agent, agent))

                st.markdown("### Final Consolidated Answer")
                st.write(final_response)

                st.markdown("---")
                st.markdown("### Individual Agent Outputs")

                for agent_name, output in agent_outputs.items():
                    with st.expander(agent_name):
                        st.write(output)

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)


st.markdown("---")
st.caption("Demo application for learning Agentic AI using Groq LLM, Streamlit and CSV data.")