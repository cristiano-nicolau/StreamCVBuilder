from __future__ import annotations

from typing import Any, Dict

import streamlit as st

DATA_KEY = "cv_data"

from .callbacks_cloud import EditorCallbacks, PreviewCallbacks
from .cv_builder import render_cv_builder
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
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Upload Data", use_container_width=True, key="btn_upload"):
            st.session_state['show_upload_modal'] = True
            
    with col2:
        callbacks.on_download()
    
    with col3:
        st.button(
            "Delete All Data",
            use_container_width=True,
            key="btn_delete_all",
            on_click=callbacks.on_delete,
        )
    
    # Upload Modal
    if 'show_upload_modal' not in st.session_state:
        st.session_state['show_upload_modal'] = False
        
    if st.session_state['show_upload_modal']:
        with st.expander("Upload CV Data", expanded=True):
            callbacks.on_upload()
            if st.button("Close"):
                st.session_state['show_upload_modal'] = False


__all__ = [
    "EditorCallbacks",
    "PreviewCallbacks",
    "render_data_editor",
    "render_cv_preview",
    "render_cv_builder",
    "get_available_templates",
    "generate_html_cv",
]