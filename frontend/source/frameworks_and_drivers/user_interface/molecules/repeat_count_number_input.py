import streamlit as st


def display():
    st.number_input(
        "Repeat count",
        min_value=0,
        value=1,
        step=1,
        help="0 means forever",
        key="repeat_count",
    )
