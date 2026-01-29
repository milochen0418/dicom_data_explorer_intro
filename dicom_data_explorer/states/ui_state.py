import reflex as rx


class UIState(rx.State):
    """State for UI elements like sidebar, onboarding, and global settings."""

    is_sidebar_open: bool = True
    is_onboarding_open: bool = False
    current_onboarding_step: int = 0
    selected_source: str = ""
    onboarding_steps: list[dict[str, str]] = [
        {
            "title": "Welcome to DICOM Explorer",
            "content": "This tool helps you explore and download medical imaging data without needing technical expertise. We bridge the gap between complex archives and you.",
            "icon": "hand",
        },
        {
            "title": "Understanding Collections",
            "content": "A 'Collection' (or Dataset) is a group of images usually related to a specific research project, cancer type, or clinical trial.",
            "icon": "folder-open",
        },
        {
            "title": "Patients & Studies",
            "content": "Data is organized by 'Patient'. Each patient may have multiple 'Studies' (e.g., a specific visit to the doctor for a scan).",
            "icon": "users",
        },
        {
            "title": "Series & Instances",
            "content": "A 'Series' is a single scan (like a CT chest scan) consisting of many individual images called 'Instances' (DICOM files).",
            "icon": "layers",
        },
        {
            "title": "Ready to Explore?",
            "content": "Select a Data Source on the dashboard to start browsing. You can always revisit this guide from the Help menu.",
            "icon": "rocket",
        },
    ]

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def open_onboarding(self):
        self.is_onboarding_open = True
        self.current_onboarding_step = 0

    @rx.event
    def close_onboarding(self):
        self.is_onboarding_open = False

    @rx.event
    def next_onboarding_step(self):
        if self.current_onboarding_step < len(self.onboarding_steps) - 1:
            self.current_onboarding_step += 1
        else:
            self.is_onboarding_open = False

    @rx.event
    def prev_onboarding_step(self):
        if self.current_onboarding_step > 0:
            self.current_onboarding_step -= 1

    @rx.event
    def select_source(self, source: str):
        self.selected_source = source