import reflex as rx
from dicom_data_explorer_intro.services.idc_service import (
    fetch_collections,
    fetch_modalities,
    fetch_body_parts,
    fetch_series,
)


class IDCState(rx.State):
    collections: list[dict] = []
    modalities: list[str] = []
    body_parts: list[str] = []
    series_results: list[dict] = []
    selected_collection: str = ""
    selected_modality: str = ""
    selected_body_part: str = ""
    is_loading: bool = False
    error_message: str = ""
    search_performed: bool = False
    page: int = 1
    items_per_page: int = 10
    selected_series_uid: str = ""
    sort_field: str = "SeriesDate"
    sort_direction: str = "desc"
    search_query: str = ""
    min_images: str = ""
    max_images: str = ""

    @rx.var
    def total_pages(self) -> int:
        return (
            len(self.filtered_results) + self.items_per_page - 1
        ) // self.items_per_page

    @rx.var
    def current_page_results(self) -> list[dict]:
        start = (self.page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_results[start:end]

    @rx.var
    def filtered_results(self) -> list[dict]:
        results = self.series_results
        query = self.search_query.strip().lower()
        if query:
            def matches(item: dict) -> bool:
                haystack = " ".join(
                    str(item.get(field, ""))
                    for field in [
                        "Collection",
                        "SeriesDescription",
                        "SeriesInstanceUID",
                        "Modality",
                        "BodyPartExamined",
                    ]
                ).lower()
                return query in haystack

            results = [item for item in results if matches(item)]

        def parse_int(value: str) -> int | None:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        min_val = parse_int(self.min_images)
        max_val = parse_int(self.max_images)
        if min_val is not None:
            results = [
                item
                for item in results
                if int(item.get("ImageCount") or 0) >= min_val
            ]
        if max_val is not None:
            results = [
                item
                for item in results
                if int(item.get("ImageCount") or 0) <= max_val
            ]

        sort_key = self.sort_field
        reverse = self.sort_direction == "desc"

        def key_func(item: dict):
            value = item.get(sort_key, "")
            if sort_key == "ImageCount":
                try:
                    return int(value)
                except (TypeError, ValueError):
                    return 0
            return value or ""

        return sorted(results, key=key_func, reverse=reverse)

    @rx.var
    def selected_series_details(self) -> dict:
        if not self.selected_series_uid:
            return {}
        for series in self.series_results:
            if series.get("SeriesInstanceUID") == self.selected_series_uid:
                return series
        return {}

    @rx.event
    def load_initial_data(self):
        """Load collections on mount."""
        self.is_loading = True
        yield
        cols = fetch_collections()
        self.collections = cols
        mods = fetch_modalities()
        self.modalities = [m.get("Modality") for m in mods if m.get("Modality")]
        parts = fetch_body_parts()
        self.body_parts = [
            b.get("BodyPartExamined") for b in parts if b.get("BodyPartExamined")
        ]
        self.is_loading = False

    @rx.event
    def update_filters(self, key: str, value: str):
        """Update a specific filter."""
        if key == "collection":
            self.selected_collection = value
        elif key == "modality":
            self.selected_modality = value
        elif key == "body_part":
            self.selected_body_part = value
        self.page = 1

    @rx.event
    def update_search_query(self, value: str):
        self.search_query = value
        self.page = 1

    @rx.event
    def update_min_images(self, value: float):
        try:
            self.min_images = str(int(value))
        except (TypeError, ValueError):
            self.min_images = ""
        self.page = 1

    @rx.event
    def update_max_images(self, value: float):
        try:
            self.max_images = str(int(value))
        except (TypeError, ValueError):
            self.max_images = ""
        self.page = 1

    @rx.event
    def update_sort_field(self, value: str):
        self.sort_field = value
        self.page = 1

    @rx.event
    def update_sort_direction(self, value: str):
        self.sort_direction = value
        self.page = 1

    @rx.event
    def search_data(self):
        """Search for series based on current filters."""
        self.is_loading = True
        self.search_performed = True
        self.series_results = []
        self.page = 1
        self.selected_series_uid = ""
        yield
        results = fetch_series(
            collection=self.selected_collection,
            modality=self.selected_modality,
            body_part=self.selected_body_part,
        )
        self.series_results = results
        self.is_loading = False

    @rx.event
    def clear_search(self):
        self.selected_collection = ""
        self.selected_modality = ""
        self.selected_body_part = ""
        self.search_query = ""
        self.min_images = ""
        self.max_images = ""
        self.sort_field = "SeriesDate"
        self.sort_direction = "desc"
        self.series_results = []
        self.search_performed = False
        self.page = 1

    @rx.event
    def set_page(self, page: int):
        self.page = page

    @rx.event
    def select_series(self, uid: str):
        if self.selected_series_uid == uid:
            self.selected_series_uid = ""
        else:
            self.selected_series_uid = uid