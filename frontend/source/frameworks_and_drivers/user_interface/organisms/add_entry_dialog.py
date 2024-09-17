import requests
import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client
from source.frameworks_and_drivers.external_interfaces.backend import models
from source.frameworks_and_drivers.user_interface.molecules import (
    amount_number_input,
    concept_text_input,
    due_date_input,
    frequency_radio,
    repeat_count_number_input,
    repeat_interval_number_input,
    status_selectbox,
)


@st.dialog(
    title="Add entry",
    width="large",
)
def display():
    backend_client = get_backend_client()

    def on_click():
        try:
            match st.session_state.frequency:
                case models.Frequency.ONE_TIME:
                    backend_client.create_entry(
                        concept=st.session_state.concept,
                        amount=st.session_state.amount,
                        due_date=st.session_state.due_date.strftime("%Y-%m-%d"),
                        status=st.session_state.status,
                        frequency=st.session_state.frequency,
                    )
                case models.Frequency.BI_WEEKLY:
                    backend_client.create_entry(
                        concept=st.session_state.concept,
                        amount=st.session_state.amount,
                        due_date=st.session_state.due_date.strftime("%Y-%m-%d"),
                        frequency=st.session_state.frequency,
                        repeat_count=st.session_state.repeat_count,
                    )
                case _:
                    backend_client.create_entry(
                        concept=st.session_state.concept,
                        amount=st.session_state.amount,
                        due_date=st.session_state.due_date.strftime("%Y-%m-%d"),
                        frequency=st.session_state.frequency,
                        repeat_count=st.session_state.repeat_count,
                        repeat_interval=st.session_state.repeat_interval,
                    )
            st.session_state.sucess_message = "Success at adding entry!"
        except requests.HTTPError as exc:
            st.session_state.error_message = (
                f"Error {exc.response.status_code} at adding entry!"
            )

    frequency_radio.display()

    with st.form(
        key="add_entry_form",
        border=False,
    ):
        column1, column2 = st.columns(2)
        with column1:
            concept_text_input.display()
            due_date_input.display()

        with column2:
            amount_number_input.display()

            if st.session_state.frequency in {
                models.Frequency.ONE_TIME,
            }:
                status_selectbox.display()

            if st.session_state.frequency in {
                models.Frequency.BI_WEEKLY,
            }:
                repeat_count_number_input.display()

            if st.session_state.frequency not in {
                models.Frequency.ONE_TIME,
                models.Frequency.BI_WEEKLY,
            }:
                subcolumn1, subcolumn2 = st.columns(2)
                with subcolumn1:
                    repeat_count_number_input.display()

                with subcolumn2:
                    repeat_interval_number_input.display()

        if st.form_submit_button(
            label="Submit",
            use_container_width=True,
            on_click=on_click,
        ):
            st.rerun()
