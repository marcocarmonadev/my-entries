import streamlit as st

from source.frameworks_and_drivers.user_interface.organisms import (
    add_entry_dialog,
    delete_entry_dialog,
    entries_data_editor,
    statistics_metrics,
    update_amount_inside_cajita_dialog,
)


def display():
    st.set_page_config(
        page_title="My entries",
        page_icon="💰",
    )
    st.title(
        body="💰 My entries",
    )

    statistics_metrics.display()

    column1, column2, column3 = st.columns([0.46, 0.46, 0.08])
    with column1:
        if st.button(
            label="➕ Entry",
            use_container_width=True,
            key="add_entry_button",
        ):
            add_entry_dialog.display()

    with column2:
        if st.button(
            label="🗑️ Entry",
            use_container_width=True,
            key="delete_entry_button",
        ):
            delete_entry_dialog.display()

    with column3:
        if st.button(
            label="💸",
            key="update_amount_inside_cajita_button",
        ):
            update_amount_inside_cajita_dialog.display()

    if "error_message" in st.session_state:
        st.toast(
            body=st.session_state.error_message,
            icon="🔴",
        )
        del st.session_state.error_message

    if "sucess_message" in st.session_state:
        st.toast(
            body=st.session_state.sucess_message,
            icon="🟢",
        )
        del st.session_state.sucess_message

    entries_data_editor.display()


if __name__ == "__main__":
    display()
