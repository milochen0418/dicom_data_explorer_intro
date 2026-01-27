import reflex as rx
from dicom_data_explorer_intro.components.sidebar import sidebar
from dicom_data_explorer_intro.components.onboarding import onboarding_modal


def layout(content: rx.Component) -> rx.Component:
    """Main layout wrapper with sidebar and onboarding."""
    return rx.el.div(
        sidebar(),
        rx.el.main(content, class_name="flex-1 h-full overflow-y-auto bg-gray-50"),
        onboarding_modal(),
        class_name="flex h-screen w-screen overflow-hidden font-['Inter'] text-gray-900",
    )