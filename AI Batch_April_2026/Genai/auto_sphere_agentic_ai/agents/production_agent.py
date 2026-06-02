import pandas as pd
from llm_handler import ask_groq


DATA_PATH = "data_source/production_data.csv"


def load_production_data():
    return pd.read_csv(DATA_PATH)


def filter_relevant_data(df: pd.DataFrame, user_question: str) -> pd.DataFrame:
    """
    Simple filtering logic.
    If vehicle model name is found in question, filter that model.
    Otherwise return full data.
    """

    question = user_question.lower()

    models = df["vehicle_model"].dropna().unique()

    for model in models:
        if model.lower() in question:
            return df[df["vehicle_model"].str.lower() == model.lower()]

    return df


def run_production_agent(user_question: str) -> str:
    """
    Production Agent:
    Answers questions about manufacturing status, planned units,
    completed units and production delays.
    """

    df = load_production_data()
    filtered_df = filter_relevant_data(df, user_question)

    data_text = filtered_df.to_string(index=False)

    system_prompt = """
You are a Production Agent for a premium car manufacturing company.
Your responsibility is to analyze production and manufacturing data.

You should answer questions about:
- vehicle production
- plant location
- planned units
- completed units
- production status
- delayed or completed production

Give clear business-friendly answers.
Do not make up data.
Use only the provided production data.
"""

    user_prompt = f"""
User Question:
{user_question}

Production Data:
{data_text}

Please provide a simple production-related answer.
"""

    return ask_groq(system_prompt, user_prompt)