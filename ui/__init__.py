from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from .callbacks import EditorCallbacks, PreviewCallbacks
from .editor_sections import (
    render_about_me,
    render_education,
    render_experience,
    render_personal_info,
    render_projects,
    render_publications,
    render_skills,
    render_social_networks,
)
from .preview import render_cv_preview
from .templates import generate_html_cv, get_available_templates


def render_data_editor(
    cv_data: Dict[str, Any],
    example_data: Dict[str, Any],
    callbacks: EditorCallbacks,
) -> None:
    render_personal_info(cv_data, example_data)
    render_social_networks(cv_data, example_data)
    render_about_me(cv_data, example_data)
    render_education(cv_data, example_data)
    render_experience(cv_data, example_data)
    render_projects(cv_data, example_data)
    render_publications(cv_data, example_data)
    render_skills(cv_data, example_data)

    st.markdown("---")
    footer_cols = st.columns(2)
    footer_cols[0].button(
        "Save All Data",
        use_container_width=True,
        key="btn_save_all",
        on_click=callbacks.on_save,
    )
    footer_cols[1].button(
        "Delete All Data",
        use_container_width=True,
        key="btn_delete_all",
        on_click=callbacks.on_delete,
    )


__all__ = [
    "EditorCallbacks",
    "PreviewCallbacks",
    "render_data_editor",
    "render_cv_preview",
    "get_available_templates",
    "generate_html_cv",
]
