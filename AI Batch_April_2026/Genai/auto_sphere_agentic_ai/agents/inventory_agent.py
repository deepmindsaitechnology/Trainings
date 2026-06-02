import pandas as pd
from llm_handler import ask_groq


DATA_PATH = "data_source/inventory_data.csv"


def load_inventory_data():
    return pd.read_csv(DATA_PATH)

def filter_relevant_data(df: pd.DataFrame, user_question: str) -> pd.DataFrame:
    """
    Simple filtering by vehicle model, city/location, vehicle type or stock status.
    """

    question = user_question.lower()

    models = df["vehicle_model"].dropna().unique()
    for model in models:
        if model.lower() in question:
            return df[df["vehicle_model"].str.lower() == model.lower()]

    locations = df["location"].dropna().unique()
    for location in locations:
        if location.lower() in question:
            return df[df["location"].str.lower() == location.lower()]

    vehicle_types = df["vehicle_type"].dropna().unique()
    for vehicle_type in vehicle_types:
        if vehicle_type.lower() in question:
            return df[df["vehicle_type"].str.lower() == vehicle_type.lower()]

    if "low stock" in question:
        return df[df["stock_status"].str.lower() == "low stock"]

    if "out of stock" in question:
        return df[df["stock_status"].str.lower() == "out of stock"]

    return df


def run_inventory_agent(user_question: str) -> str:
    """
    Inventory Agent:
    Answers questions about stock availability,
    reserved units and dealer/warehouse location.
    """

    df = load_inventory_data()
    filtered_df = filter_relevant_data(df, user_question)

    data_text = filtered_df.to_string(index=False)

    system_prompt = """
You are an Inventory Agent for a premium car manufacturing company.
Your responsibility is to analyze vehicle stock and availability.

You should answer questions about:
- available units
- reserved units
- city-wise inventory
- EV, petrol and diesel inventory
- low stock or out of stock vehicles

Give clear business-friendly answers.
Do not make up data.
Use only the provided inventory data.
"""

    user_prompt = f"""
User Question:
{user_question}

Inventory Data:
{data_text}

Please provide a simple inventory-related answer.
"""

    return ask_groq(system_prompt, user_prompt)