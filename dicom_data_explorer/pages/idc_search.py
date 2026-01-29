import reflex as rx
from dicom_data_explorer.states.idc_state import IDCState
from dicom_data_explorer.states.download_state import DownloadState
from dicom_data_explorer.components.layout import layout
from dicom_data_explorer.components.tooltip import helper_tooltip


def filter_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("IDC Search", class_name="font-bold text-gray-900"),
            rx.el.button(
                "Clear",
                on_click=IDCState.clear_search,
                class_name="text-sm text-red-500 hover:text-red-700 font-medium",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Collection", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.select(
                rx.el.option("All Collections", value=""),
                rx.foreach(
                    IDCState.collections,
                    lambda c: rx.el.option(c["Collection"], value=c["Collection"]),
                ),
                value=IDCState.selected_collection,
                on_change=lambda val: IDCState.update_filters("collection", val),
                class_name="w-full rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white appearance-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Modality", class_name="block text-sm font-medium text-gray-700"
                ),
                helper_tooltip("The type of machine used (e.g., CT, MRI, X-Ray)"),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.select(
                rx.el.option("All Modalities", value=""),
                rx.foreach(IDCState.modalities, lambda m: rx.el.option(m, value=m)),
                value=IDCState.selected_modality,
                on_change=lambda val: IDCState.update_filters("modality", val),
                class_name="w-full rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white appearance-none",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Body Part", class_name="block text-sm font-medium text-gray-700"
                ),
                helper_tooltip("The part of the body that was scanned"),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.select(
                rx.el.option("All Body Parts", value=""),
                rx.foreach(IDCState.body_parts, lambda b: rx.el.option(b, value=b)),
                value=IDCState.selected_body_part,
                on_change=lambda val: IDCState.update_filters("body_part", val),
                class_name="w-full rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white appearance-none",
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Search IDC",
            on_click=IDCState.search_data,
            class_name="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 shadow-md transition-colors flex items-center justify-center gap-2",
        ),
        class_name="w-72 bg-white border-r border-gray-200 p-6 flex flex-col h-full shrink-0 overflow-y-auto",
    )


def results_table_row(series: dict, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("file-digit", size=16, class_name="text-gray-400"),
                series["Modality"],
                class_name="flex items-center gap-2 font-medium text-gray-900",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            series["BodyPartExamined"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            series["SeriesDate"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.span(
                series["ImageCount"],
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Details",
                    on_click=IDCState.select_series(series["SeriesInstanceUID"]),
                    class_name="text-blue-600 hover:text-blue-900 font-medium text-xs mr-3",
                ),
                rx.el.button(
                    rx.icon("shopping-cart", size=16),
                    on_click=DownloadState.add_to_cart(series, "IDC"),
                    class_name="text-green-600 hover:text-green-800 p-1 rounded-full hover:bg-green-50 transition-colors",
                    title="Add to Cart",
                ),
                class_name="flex items-center justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name=rx.cond(
            IDCState.selected_series_uid == series["SeriesInstanceUID"],
            "bg-blue-50 border-l-4 border-l-blue-500",
            rx.cond(index % 2 == 0, "bg-white", "bg-gray-50"),
        ),
    )


def metadata_panel() -> rx.Component:
    return rx.cond(
        IDCState.selected_series_uid != "",
        rx.el.div(
            rx.el.div(
                rx.el.h3("Series Metadata", class_name="font-bold text-gray-900"),
                rx.el.button(
                    rx.icon("x", size=18),
                    on_click=IDCState.select_series(""),
                    class_name="text-gray-400 hover:text-gray-600",
                ),
                class_name="flex justify-between items-center mb-4 pb-4 border-b",
            ),
            rx.el.div(
                rx.foreach(
                    IDCState.selected_series_details.entries(),
                    lambda entry: rx.el.div(
                        rx.el.dt(
                            entry[0],
                            class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1",
                        ),
                        rx.el.dd(
                            entry[1], class_name="text-sm text-gray-900 break-words"
                        ),
                        class_name="mb-4",
                    ),
                ),
                class_name="overflow-y-auto max-h-[calc(100vh-250px)]",
            ),
            rx.el.button(
                "Add to Downloads",
                on_click=DownloadState.add_to_cart(
                    IDCState.selected_series_details, "IDC"
                ),
                class_name="w-full mt-4 bg-gray-900 text-white py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors",
            ),
            class_name="w-80 bg-white border-l border-gray-200 p-6 h-full shrink-0 shadow-lg",
        ),
        None,
    )


def results_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "IDC Search Results", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.div(
                rx.el.span(
                    f"Page {IDCState.page} of {IDCState.total_pages}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-end mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Search",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    value=IDCState.search_query,
                    on_change=IDCState.update_search_query,
                    placeholder="Collection, UID, description...",
                    class_name="w-full rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Min Images",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    value=IDCState.min_images,
                    on_change=IDCState.update_min_images,
                    placeholder="0",
                    type="number",
                    step=1,
                    class_name="w-28 rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Max Images",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    value=IDCState.max_images,
                    on_change=IDCState.update_max_images,
                    placeholder="9999",
                    type="number",
                    step=1,
                    class_name="w-28 rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Sort By",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Date", value="SeriesDate"),
                    rx.el.option("Images", value="ImageCount"),
                    rx.el.option("Modality", value="Modality"),
                    value=IDCState.sort_field,
                    on_change=IDCState.update_sort_field,
                    class_name="w-36 rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Order",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Desc", value="desc"),
                    rx.el.option("Asc", value="asc"),
                    value=IDCState.sort_direction,
                    on_change=IDCState.update_sort_direction,
                    class_name="w-28 rounded-lg border-gray-300 border p-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white",
                ),
            ),
            class_name="flex flex-wrap items-end gap-4 mb-6",
        ),
        rx.cond(
            IDCState.is_loading,
            rx.el.div(
                rx.spinner(size="3"),
                rx.el.p("Querying IDC Index...", class_name="mt-4 text-gray-500"),
                class_name="flex flex-col items-center justify-center h-64",
            ),
            rx.cond(
                IDCState.series_results.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Modality",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Body Part",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Date",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Images",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th("", class_name="px-6 py-3 relative"),
                                ),
                                class_name="bg-gray-50",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    IDCState.current_page_results,
                                    lambda s, i: results_table_row(s, i),
                                ),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="overflow-x-auto rounded-lg border border-gray-200 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Previous",
                            on_click=IDCState.set_page(IDCState.page - 1),
                            disabled=IDCState.page <= 1,
                            class_name="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        rx.el.button(
                            "Next",
                            on_click=IDCState.set_page(IDCState.page + 1),
                            disabled=IDCState.page >= IDCState.total_pages,
                            class_name="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="flex justify-end gap-2 mt-4",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.icon("search", size=48, class_name="text-gray-300 mb-4"),
                    rx.el.h3(
                        rx.cond(
                            IDCState.search_performed,
                            "No results found",
                            "Ready to search IDC",
                        ),
                        class_name="text-lg font-medium text-gray-900",
                    ),
                    rx.el.p(
                        rx.cond(
                            IDCState.search_performed,
                            "Try adjusting your filters.",
                            "Select filters on the left and click Search IDC.",
                        ),
                        class_name="text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center h-64 bg-white rounded-lg border border-dashed border-gray-300",
                ),
            ),
        ),
        class_name="flex-1 p-8 overflow-y-auto",
    )


def idc_search_content() -> rx.Component:
    return rx.el.div(
        filter_sidebar(),
        results_view(),
        metadata_panel(),
        class_name="flex h-full w-full",
    )


def idc_search_page() -> rx.Component:
    return layout(idc_search_content())