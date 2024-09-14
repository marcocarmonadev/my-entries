from functools import partial

import requests
import streamlit as st

from .backend import BackendClient

BackendInterface = partial(BackendClient)


@st.cache_resource
def get_http_session():
    return requests.Session()


@st.cache_resource
def get_backend_client():
    return BackendInterface(
        http_session=get_http_session(),
    )
