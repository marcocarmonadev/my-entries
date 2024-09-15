import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client
from source.frameworks_and_drivers.external_interfaces.backend import models


def display():
    backend_client = get_backend_client()
    entries = backend_client.get_entries()

    def on_change() -> None:
        entries_data_editor = st.session_state.entries_data_editor

        if deleted_rows := entries_data_editor["deleted_rows"]:
            backend_client.delete_entries(
                entry_uuids=[entries[i].uuid for i in deleted_rows],
            )
        if edited_rows := entries_data_editor["edited_rows"]:
            for k, body in edited_rows.items():
                if k not in deleted_rows:
                    entry: models.Entry = entries[k]
                    backend_client.update_entry(
                        entry.uuid,
                        body,
                    )

    st.data_editor(
        key="entries_data_editor",
        disabled=["uuid"],
        data=[entry.model_dump() for entry in entries],
        use_container_width=True,
        on_change=on_change,
        column_order=[
            "uuid",
            "concept",
            "amount",
            "due_date",
            "status",
            "frequency",
        ],
        column_config={
            "uuid": st.column_config.TextColumn(
                label="UUID",
                required=True,
                width="small",
            ),
            "concept": st.column_config.TextColumn(
                label="Concept",
                required=True,
            ),
            "amount": st.column_config.NumberColumn(
                label="Amount",
                format="$%f",
                required=True,
            ),
            "due_date": st.column_config.DateColumn(
                label="Due date",
                required=True,
            ),
            "status": st.column_config.SelectboxColumn(
                label="Status",
                options=[status for status in models.Status],
                required=True,
            ),
            "frequency": st.column_config.SelectboxColumn(
                label="Frequency",
                options=[frequency for frequency in models.Frequency],
                required=True,
                disabled=True,
            ),
        },
    )
