import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client


@st.experimental_dialog(
    title="Delete entries",
)
def display():
    backend_client = get_backend_client()

    def on_click():
        backend_client.delete_entries(
            st.session_state.entry_uuids.split("\n"),
        )

    with st.form(
        key="delete_entry_form",
        border=False,
    ):
        st.text_area(
            label="Entry uuids",
            key="entry_uuids",
        )

        if st.form_submit_button(
            label="Submit",
            use_container_width=True,
            on_click=on_click,
        ):
            st.rerun()
