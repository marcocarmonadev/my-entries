import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client
from source.frameworks_and_drivers.external_interfaces.backend import models


@st.experimental_dialog(
    title="Add entry",
)
def display():
    backend_client = get_backend_client()

    def on_click():
        backend_client.create_entry(
            st.session_state.concept,
            st.session_state.amount,
            st.session_state.due_date,
            st.session_state.status,
            st.session_state.repeat_count,
            st.session_state.repeat_interval,
        )

    with st.form(
        key="add_entry_form",
        border=False,
    ):
        column1, column2 = st.columns(2)
        with column1:
            st.text_input(
                "Concept",
                key="concept",
            )
            st.date_input(
                "Due date",
                format="YYYY-MM-DD",
                key="due_date",
            )
            st.number_input(
                "Repeat count",
                min_value=-1,
                value=0,
                step=1,
                help="-1 means forever",
                key="repeat_count",
            )

        with column2:
            st.number_input(
                "Amount",
                key="amount",
                value=0.0,
            )
            st.selectbox(
                label="Status",
                options=[status for status in models.Status],
                index=0,
                key="status",
            )
            st.number_input(
                "Repeat interval",
                min_value=1,
                step=1,
                key="repeat_interval",
            )

        if st.form_submit_button(
            label="Submit",
            use_container_width=True,
            on_click=on_click,
        ):
            st.rerun()
