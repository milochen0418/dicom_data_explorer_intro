import reflex as rx
from dicom_data_explorer.states.download_state import DownloadState
from dicom_data_explorer.components.layout import layout


def cart_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("file-archive", class_name="text-blue-500", size=24),
                rx.el.div(
                    rx.el.h4(
                        item["Collection"],
                        class_name="font-semibold text-gray-900 truncate",
                    ),
                    rx.el.p(
                        f"{item['Modality']} • {item['BodyPartExamined']} • {item['ImageCount']} Images",
                        class_name="text-sm text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.span(
                    item["source"],
                    class_name="bg-gray-100 text-gray-700 text-xs font-medium px-2 py-1 rounded-md mr-3",
                ),
                rx.el.button(
                    rx.icon("trash-2", size=18),
                    on_click=DownloadState.remove_from_cart(item["SeriesInstanceUID"]),
                    class_name="text-red-400 hover:text-red-600 p-2 hover:bg-red-50 rounded-full transition-colors",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center w-full",
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm mb-3",
    )


def history_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("circle_pause", class_name="text-green-500", size=20),
                rx.el.div(
                    rx.el.h4(
                        item["Collection"],
                        class_name="font-medium text-gray-900 truncate",
                    ),
                    rx.el.p(
                        f"Downloaded on {item['downloaded_at']}",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.span(
                item["source"],
                class_name="bg-gray-50 text-gray-500 text-xs px-2 py-1 rounded",
            ),
            class_name="flex justify-between items-center w-full",
        ),
        class_name="p-3 bg-gray-50 rounded-lg border border-gray-100 mb-2",
    )


def downloads_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Downloads", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your selected series and download history.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Download Cart", class_name="text-lg font-bold text-gray-900"
                    ),
                    rx.cond(
                        DownloadState.cart_count > 0,
                        rx.el.button(
                            "Clear Cart",
                            on_click=DownloadState.clear_cart,
                            class_name="text-sm text-red-500 hover:text-red-700 font-medium",
                        ),
                        None,
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.cond(
                    DownloadState.cart_count > 0,
                    rx.el.div(
                        rx.foreach(DownloadState.cart_items, cart_item),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span("Total Items:", class_name="text-gray-600"),
                                rx.el.span(
                                    DownloadState.cart_count,
                                    class_name="font-bold text-gray-900",
                                ),
                                class_name="flex justify-between mb-2",
                            ),
                            rx.el.div(
                                rx.el.span("Est. Size:", class_name="text-gray-600"),
                                rx.el.span(
                                    f"{DownloadState.total_size_mb} MB",
                                    class_name="font-bold text-gray-900",
                                ),
                                class_name="flex justify-between mb-6",
                            ),
                            rx.cond(
                                DownloadState.is_downloading,
                                rx.el.div(
                                    rx.el.div(
                                        class_name="h-2 bg-blue-600 rounded-full transition-all duration-300",
                                        style={
                                            "width": f"{DownloadState.download_progress}%"
                                        },
                                    ),
                                    class_name="w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-2",
                                ),
                                rx.el.button(
                                    "Download All Series",
                                    on_click=DownloadState.start_download,
                                    class_name="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 shadow-lg hover:shadow-xl transition-all",
                                ),
                            ),
                            rx.cond(
                                DownloadState.is_downloading,
                                rx.el.div(
                                    rx.el.p(
                                        DownloadState.progress_message,
                                        class_name="text-xs text-gray-500",
                                    ),
                                    rx.el.p(
                                        f"{DownloadState.downloaded_files} / {DownloadState.total_files} files",
                                        class_name="text-xs text-gray-600 font-medium",
                                    ),
                                    class_name="mt-2 flex items-center justify-between",
                                ),
                                None,
                            ),
                            class_name="mt-6 p-6 bg-gray-50 rounded-xl border border-gray-200",
                        ),
                    ),
                    rx.el.div(
                        rx.icon(
                            "shopping-cart", size=48, class_name="text-gray-300 mb-4"
                        ),
                        rx.el.p("Your cart is empty", class_name="text-gray-500"),
                        rx.el.a(
                            "Browse IDC",
                            href="/idc-search",
                            class_name="mt-4 text-blue-600 font-medium hover:underline",
                        ),
                        class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-dashed border-gray-300",
                    ),
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.h2("History", class_name="text-lg font-bold text-gray-900 mb-4"),
                rx.cond(
                    DownloadState.download_history.length() > 0,
                    rx.el.div(
                        rx.foreach(DownloadState.download_history, history_item),
                        class_name="overflow-y-auto max-h-[600px] pr-2",
                    ),
                    rx.el.p(
                        "No downloads yet.", class_name="text-sm text-gray-500 italic"
                    ),
                ),
                class_name="col-span-1 pl-6 border-l border-gray-200",
            ),
            class_name="grid grid-cols-3 gap-8",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )


def downloads_page() -> rx.Component:
    return layout(downloads_content())