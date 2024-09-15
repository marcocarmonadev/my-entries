import streamlit as st


def display():
    st.number_input(
        "Repeat interval",
        min_value=1,
        step=1,
        key="repeat_interval",
    )
