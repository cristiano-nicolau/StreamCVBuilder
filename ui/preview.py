from __future__ import annotations

import base64
from typing import Any, Dict

import streamlit as st

from .callbacks import PreviewCallbacks
from .templates import generate_html_cv, get_available_templates
from .pdf_generator import html_to_pdf_bytes


def render_cv_preview(
    cv_data: Dict[str, Any],
    example_data: Dict[str, Any],
    callbacks: PreviewCallbacks,
) -> None:
    data_to_use = cv_data if cv_data else example_data
    has_user_data = cv_data and cv_data.get("name")
    
    if not data_to_use or not data_to_use.get("name"):
        st.warning("No CV data available. Please fill in the Data Editor tab or load example data.")
        if st.button("Load Example Data", use_container_width=True, type="primary"):
            callbacks.on_load_example()
            st.rerun()
        return
        
    templates = get_available_templates()
    template_names = [t["name"] for t in templates]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_template = st.selectbox("Choose a template", template_names, key="template_selector")
        
        st.markdown("---")
        st.markdown("### Select Content to Include")
        
        sections_data = data_to_use.get("sections", {})
        
        include_aboutme = st.checkbox("About Me", value=bool(sections_data.get("aboutme")), key="include_aboutme")
        
        experience_list = sections_data.get("experience", [])
        if experience_list:
            include_experience = st.checkbox(f"Experience ({len(experience_list)} items)", value=True, key="include_experience")
            selected_experience_indices = []
            if include_experience:
                with st.expander("Select specific experiences"):
                    for idx, exp in enumerate(experience_list):
                        exp_label = f"{exp.get('position', 'Position')} @ {exp.get('company', 'Company')}"
                        if st.checkbox(exp_label, value=True, key=f"exp_select_{idx}"):
                            selected_experience_indices.append(idx)
        else:
            include_experience = False
            selected_experience_indices = []
        
        education_list = sections_data.get("education", [])
        if education_list:
            include_education = st.checkbox(f"Education ({len(education_list)} items)", value=True, key="include_education")
            selected_education_indices = []
            if include_education:
                with st.expander("Select specific education"):
                    for idx, edu in enumerate(education_list):
                        edu_label = f"{edu.get('degree', 'Degree')} @ {edu.get('institution', 'Institution')}"
                        if st.checkbox(edu_label, value=True, key=f"edu_select_{idx}"):
                            selected_education_indices.append(idx)
        else:
            include_education = False
            selected_education_indices = []
        
        projects_list = sections_data.get("projects", [])
        if projects_list:
            include_projects = st.checkbox(f"Projects ({len(projects_list)} items)", value=True, key="include_projects")
            selected_projects_indices = []
            if include_projects:
                with st.expander("Select specific projects"):
                    for idx, proj in enumerate(projects_list):
                        proj_label = proj.get('name', f'Project {idx+1}')
                        if st.checkbox(proj_label, value=True, key=f"proj_select_{idx}"):
                            selected_projects_indices.append(idx)
        else:
            include_projects = False
            selected_projects_indices = []
        
        publications_list = sections_data.get("publications", [])
        if publications_list:
            include_publications = st.checkbox(f"Publications ({len(publications_list)} items)", value=True, key="include_publications")
            selected_publications_indices = []
            if include_publications:
                with st.expander("Select specific publications"):
                    for idx, pub in enumerate(publications_list):
                        pub_label = pub.get('title', f'Publication {idx+1}')
                        if st.checkbox(pub_label, value=True, key=f"pub_select_{idx}"):
                            selected_publications_indices.append(idx)
        else:
            include_publications = False
            selected_publications_indices = []
        
        skills_list = sections_data.get("skills", [])
        if skills_list:
            include_skills = st.checkbox(f"Skills ({len(skills_list)} items)", value=True, key="include_skills")
            selected_skills_indices = []
            if include_skills:
                with st.expander("Select specific skills"):
                    for idx, skill in enumerate(skills_list):
                        skill_label = skill.get('label', f'Skill {idx+1}')
                        if st.checkbox(skill_label, value=True, key=f"skill_select_{idx}"):
                            selected_skills_indices.append(idx)
        else:
            include_skills = False
            selected_skills_indices = []
        
        st.markdown("---")
        
        generate_html = False
        generate_pdf = False
        
        if not has_user_data:
            if st.button("Load Example Data", use_container_width=True, type="primary", key="load_example_sidebar"):
                callbacks.on_load_example()
                st.rerun()
        else:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                generate_html = st.button("Generate HTML", use_container_width=True, type="primary")
            with col_btn2:
                generate_pdf = st.button("Generate PDF", use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='text-align: center;'>Template Preview</h3>", unsafe_allow_html=True)
        
        filtered_data = data_to_use.copy()
        filtered_sections = {}
        
        if include_aboutme and sections_data.get("aboutme"):
            filtered_sections["aboutme"] = sections_data["aboutme"]
        
        if include_experience and selected_experience_indices:
            filtered_sections["experience"] = [experience_list[i] for i in selected_experience_indices]
        
        if include_education and selected_education_indices:
            filtered_sections["education"] = [education_list[i] for i in selected_education_indices]
        
        if include_projects and selected_projects_indices:
            filtered_sections["projects"] = [projects_list[i] for i in selected_projects_indices]
        
        if include_publications and selected_publications_indices:
            filtered_sections["publications"] = [publications_list[i] for i in selected_publications_indices]
        
        if include_skills and selected_skills_indices:
            filtered_sections["skills"] = [skills_list[i] for i in selected_skills_indices]
        
        filtered_data["sections"] = filtered_sections
        
        template_path = next((t["path"] for t in templates if t["name"] == selected_template), None)
        if template_path:
            html_content = generate_html_cv(filtered_data, template_path)
            if html_content:
                st.components.v1.html(html_content, height=900, scrolling=True)
    
    if has_user_data and (generate_html or generate_pdf):
        template_path = next((t["path"] for t in templates if t["name"] == selected_template), None)
        if not template_path:
            st.error("Template not found!")
            return
            
        html_content = generate_html_cv(filtered_data, template_path)
        if not html_content:
            st.error("Failed to generate CV!")
            return
        
        if generate_html:
            st.success("HTML generated successfully!")
            b64_html = base64.b64encode(html_content.encode()).decode()
            st.markdown(
                f'<a href="data:text/html;base64,{b64_html}" download="cv.html" style="display: inline-block; padding: 0.5rem 1rem; background-color: #0066cc; color: white; text-decoration: none; border-radius: 4px; font-weight: 500;">Download HTML</a>',
                unsafe_allow_html=True
            )
        
        if generate_pdf:
            # Prefer generating PDF from the rendered HTML of the selected template
            pdf_bytes = html_to_pdf_bytes(html_content)
            if pdf_bytes:
                st.success("PDF generated successfully!")
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                st.markdown(
                    f'<a href="data:application/pdf;base64,{b64_pdf}" download="cv.pdf" style="display: inline-block; padding: 0.5rem 1rem; background-color: #0066cc; color: white; text-decoration: none; border-radius: 4px; font-weight: 500;">Download PDF</a>',
                    unsafe_allow_html=True
                )
            else:
                st.error("Failed to convert HTML to PDF. Try a simpler template or export HTML.")

