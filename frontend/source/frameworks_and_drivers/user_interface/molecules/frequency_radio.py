import streamlit as st

from source.frameworks_and_drivers.external_interfaces.backend import models


def display():
    st.radio(
        label="Frequency",
        index=0,
        options=[frequency for frequency in models.Frequency],
        key="frequency",
        horizontal=True,
        format_func=lambda frequency: frequency.replace("_", "-"),
    )
