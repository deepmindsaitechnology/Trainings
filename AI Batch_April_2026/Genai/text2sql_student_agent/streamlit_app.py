"""One-page Streamlit UI for the Student DB Text2SQL conversational agent."""

import streamlit as st
from mysql.connector import Error as MySQLError

from llm_handlers import ask_database, get_db_connection, load_schema_metadata

st.set_page_config(
    page_title="Student DB AI Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Student Database AI Assistant")
st.caption(
    "Ask questions in natural language. "
    "The agent creates and runs read-only SQL on `source_db`."
)

schema = load_schema_metadata()

with st.sidebar:
    st.header("Database")
    st.code("source_db", language=None)

    if st.button("Test DB Connection", use_container_width=True):
        try:
            connection = get_db_connection()
            connection.close()
            st.success("Database connection successful.")
        except Exception as error:
            st.error(f"Connection failed: {error}")

    st.divider()
    st.subheader("Available Tables")

    for table_name, metadata in schema["tables"].items():
        with st.expander(table_name):
            for column, datatype in metadata["columns"].items():
                st.write(f"**{column}** — {datatype}")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.info(
    "Example questions: Which student scored highest total marks? · "
    "Show average marks by class · List teachers teaching Science · "
    "How many students use each bus route?"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! Ask me questions about students, exam marks, or teachers."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sql"):
            with st.expander("View generated SQL"):
                st.code(message["sql"], language="sql")

        if message.get("data") is not None:
            st.dataframe(
                message["data"],
                use_container_width=True,
                hide_index=True,
            )

question = st.chat_input("Ask a question about your school database...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    previous_questions = [
        msg["content"]
        for msg in st.session_state.messages[-6:]
        if msg["role"] == "user"
    ]

    conversation_context = " | ".join(previous_questions[:-1])

    with st.chat_message("assistant"):
        try:
            with st.spinner("Generating SQL and checking database results..."):
                response = ask_database(question, conversation_context)

            st.markdown(response["answer"])

            with st.expander("View generated SQL"):
                st.code(response["sql"], language="sql")
                st.caption(response["interpretation"])

            st.dataframe(
                response["data"],
                use_container_width=True,
                hide_index=True,
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response["answer"],
                    "sql": response["sql"],
                    "data": response["data"],
                }
            )

        except (ValueError, MySQLError) as error:
            message = f"Unable to answer from the database: {error}"
            st.error(message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": message,
                }
            )

        except Exception as error:
            message = f"Application error: {error}"
            st.error(message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": message,
                }
            )