import reflex as rx
from dicom_data_explorer_intro.pages.welcome import welcome_page
from dicom_data_explorer_intro.pages.collections import collections_page
from dicom_data_explorer_intro.pages.search import search_page
from dicom_data_explorer_intro.pages.idc_search import idc_search_page
from dicom_data_explorer_intro.pages.downloads import downloads_page
from dicom_data_explorer_intro.states.tcia_state import TCIAState
from dicom_data_explorer_intro.states.idc_state import IDCState
from dicom_data_explorer_intro.components.layout import layout


def index() -> rx.Component:
    return layout(welcome_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(
    collections_page, route="/collections", on_load=TCIAState.load_initial_data
)
app.add_page(search_page, route="/search", on_load=TCIAState.load_initial_data)
app.add_page(idc_search_page, route="/idc-search", on_load=IDCState.load_initial_data)
app.add_page(downloads_page, route="/downloads")