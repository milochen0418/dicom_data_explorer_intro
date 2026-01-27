import reflex as rx
from dicom_data_explorer_intro.states.ui_state import UIState
from dicom_data_explorer_intro.states.download_state import DownloadState


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon,
                size=20,
                class_name="text-gray-500 group-hover:text-blue-600 transition-colors",
            ),
            rx.el.span(text, class_name="font-medium"),
            class_name="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-blue-50 group transition-all duration-200",
        ),
        href=href,
        class_name="w-full text-gray-700 block mb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="text-blue-600", size=28),
                rx.el.span(
                    "DICOM Explorer", class_name="text-xl font-bold text-gray-900"
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="h-16 flex items-center px-6 border-b border-gray-100",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "MENU",
                    class_name="text-xs font-bold text-gray-400 px-4 mb-2 tracking-wider",
                ),
                sidebar_item("Welcome", "layout-dashboard", "/"),
                sidebar_item("Collections", "database", "/collections"),
                sidebar_item("TCIA Search", "search", "/search"),
                sidebar_item("IDC Search", "cloud-drizzle", "/idc-search"),
                rx.el.div(
                    sidebar_item("Downloads", "download", "/downloads"),
                    rx.cond(
                        DownloadState.cart_count > 0,
                        rx.el.div(
                            DownloadState.cart_count,
                            class_name="absolute right-6 top-3 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full",
                        ),
                        None,
                    ),
                    class_name="relative",
                ),
                class_name="py-6",
            ),
            rx.el.div(
                rx.el.p(
                    "SUPPORT",
                    class_name="text-xs font-bold text-gray-400 px-4 mb-2 tracking-wider",
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon(
                            "graduation-cap",
                            size=20,
                            class_name="text-gray-500 group-hover:text-blue-600 transition-colors",
                        ),
                        rx.el.span("Show Tutorial", class_name="font-medium"),
                        class_name="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-blue-50 group transition-all duration-200 w-full",
                    ),
                    on_click=UIState.open_onboarding,
                    class_name="w-full text-left text-gray-700 block mb-1",
                ),
                sidebar_item("Help & FAQ", "circle-help", "/help"),
                class_name="py-2 border-t border-gray-100",
            ),
            class_name="flex-1 overflow-y-auto px-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span("GU", class_name="text-sm font-bold text-blue-600"),
                    class_name="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "Guest User", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p("Ready to explore", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="p-4 border-t border-gray-100",
        ),
        class_name="w-64 h-full bg-white border-r border-gray-200 flex flex-col shrink-0",
    )