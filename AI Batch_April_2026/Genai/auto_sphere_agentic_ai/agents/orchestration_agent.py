from llm_handler import ask_groq

from agents.production_agent import run_production_agent
from agents.quality_agent import run_quality_agent
from agents.inventory_agent import run_inventory_agent
from agents.sales_agent import run_sales_agent


def identify_required_agents(user_question: str):
    """
    Simple rule-based routing.
    This keeps the demo easy to understand.

    Returns a list of agents to call.
    """

    question = user_question.lower()

    selected_agents = []

    production_keywords = [
        "production", "manufacturing", "plant", "planned", "completed",
        "factory", "target", "delayed", "build"
    ]

    quality_keywords = [
        "quality", "inspection", "defect", "failed", "passed",
        "issue", "severity", "brake", "engine", "paint", "battery"
    ]

    inventory_keywords = [
        "inventory", "stock", "available", "reserved", "warehouse",
        "dealer", "low stock", "out of stock"
    ]

    sales_keywords = [
        "sales", "revenue", "sold", "city", "state", "highest sales",
        "monthly sales", "performance"
    ]

    overall_keywords = [
        "overall", "summary", "complete", "full", "business summary",
        "performance summary", "360", "all details"
    ]

    if any(keyword in question for keyword in overall_keywords):
        return ["production", "quality", "inventory", "sales"]

    if any(keyword in question for keyword in production_keywords):
        selected_agents.append("production")

    if any(keyword in question for keyword in quality_keywords):
        selected_agents.append("quality")

    if any(keyword in question for keyword in inventory_keywords):
        selected_agents.append("inventory")

    if any(keyword in question for keyword in sales_keywords):
        selected_agents.append("sales")

    # If no clear route found, call all agents.
    # This helps answer broad business questions.
    if not selected_agents:
        selected_agents = ["production", "quality", "inventory", "sales"]

    return selected_agents


def run_orchestration_agent(user_question: str):
    """
    Orchestration Agent:
    1. Reads user question
    2. Decides which specialist agents to call
    3. Collects each agent response
    4. Creates final combined response using Groq LLM
    """

    selected_agents = identify_required_agents(user_question)

    agent_outputs = {}

    if "production" in selected_agents:
        agent_outputs["Production Agent"] = run_production_agent(user_question)

    if "quality" in selected_agents:
        agent_outputs["Quality Agent"] = run_quality_agent(user_question)

    if "inventory" in selected_agents:
        agent_outputs["Inventory Agent"] = run_inventory_agent(user_question)

    if "sales" in selected_agents:
        agent_outputs["Sales Agent"] = run_sales_agent(user_question)

    combined_agent_text = ""

    for agent_name, output in agent_outputs.items():
        combined_agent_text += f"\n\n--- {agent_name} Output ---\n{output}"

    system_prompt = """
You are the Orchestration Agent for an automotive company AI assistant.

Your job:
- Review outputs from specialist agents
- Combine them into one final answer
- Keep the answer simple, clear and business-friendly
- Mention important risks or opportunities
- Do not make up any data
- Use only the agent outputs provided
"""

    user_prompt = f"""
User Question:
{user_question}

Specialist Agent Outputs:
{combined_agent_text}

Now provide the final consolidated answer.
"""

    final_response = ask_groq(system_prompt, user_prompt)

    return {
        "selected_agents": selected_agents,
        "agent_outputs": agent_outputs,
        "final_response": final_response
    }