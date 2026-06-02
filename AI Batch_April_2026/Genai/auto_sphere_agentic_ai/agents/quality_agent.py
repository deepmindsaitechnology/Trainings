import pandas as pd
from llm_handler import ask_groq


DATA_PATH = "data_source/quality_data.csv"


def load_quality_data():
    return pd.read_csv(DATA_PATH)


def filter_relevant_data(df: pd.DataFrame, user_question: str) -> pd.DataFrame:
    """
    Simple filtering by vehicle model or defect category.
    """

    question = user_question.lower()

    models = df["vehicle_model"].dropna().unique()
    for model in models:
        if model.lower() in question:
            return df[df["vehicle_model"].str.lower() == model.lower()]

    defect_categories = df["defect_category"].dropna().unique()
    for defect in defect_categories:
        if defect.lower() in question:
            return df[df["defect_category"].str.lower() == defect.lower()]

    return df


def run_quality_agent(user_question: str) -> str:
    """
    Quality Agent:
    Answers questions about inspection results, defects,
    severity and corrective action status.
    """

    df = load_quality_data()
    filtered_df = filter_relevant_data(df, user_question)

    data_text = filtered_df.to_string(index=False)

    system_prompt = """
You are a Quality Inspection Agent for a premium car manufacturing company.
Your responsibility is to analyze quality inspection and defect data.

You should answer questions about:
- inspection results
- passed or failed vehicles
- defect category
- defect severity
- open or resolved issues
- quality risk

Give clear business-friendly answers.
Do not make up data.
Use only the provided quality data.
"""

    user_prompt = f"""
User Question:
{user_question}

Quality Inspection Data:
{data_text}

Please provide a simple quality-related answer.
"""

    return ask_groq(system_prompt, user_prompt)