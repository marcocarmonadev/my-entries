import streamlit as st

from source.frameworks_and_drivers.user_interface.organisms import (
    add_entry_dialog,
    delete_entry_dialog,
    entries_data_editor,
    statistics,
)


def display():
    st.title(
        body="Entries",
    )

    statistics.display()

    column1, column2 = st.columns(2)
    with column1:
        if st.button(
            label="Add entry",
            use_container_width=True,
        ):
            add_entry_dialog.display()

    with column2:
        if st.button(
            label="Delete entry",
            use_container_width=True,
        ):
            delete_entry_dialog.display()

    entries_data_editor.display()
