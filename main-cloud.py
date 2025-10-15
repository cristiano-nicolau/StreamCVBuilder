from __future__ import annotations

import copy
from typing import Optional, Tuple

import streamlit as st
from streamlit_option_menu import option_menu

import io
import base64
import yaml
from ui.__init__cloud__ import render_cv_preview, render_data_editor, render_cv_builder, EditorCallbacks, PreviewCallbacks
from utils.yaml_utils import load_example_data, dump_yaml_to_string, load_yaml_from_file

APP_TITLE = "CV Builder"
PAGE_ICON = "📄"
NAV_KEY = "view_mode"
DATA_KEY = "cv_data"
EXAMPLE_KEY = "example_data"
FEEDBACK_KEY = "app_feedback"
DEFAULT_VIEW = "Data Editor"
PREVIEW_VIEW = "CV Generator"
CV_BUILDER_VIEW = "CV Builder"
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
    div[data-testid="stHorizontalBlock"] .nav.nav-pills {
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .nav.nav-pills .nav-link {
        border-radius: 0;
        margin: 0 0.4rem;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        border: 1px solid #3498db33;
        background-color: #f0f3f7;
    }
    .nav.nav-pills .nav-link.active {
        background-color: #3498db;
        color: #fff;
        border-color: #3498db;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.35);
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
        st.session_state[DATA_KEY] = {}
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

    # Show a toast notification first
    st.toast(message, icon="✅" if level == "success" else "⚠️" if level == "warning" else "ℹ️")

    # Then show the regular feedback message
    notifier = getattr(st, level, st.info)
    notifier(message)

def handle_save() -> None:
    """Save current CV data to session state."""
    # This function is no longer used but kept for compatibility
    pass

def handle_load_example() -> None:
    """Replace current data with the example dataset."""

    st.session_state[DATA_KEY] = copy.deepcopy(st.session_state.get(EXAMPLE_KEY, {}))
    push_feedback("info", "Example data loaded.")

def handle_download() -> None:
    """Download current CV data as YAML file."""
    data = st.session_state.get(DATA_KEY, {})
    # Consider data empty if all fields are empty or lists are empty
    def is_data_empty(data):
        if not data:
            return True
        for k, v in data.items():
            if isinstance(v, dict):
                if not is_data_empty(v):
                    return False
            elif isinstance(v, list):
                if any(v):
                    return False
            elif v not in ("", None):
                return False
        return True

    if is_data_empty(data):
        data = copy.deepcopy(st.session_state.get(EXAMPLE_KEY, {}))

    yaml_str = dump_yaml_to_string(data)
    st.download_button(
        label="Download CV Data",
        data=yaml_str,
        file_name="cv_data.yaml",
        mime="application/x-yaml",
        use_container_width=True
    )

def handle_upload() -> None:
    """Upload CV data from YAML file."""
    uploaded_file = st.file_uploader("Choose a YAML file", type=['yaml', 'yml'], key="cv_data_upload")
    if uploaded_file is not None:
        data = load_yaml_from_file(uploaded_file)
        if data:
            # primeiro elimina tudo
            st.session_state[DATA_KEY] = {}
            st.session_state[DATA_KEY] = data
            st.session_state['show_upload_modal'] = False
            push_feedback("success", "Data uploaded successfully.")
            st.rerun()
        else:
            push_feedback("error", "Unable to load uploaded file. Please check the file format.")

def handle_delete_all() -> None:
    """Clear all data from session state."""
    st.session_state[DATA_KEY] = {}
    push_feedback("success", "All data has been removed.")

def handle_change_view(view: str) -> None:
    """Switch between available views."""

    st.session_state[NAV_KEY] = view

def render_tab_navigation() -> None:
    """Render the top-level tab navigation."""

    options = [DEFAULT_VIEW, PREVIEW_VIEW, CV_BUILDER_VIEW]
    icons = ["pencil-square", "file-earmark-text", "kanban"]
    default_index = options.index(st.session_state[NAV_KEY])
    selected_view = option_menu(
        None,
        options,
        icons=icons,
        menu_icon="list",
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "nav-link": {"text-align": "center"},
            "nav-link-selected": {
                "background-color": "#4D4F51",
                "color": "white",
            },
        },
        key="main_navigation",
    )

    if selected_view != st.session_state[NAV_KEY]:
        handle_change_view(selected_view)

def main() -> None:
    """Application entry point."""

    configure_page()
    ensure_session_state()
    display_feedback()
    st.markdown("## " + APP_TITLE, unsafe_allow_html=True)
    st.markdown("Create and customize your CV using predefined templates.")
    st.markdown("Put your data in the editor tab and generate a preview or download your CV in the CV Generator tab, or build it step by step in the CV Builder tab.")
    render_tab_navigation()

    editor_callbacks = EditorCallbacks(
        on_save=handle_save,
        on_load_example=handle_load_example,
        on_delete=handle_delete_all,
        on_open_preview=lambda: handle_change_view(PREVIEW_VIEW),
        on_download=handle_download,
        on_upload=handle_upload,
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
    elif st.session_state[NAV_KEY] == CV_BUILDER_VIEW:
        render_cv_builder(
            st.session_state[DATA_KEY],
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