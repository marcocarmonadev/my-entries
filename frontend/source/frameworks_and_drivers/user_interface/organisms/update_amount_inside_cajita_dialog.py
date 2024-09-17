import requests
import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client


@st.dialog(
    title="Update amount inside Cajita",
)
def display():
    backend_client = get_backend_client()

    def on_click():
        try:
            backend_client.update_amount_inside_cajita(
                new_amount=st.session_state.amount_inside_cajita
            )
            st.session_state.sucess_message = (
                "Success at updating amount inside Cajita!"
            )
        except requests.HTTPError as exc:
            st.session_state.error_message = (
                f"Error {exc.response.status_code} at updating amount inside Cajita!"
            )

    with st.form(
        key="update_amount_inside_cajita_form",
        border=False,
    ):
        column1, column2 = st.columns(2)
        with column1:
            st.number_input(
                label="Amount inside Cajita",
                key="amount_inside_cajita",
                label_visibility="collapsed",
                format="%0.2f",
            )

        with column2:
            if st.form_submit_button(
                label="Submit",
                use_container_width=True,
                on_click=on_click,
            ):
                st.rerun()
