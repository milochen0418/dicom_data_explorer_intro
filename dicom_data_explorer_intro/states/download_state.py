import reflex as rx
from datetime import datetime
import asyncio
import logging


class DownloadState(rx.State):
    cart_items: list[dict] = []
    download_history: list[dict] = []
    is_downloading: bool = False
    download_progress: int = 0

    @rx.var
    def cart_count(self) -> int:
        return len(self.cart_items)

    @rx.var
    def total_size_mb(self) -> float:
        total = 0.0
        for item in self.cart_items:
            size = item.get("series_size_MB")
            if size:
                try:
                    total += float(size)
                except (ValueError, TypeError) as e:
                    logging.exception(f"Error calculating size for item: {e}")
        return round(total, 2)

    @rx.event
    def add_to_cart(self, series: dict, source: str):
        for item in self.cart_items:
            if item["SeriesInstanceUID"] == series["SeriesInstanceUID"]:
                return
        item = series.copy()
        item["source"] = source
        item["added_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cart_items.append(item)

    @rx.event
    def remove_from_cart(self, series_uid: str):
        self.cart_items = [
            item for item in self.cart_items if item["SeriesInstanceUID"] != series_uid
        ]

    @rx.event
    def clear_cart(self):
        self.cart_items = []

    @rx.event
    async def start_download(self):
        """Simulate download process."""
        if not self.cart_items:
            return
        self.is_downloading = True
        self.download_progress = 0
        for i in range(1, 101, 10):
            self.download_progress = i
            await asyncio.sleep(0.2)
            yield
        self.download_progress = 100
        completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in self.cart_items:
            history_item = item.copy()
            history_item["downloaded_at"] = completed_time
            self.download_history.insert(0, history_item)
        self.cart_items = []
        self.is_downloading = False
        self.download_progress = 0