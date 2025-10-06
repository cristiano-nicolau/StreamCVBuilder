from __future__ import annotations

import copy
from typing import Optional, Tuple

import streamlit as st

from ui import EditorCallbacks, PreviewCallbacks, render_cv_preview, render_data_editor
from utils.yaml_utils import load_example_data, load_user_data, save_user_data

APP_TITLE = "CV Generator"
PAGE_ICON = "📄"
NAV_KEY = "view_mode"
DATA_KEY = "cv_data"
EXAMPLE_KEY = "example_data"
FEEDBACK_KEY = "app_feedback"
DEFAULT_VIEW = "Data Editor"
PREVIEW_VIEW = "CV Preview"
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.4rem;
    }
    button.st-emotion-cache-1ctn9vp.ef3psqc11 {
        background-color: #e74c3c;
    }
    button.st-emotion-cache-19rxjzo.ef3psqc11 {
        background-color: #2ecc71;
    }
</style>
"""

def configure_page() -> None:
    """Configure global page options and styles."""

    st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def ensure_session_state() -> None:
    """Ensure required session state entries exist."""

    st.session_state.setdefault(EXAMPLE_KEY, load_example_data() or {})
    if DATA_KEY not in st.session_state:
        stored = load_user_data()
        st.session_state[DATA_KEY] = stored if stored else {}
    st.session_state.setdefault(NAV_KEY, DEFAULT_VIEW)
    st.session_state.setdefault(FEEDBACK_KEY, None)

def push_feedback(level: str, message: str) -> None:
    """Store feedback for display after the rerun triggered by Streamlit."""

    st.session_state[FEEDBACK_KEY] = (level, message)

def display_feedback() -> None:
    """Display feedback messages when available."""

    feedback: Optional[Tuple[str, str]] = st.session_state.get(FEEDBACK_KEY)
    if not feedback:
        return

    level, message = feedback
    st.session_state[FEEDBACK_KEY] = None
    notifier = getattr(st, level, st.info)
    notifier(message)

def handle_save() -> None:
    """Persist current CV data to disk."""

    success = save_user_data(st.session_state[DATA_KEY])
    if success:
        push_feedback("success", "Data saved successfully.")
    else:
        push_feedback("error", "Unable to save data. Please try again.")

def handle_load_example() -> None:
    """Replace current data with the example dataset."""

    st.session_state[DATA_KEY] = copy.deepcopy(st.session_state.get(EXAMPLE_KEY, {}))
    push_feedback("info", "Example data loaded.")

def handle_delete_all() -> None:
    """Clear all data from session and persistent storage."""

    st.session_state[DATA_KEY] = {}
    save_user_data({})
    push_feedback("success", "All data has been removed.")

def handle_change_view(view: str) -> None:
    """Switch between available views."""

    st.session_state[NAV_KEY] = view

def render_sidebar_navigation() -> None:
    """Render navigation controls inside the sidebar."""

    options = [DEFAULT_VIEW, PREVIEW_VIEW]
    default_index = options.index(st.session_state[NAV_KEY])
    selected_view = st.sidebar.radio(
        "Navigation",
        options=options,
        index=default_index,
        key="sidebar_navigation",
    )
    if selected_view != st.session_state[NAV_KEY]:
        handle_change_view(selected_view)

def main() -> None:
    """Application entry point."""

    configure_page()
    ensure_session_state()
    display_feedback()
    render_sidebar_navigation()

    editor_callbacks = EditorCallbacks(
        on_save=handle_save,
        on_load_example=handle_load_example,
        on_delete=handle_delete_all,
        on_open_preview=lambda: handle_change_view(PREVIEW_VIEW),
    )

    preview_callbacks = PreviewCallbacks(
        on_edit=lambda: handle_change_view(DEFAULT_VIEW),
        on_load_example=handle_load_example,
    )

    if st.session_state[NAV_KEY] == DEFAULT_VIEW:
        render_data_editor(
            st.session_state[DATA_KEY],
            st.session_state[EXAMPLE_KEY],
            editor_callbacks,
        )
    else:
        render_cv_preview(
            st.session_state[DATA_KEY],
            st.session_state[EXAMPLE_KEY],
            preview_callbacks,
        )


if __name__ == "__main__":
    main()