import reflex as rx
from dicom_data_explorer.states.ui_state import UIState
from dicom_data_explorer.components.tooltip import helper_tooltip


def step_card(number: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            number,
            class_name="w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold flex items-center justify-center mb-3",
        ),
        rx.el.h3(title, class_name="font-semibold text-gray-900 mb-1"),
        rx.el.p(description, class_name="text-sm text-gray-500"),
        class_name="flex flex-col p-4 bg-white rounded-xl border border-gray-100 shadow-sm",
    )


def data_source_card(
    id: str,
    title: str,
    description: str,
    badges: list[str],
    recommended: bool = False,
    link: str = "#",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
                rx.cond(
                    recommended,
                    rx.el.span(
                        "Recommended",
                        class_name="bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded-full ml-2",
                    ),
                    None,
                ),
                class_name="flex items-center mb-2",
            ),
            rx.el.p(
                description, class_name="text-gray-600 text-sm mb-4 leading-relaxed"
            ),
            rx.el.div(
                rx.foreach(
                    badges,
                    lambda tag: rx.el.span(
                        tag,
                        class_name="bg-gray-100 text-gray-600 text-xs font-medium px-2 py-1 rounded-md",
                    ),
                ),
                class_name="flex flex-wrap gap-2 mb-6",
            ),
        ),
        rx.el.a(
            rx.el.button(
                "Explore Data",
                class_name="w-full py-2.5 rounded-lg bg-gray-900 text-white font-medium transition-all flex items-center justify-center gap-2 hover:bg-gray-800",
            ),
            href=link,
        ),
        class_name="flex flex-col justify-between p-6 bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all",
    )


def welcome_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Welcome to DICOM Explorer",
                    class_name="text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Your gateway to public medical imaging datasets.",
                    rx.el.span(
                        " No coding required.", class_name="text-blue-600 font-medium"
                    ),
                    class_name="text-gray-600 text-lg",
                ),
            ),
            rx.el.button(
                "Start Interactive Tour",
                on_click=UIState.open_onboarding,
                class_name="px-4 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors shadow-sm",
            ),
            class_name="flex justify-between items-end mb-10",
        ),
        rx.el.div(
            rx.el.h2(
                "How it works", class_name="text-lg font-semibold text-gray-900 mb-4"
            ),
            rx.el.div(
                step_card(
                    "1", "Choose Source", "Select a public repository like IDC."
                ),
                step_card(
                    "2", "Browse Data", "Filter by body part, modality, or disease."
                ),
                step_card("3", "Select Series", "Preview metadata and choose scans."),
                step_card(
                    "4", "Download", "Get the DICOM files to your local machine."
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-10",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Select Data Source", class_name="text-xl font-bold text-gray-900"
                ),
                helper_tooltip(
                    "Repositories hosting anonymized medical images for research."
                ),
                class_name="flex items-center mb-6",
            ),
            rx.el.div(
                data_source_card(
                    "IDC",
                    "NCI Imaging Data Commons",
                    "A cloud-native repository with powerful search capabilities across vast amounts of data.",
                    ["Cloud Native", "Big Data", "Advanced Search"],
                    recommended=True,
                    link="/idc-search",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            ),
            class_name="mb-8",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )