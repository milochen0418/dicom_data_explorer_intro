import reflex as rx
from dicom_data_explorer_intro.states.tcia_state import TCIAState
from dicom_data_explorer_intro.components.layout import layout


def collection_card(data: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("folder", class_name="text-blue-500", size=24),
            rx.el.h3(
                data["Collection"], class_name="font-semibold text-gray-900 truncate"
            ),
            class_name="flex items-center gap-3 mb-2",
        ),
        rx.el.div(
            rx.el.span(
                "Public",
                class_name="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full",
            ),
            class_name="flex gap-2",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer",
        on_click=lambda: [
            TCIAState.update_filters("collection", data["Collection"]),
            rx.redirect("/search"),
        ],
    )


def collections_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Browse Collections", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Select a collection to view its available imaging series.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.cond(
            TCIAState.is_loading,
            rx.el.div(
                rx.spinner(size="3"),
                class_name="flex justify-center items-center py-20",
            ),
            rx.el.div(
                rx.foreach(TCIAState.collections, collection_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
            ),
        ),
        class_name="p-6",
    )


def collections_page() -> rx.Component:
    return layout(collections_content())