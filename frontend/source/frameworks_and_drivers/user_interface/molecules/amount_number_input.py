import streamlit as st


def display():
    st.number_input(
        "Amount",
        key="amount",
        value=0.0,
    )
