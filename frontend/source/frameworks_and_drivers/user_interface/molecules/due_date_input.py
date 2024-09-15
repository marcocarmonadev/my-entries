import streamlit as st


def display():
    st.date_input(
        "Due date",
        format="YYYY-MM-DD",
        key="due_date",
    )
