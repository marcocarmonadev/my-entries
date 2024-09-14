import streamlit as st

from source.frameworks_and_drivers.external_interfaces import get_backend_client


def display():
    backend_client = get_backend_client()
    entries_statistics = backend_client.get_entries_statistics()
    column1, column2, column3, column4 = st.columns(4)

    column1.metric(
        label="Income amount",
        value=f'${entries_statistics["income_amount"]}',
    )

    column2.metric(
        label="Expense amount",
        value=f'${entries_statistics["expense_amount"]}',
    )

    column3.metric(
        label="Complete expense amount",
        value=f'${entries_statistics["complete_expense_amount"]}',
    )

    column4.metric(
        label="Total amount",
        value=f'${entries_statistics["total_amount"]}',
    )
