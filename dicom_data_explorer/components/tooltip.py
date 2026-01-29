import reflex as rx


def helper_tooltip(text: str) -> rx.Component:
    """A consistent tooltip component for helping beginners."""
    return rx.tooltip(
        rx.el.span(
            rx.icon(
                "info",
                class_name="text-blue-400 hover:text-blue-600 transition-colors cursor-help",
                size=16,
            ),
            class_name="inline-flex items-center justify-center bg-blue-50 rounded-full p-1 ml-2",
        ),
        content=text,
        class_name="max-w-xs bg-gray-800 text-white text-xs p-2 rounded shadow-lg",
    )