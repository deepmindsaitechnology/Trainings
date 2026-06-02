import pandas as pd
from llm_handler import ask_groq


DATA_PATH = "data_source/sales_data.csv"


def load_sales_data():
    return pd.read_csv(DATA_PATH)


def filter_relevant_data(df: pd.DataFrame, user_question: str) -> pd.DataFrame:
    """
    Simple filtering by vehicle model, city, state or vehicle type.
    """

    question = user_question.lower()

    models = df["vehicle_model"].dropna().unique()
    for model in models:
        if model.lower() in question:
            return df[df["vehicle_model"].str.lower() == model.lower()]

    cities = df["city"].dropna().unique()
    for city in cities:
        if city.lower() in question:
            return df[df["city"].str.lower() == city.lower()]

    states = df["state"].dropna().unique()
    for state in states:
        if state.lower() in question:
            return df[df["state"].str.lower() == state.lower()]

    vehicle_types = df["vehicle_type"].dropna().unique()
    for vehicle_type in vehicle_types:
        if vehicle_type.lower() in question:
            return df[df["vehicle_type"].str.lower() == vehicle_type.lower()]

    return df


def run_sales_agent(user_question: str) -> str:
    """
    Sales Agent:
    Answers questions about model-wise sales,
    city-wise sales and revenue.
    """

    df = load_sales_data()
    filtered_df = filter_relevant_data(df, user_question)

    data_text = filtered_df.to_string(index=False)

    system_prompt = """
You are a Sales Performance Agent for a premium car manufacturing company.
Your responsibility is to analyze sales and revenue data.

You should answer questions about:
- model-wise sales
- city-wise sales
- state-wise sales
- EV, petrol and diesel sales
- total units sold
- revenue in crore rupees

Give clear business-friendly answers.
Do not make up data.
Use only the provided sales data.
"""

    user_prompt = f"""
User Question:
{user_question}

Sales Data:
{data_text}

Please provide a simple sales-related answer.
"""

    return ask_groq(system_prompt, user_prompt)