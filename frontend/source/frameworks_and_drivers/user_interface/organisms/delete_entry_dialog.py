import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client


@st.dialog(
    title="Delete entry",
)
def display():
    backend_client = get_backend_client()

    def on_click():
        backend_client.delete_entry(
            st.session_state.entry_uuid,
        )
        st.session_state.sucess_message = "Success at deleting entry!"

    with st.form(
        key="delete_entry_form",
        border=False,
    ):
        column1, column2 = st.columns(2)
        with column1:
            st.text_input(
                label="Entry uuid",
                key="entry_uuid",
                label_visibility="collapsed",
                placeholder="00000000-0000-0000-0000-000000000000",
            )

        with column2:
            if st.form_submit_button(
                label="Submit",
                use_container_width=True,
                on_click=on_click,
            ):
                st.rerun()
