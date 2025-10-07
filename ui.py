from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import jinja2
import streamlit as st


@dataclass(frozen=True)
class EditorCallbacks:
    """Callbacks used by the editor view."""

    on_save: Callable[[], None]
    on_load_example: Callable[[], None]
    on_delete: Callable[[], None]
    on_open_preview: Callable[[], None]


@dataclass(frozen=True)
class PreviewCallbacks:
    """Callbacks used by the preview view."""

    on_edit: Callable[[], None]
    on_load_example: Callable[[], None]


def render_data_editor(
    cv_data: Dict[str, Any],
    example_data: Dict[str, Any],
    callbacks: EditorCallbacks,
) -> None:
    """Render the CV data editor view."""

    header_cols = st.columns(4)
    header_cols[3].button(
        "Load Example Data",
        use_container_width=True,
        key="btn_load_example_editor",
        on_click=callbacks.on_load_example,
    )


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


def render_personal_info(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render personal information section."""

    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    example = example_data or {}

    col1, col2, col3 = st.columns(3)
    with col1:
        cv_data["name"] = st.text_input(
            "Full Name",
            value=cv_data.get("name", ""),
            placeholder=example.get("name", "Your full name"),
            key="input_name",
        )
        cv_data["role"] = st.text_input(
            "Current Role",
            value=cv_data.get("role", ""),
            placeholder=example.get("role", "Software Engineer"),
            key="input_role",
        )
    with col2:
        cv_data["email"] = st.text_input(
            "Email",
            value=cv_data.get("email", ""),
            placeholder=example.get("email", "your.email@example.com"),
            key="input_email",
        )
        cv_data["phone"] = st.text_input(
            "Phone",
            value=cv_data.get("phone", ""),
            placeholder=example.get("phone", "+1 555 555 5555"),
            key="input_phone",
        )
    with col3:
        cv_data["location"] = st.text_input(
            "Location",
            value=cv_data.get("location", ""),
            placeholder=example.get("location", "City, Country"),
            key="input_location",
        )


def render_social_networks(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render social networks section."""

    st.markdown('<div class="section-header">Social Networks</div>', unsafe_allow_html=True)
    socials = cv_data.setdefault("social_networks", [])
    example_socials = example_data.get("social_networks", []) if example_data else []

    if st.button("Add Social Network", key="btn_add_social"):
        socials.append({"network": "", "username": "", "url": ""})

    remove_idx: Optional[int] = None
    for idx, social in enumerate(socials):
        with st.expander(f"Social Network {idx + 1}", expanded=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            example_item = example_socials[idx] if idx < len(example_socials) else {}
            with col1:
                social["network"] = st.text_input(
                    "Network",
                    value=social.get("network", ""),
                    placeholder=example_item.get("network", "LinkedIn"),
                    key=f"input_social_network_{idx}",
                )
            with col2:
                social["username"] = st.text_input(
                    "Username",
                    value=social.get("username", ""),
                    placeholder=example_item.get("username", "your_username"),
                    key=f"input_social_username_{idx}",
                )
            with col3:
                if st.button("Remove", key=f"btn_remove_social_{idx}"):
                    remove_idx = idx
            social["url"] = st.text_input(
                "URL/Link",
                value=social.get("url", ""),
                placeholder=example_item.get("url", "https://linkedin.com/in/username"),
                key=f"input_social_url_{idx}",
            )
    if remove_idx is not None and 0 <= remove_idx < len(socials):
        socials.pop(remove_idx)


def _normalize_section_key(sections: Dict[str, Any], preferred: str, legacy: str) -> List[Any]:
    """Return a list for a section key, migrating legacy keys when needed."""

    if preferred not in sections and legacy in sections:
        sections[preferred] = sections.pop(legacy) or []
    value = sections.setdefault(preferred, [])
    if not isinstance(value, list):
        value = [value] if value else []
        sections[preferred] = value
    return value


def render_about_me(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render About Me section."""

    st.markdown('<div class="section-header">About Me</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    about_list = _normalize_section_key(sections, "aboutme", "AboutMe")
    example_sections = example_data.get("sections", {}) if example_data else {}
    example_about = "\n".join(example_sections.get("aboutme") or example_sections.get("AboutMe") or [])

    about_text = st.text_area(
        "Personal description",
        value="\n".join(about_list).strip(),
        height=150,
        placeholder=example_about or "Write a brief description about yourself...",
        key="textarea_about",
    )

    cleaned = about_text.strip()
    sections["aboutme"] = [cleaned] if cleaned else []


def render_education(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render education section."""

    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    educations = sections.setdefault("education", [])
    example_educations = example_data.get("sections", {}).get("education", []) if example_data else []

    if st.button("Add Education", key="btn_add_education"):
        educations.append(
            {
                "institution": "",
                "location": "",
                "area": "",
                "degree": "",
                "start_date": "",
                "end_date": "",
                "grade": "",
                "highlights": [],
            }
        )

    remove_idx: Optional[int] = None
    for idx, edu in enumerate(educations):
        with st.expander(f"Education {idx + 1}", expanded=True):
            example_item = example_educations[idx] if idx < len(example_educations) else {}
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                edu["institution"] = st.text_input(
                    "Institution",
                    value=edu.get("institution", ""),
                    placeholder=example_item.get("institution", ""),
                    key=f"input_edu_institution_{idx}",
                )
                edu["area"] = st.text_input(
                    "Field of Study",
                    value=edu.get("area", ""),
                    placeholder=example_item.get("area", ""),
                    key=f"input_edu_area_{idx}",
                )
            with col2:
                edu["location"] = st.text_input(
                    "Location",
                    value=edu.get("location", ""),
                    placeholder=example_item.get("location", ""),
                    key=f"input_edu_location_{idx}",
                )
                edu["degree"] = st.text_input(
                    "Degree",
                    value=edu.get("degree", ""),
                    placeholder=example_item.get("degree", ""),
                    key=f"input_edu_degree_{idx}",
                )
            with col3:
                if st.button("Remove", key=f"btn_remove_education_{idx}"):
                    remove_idx = idx

            col4, col5, col6 = st.columns(3)
            with col4:
                edu["start_date"] = st.text_input(
                    "Start Date",
                    value=edu.get("start_date", ""),
                    placeholder=example_item.get("start_date", "2020-09"),
                    key=f"input_edu_start_{idx}",
                )
            with col5:
                edu["end_date"] = st.text_input(
                    "End Date",
                    value=edu.get("end_date", ""),
                    placeholder=example_item.get("end_date", "Present"),
                    key=f"input_edu_end_{idx}",
                )
            with col6:
                edu["grade"] = st.text_input(
                    "Grade/GPA",
                    value=edu.get("grade", ""),
                    placeholder=example_item.get("grade", ""),
                    key=f"input_edu_grade_{idx}",
                )

            highlights_text = st.text_area(
                "Highlights",
                value="\n".join(edu.get("highlights", [])),
                height=100,
                placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_edu_highlights_{idx}",
            )
            edu["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(educations):
        educations.pop(remove_idx)


def render_experience(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render professional experience section."""

    st.markdown('<div class="section-header">Professional Experience</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    experiences = sections.setdefault("experience", [])
    example_experiences = (
        example_data.get("sections", {}).get("experience", []) if example_data else []
    )

    if st.button("Add Experience", key="btn_add_experience"):
        experiences.append(
            {
                "company": "",
                "position": "",
                "location": "",
                "start_date": "",
                "end_date": "",
                "highlights": [],
            }
        )

    remove_idx: Optional[int] = None
    for idx, exp in enumerate(experiences):
        with st.expander(f"Experience {idx + 1}", expanded=True):
            example_item = example_experiences[idx] if idx < len(example_experiences) else {}
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                exp["company"] = st.text_input(
                    "Company",
                    value=exp.get("company", ""),
                    placeholder=example_item.get("company", ""),
                    key=f"input_exp_company_{idx}",
                )
                exp["location"] = st.text_input(
                    "Location",
                    value=exp.get("location", ""),
                    placeholder=example_item.get("location", ""),
                    key=f"input_exp_location_{idx}",
                )
            with col2:
                exp["position"] = st.text_input(
                    "Role",
                    value=exp.get("position", ""),
                    placeholder=example_item.get("position", ""),
                    key=f"input_exp_position_{idx}",
                )
            with col3:
                if st.button("Remove", key=f"btn_remove_experience_{idx}"):
                    remove_idx = idx

            col4, col5 = st.columns(2)
            with col4:
                exp["start_date"] = st.text_input(
                    "Start Date",
                    value=exp.get("start_date", ""),
                    placeholder=example_item.get("start_date", ""),
                    key=f"input_exp_start_{idx}",
                )
            with col5:
                exp["end_date"] = st.text_input(
                    "End Date",
                    value=exp.get("end_date", ""),
                    placeholder=example_item.get("end_date", ""),
                    key=f"input_exp_end_{idx}",
                )

            highlights_text = st.text_area(
                "Responsibilities & Achievements",
                value="\n".join(exp.get("highlights", [])),
                height=120,
                placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_exp_highlights_{idx}",
            )
            exp["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(experiences):
        experiences.pop(remove_idx)


def render_projects(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render projects section."""

    st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    projects = sections.setdefault("projects", [])
    example_projects = example_data.get("sections", {}).get("projects", []) if example_data else []

    if st.button("Add Project", key="btn_add_project"):
        projects.append(
            {
                "name": "",
                "url": "",
                "start_date": "",
                "end_date": "",
                "summary": "",
                "highlights": [],
            }
        )

    remove_idx: Optional[int] = None
    for idx, proj in enumerate(projects):
        with st.expander(f"Project {idx + 1}", expanded=True):
            example_item = example_projects[idx] if idx < len(example_projects) else {}
            col1, col2 = st.columns([4, 1])
            with col1:
                proj["name"] = st.text_input(
                    "Project Name",
                    value=proj.get("name", ""),
                    placeholder=example_item.get("name", ""),
                    key=f"input_project_name_{idx}",
                )
            with col2:
                if st.button("Remove", key=f"btn_remove_project_{idx}"):
                    remove_idx = idx

            proj["url"] = st.text_input(
                "Project URL/Link",
                value=proj.get("url", ""),
                placeholder=example_item.get("url", "https://github.com/user/project"),
                key=f"input_project_url_{idx}",
            )

            col3, col4 = st.columns(2)
            with col3:
                proj["start_date"] = st.text_input(
                    "Start Date",
                    value=proj.get("start_date", ""),
                    placeholder=example_item.get("start_date", ""),
                    key=f"input_project_start_{idx}",
                )
            with col4:
                proj["end_date"] = st.text_input(
                    "End Date",
                    value=proj.get("end_date", ""),
                    placeholder=example_item.get("end_date", ""),
                    key=f"input_project_end_{idx}",
                )

            proj["summary"] = st.text_area(
                "Summary",
                value=proj.get("summary", ""),
                height=80,
                placeholder=example_item.get("summary", ""),
                key=f"textarea_project_summary_{idx}",
            )

            highlights_text = st.text_area(
                "Highlights",
                value="\n".join(proj.get("highlights", [])),
                height=100,
                placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_project_highlights_{idx}",
            )
            proj["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(projects):
        projects.pop(remove_idx)

def render_publications(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render publications section."""

    st.markdown('<div class="section-header">Publications</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    publications = _normalize_section_key(sections, "publications", "Publications")
    example_sections = example_data.get("sections", {}) if example_data else {}
    example_publications = example_sections.get("publications", [])

    if st.button("Add Publication", key="btn_add_publication"):
        publications.append(
            {
                "title": "",
                "venue": "",
                "authors": [],
                "doi": "",
                "date": "",
            }
        )

    remove_idx: Optional[int] = None
    for idx, pub in enumerate(publications):
        with st.expander(f"Publication {idx + 1}", expanded=True):
            example_item = example_publications[idx] if idx < len(example_publications) else {}
            col1, col2 = st.columns([4, 1])
            with col1:
                pub["title"] = st.text_input(
                    "Title",
                    value=pub.get("title", ""),
                    placeholder=example_item.get("title", ""),
                    key=f"input_publication_title_{idx}",
                )
            with col2:
                if st.button("Remove", key=f"btn_remove_publication_{idx}"):
                    remove_idx = idx

            col3, col4 = st.columns([3, 2])
            with col3:
                pub["venue"] = st.text_input(
                    "Venue",
                    value=pub.get("venue", ""),
                    placeholder=example_item.get("venue", ""),
                    key=f"input_publication_venue_{idx}",
                )
            with col4:
                pub["date"] = st.text_input(
                    "Date",
                    value=pub.get("date", ""),
                    placeholder=example_item.get("date", ""),
                    key=f"input_publication_date_{idx}",
                )

            pub["doi"] = st.text_input(
                "DOI or Identifier",
                value=pub.get("doi", ""),
                placeholder=example_item.get("doi", ""),
                key=f"input_publication_doi_{idx}",
            )

            authors_text = st.text_area(
                "Authors (one per line)",
                value="\n".join(pub.get("authors", [])),
                height=100,
                placeholder="\n".join(example_item.get("authors", [])),
                key=f"textarea_publication_authors_{idx}",
            )
            pub["authors"] = [line.strip() for line in authors_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(publications):
        publications.pop(remove_idx)


def render_skills(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    """Render skills section."""

    st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    skills = sections.setdefault("skills", [])
    example_skills = example_data.get("sections", {}).get("skills", []) if example_data else []

    if st.button("Add Skill Category", key="btn_add_skill"):
        skills.append({"label": "", "details": ""})

    remove_idx: Optional[int] = None
    for idx, skill in enumerate(skills):
        with st.expander(f"Skill {idx + 1}", expanded=True):
            example_item = example_skills[idx] if idx < len(example_skills) else {}
            col1, col2 = st.columns([4, 1])
            with col1:
                skill["label"] = st.text_input(
                    "Category",
                    value=skill.get("label", ""),
                    placeholder=example_item.get("label", ""),
                    key=f"input_skill_label_{idx}",
                )
            with col2:
                if st.button("Remove", key=f"btn_remove_skill_{idx}"):
                    remove_idx = idx

            skill["details"] = st.text_area(
                "Details",
                value=skill.get("details", ""),
                height=80,
                placeholder=example_item.get("details", ""),
                key=f"textarea_skill_details_{idx}",
            )

    if remove_idx is not None and 0 <= remove_idx < len(skills):
        skills.pop(remove_idx)


def render_cv_preview(
    cv_data: Dict[str, Any],
    example_data: Dict[str, Any],
    _: PreviewCallbacks,
) -> None:
    """Render CV preview with granular item selection and generation."""

    data_to_use = cv_data if cv_data else example_data
    
    if not data_to_use or not data_to_use.get("name"):
        st.warning("No CV data available. Please fill in the Data Editor tab first.")
        return
        
    # Get available templates
    templates = get_available_templates()
    template_names = [t["name"] for t in templates]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_template = st.selectbox(
            "Choose a template",
            template_names,
            key="template_selector"
        )
        
        st.markdown("---")
        st.markdown("### Select Content to Include")
        
        sections_data = data_to_use.get("sections", {})
        
        # About Me Section
        include_aboutme = st.checkbox("About Me", value=bool(sections_data.get("aboutme")), key="include_aboutme")
        
        # Experience Section with individual selection
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
        
        # Education Section with individual selection
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
        
        # Projects Section with individual selection
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
        
        # Publications Section with individual selection
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
        
        # Skills Section with individual selection
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
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_html = st.button("Generate HTML", use_container_width=True, type="primary")
        with col_btn2:
            generate_pdf = st.button("Generate PDF", use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='text-align: center;'>Template Preview</h3>", unsafe_allow_html=True)
        
        # Build filtered data based on selections
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
        
        # Generate preview
        template_path = next((t["path"] for t in templates if t["name"] == selected_template), None)
        if template_path:
            html_content = generate_html_cv(filtered_data, template_path)
            if html_content:
                st.components.v1.html(html_content, height=900, scrolling=True)
    
    # Handle generation
    if generate_html or generate_pdf:
        template_path = next((t["path"] for t in templates if t["name"] == selected_template), None)
        if not template_path:
            st.error("Template not found!")
            return
            
        html_content = generate_html_cv(filtered_data, template_path)
        if not html_content:
            st.error("Failed to generate CV!")
            return
        
        output_dir = Path("data") / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if generate_html:
            html_file = output_dir / "cv.html"
            html_file.write_text(html_content, encoding="utf-8")
            st.success("HTML generated successfully!")
            st.markdown(get_html_download_link(html_content, "cv.html"), unsafe_allow_html=True)
        
        if generate_pdf:
            try:
                from weasyprint import HTML
                pdf_file = output_dir / "cv.pdf"
                HTML(string=html_content).write_pdf(pdf_file)
                st.success("PDF generated successfully!")
                
                # Provide download link
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()
                    b64_pdf = base64.b64encode(pdf_bytes).decode()
                    st.markdown(
                        f'<a href="data:application/pdf;base64,{b64_pdf}" download="cv.pdf">Download PDF</a>',
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.error(f"Failed to generate PDF: {e}")
                st.info("Make sure weasyprint dependencies are installed. See README for instructions.")


def render_compact_preview(data: Dict[str, Any]) -> None:
    """Render a simplified textual preview of the CV data."""

    st.markdown("### CV Data")
    if not data:
        st.info("No data to display. Start by filling in the editor or load the example data.")
        return

    st.markdown(f"# {data.get('name', 'Your Name')}")
    if data.get("role"):
        st.markdown(f"### {data['role']}")
    contact_info = []
    if data.get("email"):
        contact_info.append(f"Email: {data['email']}")
    if data.get("phone"):
        contact_info.append(f"Tel: {data['phone']}")
    if data.get("location"):
        contact_info.append(f"Location: {data['location']}")
    if contact_info:
        st.markdown(" | ".join(contact_info))

    if data.get("social_networks"):
        st.markdown("**Links:**")
        for social in data["social_networks"]:
            if social.get("network") and social.get("url"):
                st.markdown(f"• {social['network']}: {social['url']}")

    st.markdown("---")
    sections = data.get("sections", {})

    about_me = sections.get("aboutme") or sections.get("AboutMe", [])
    if about_me:
        st.markdown("## About Me")
        for paragraph in about_me:
            if paragraph:
                st.markdown(paragraph)
        st.markdown("")

    education = sections.get("education", [])
    if education:
        st.markdown("## Education")
        for edu in education:
            if not edu.get("institution"):
                continue
            st.markdown(f"**{edu.get('degree', '')} in {edu.get('area', '')}**")
            st.markdown(f"*{edu.get('institution', '')}* - {edu.get('location', '')}")
            period = " - ".join(filter(None, [edu.get("start_date"), edu.get("end_date")]))
            if period:
                st.markdown(f"Period: {period}")
            if edu.get("grade"):
                st.markdown(f"Grade: {edu['grade']}")
            for highlight in edu.get("highlights", []):
                if highlight:
                    st.markdown(f"• {highlight}")
            st.markdown("")

    experience = sections.get("experience", [])
    if experience:
        st.markdown("## Professional Experience")
        for exp in experience:
            if not exp.get("company"):
                continue
            st.markdown(f"**{exp.get('position', '')}**")
            st.markdown(f"*{exp.get('company', '')}* - {exp.get('location', '')}")
            period = " - ".join(filter(None, [exp.get("start_date"), exp.get("end_date")]))
            if period:
                st.markdown(f"Period: {period}")
            for highlight in exp.get("highlights", []):
                if highlight:
                    st.markdown(f"• {highlight}")
            st.markdown("")

    projects = sections.get("projects", [])
    if projects:
        st.markdown("## Projects")
        for proj in projects:
            if not proj.get("name"):
                continue
            st.markdown(f"**{proj['name']}**")
            period = " - ".join(filter(None, [proj.get("start_date"), proj.get("end_date")]))
            if period:
                st.markdown(f"Period: {period}")
            if proj.get("summary"):
                st.markdown(proj["summary"])
            for highlight in proj.get("highlights", []):
                if highlight:
                    st.markdown(f"• {highlight}")
            st.markdown("")

    publications = sections.get("publications") or sections.get("Publications", [])
    if publications:
        st.markdown("## Publications")
        for pub in publications:
            if not pub.get("title"):
                continue
            title_line = f"**{pub['title']}**"
            if pub.get("venue"):
                title_line += f" — *{pub['venue']}*"
            st.markdown(title_line)
            meta_parts = []
            if pub.get("date"):
                meta_parts.append(pub["date"])
            if pub.get("doi"):
                meta_parts.append(f"DOI: {pub['doi']}")
            if meta_parts:
                st.markdown(", ".join(meta_parts))
            if pub.get("authors"):
                st.markdown("Authors: " + ", ".join(pub["authors"]))
            st.markdown("")

    skills = sections.get("skills", [])
    if skills:
        st.markdown("## Skills")
        for skill in skills:
            if not skill.get("label"):
                continue
            st.markdown(f"**{skill['label']}:** {skill.get('details', '')}")


def get_available_templates() -> List[Dict[str, str]]:
    """Return available template metadata."""

    templates: List[Dict[str, str]] = [
        {"name": "Standard", "path": os.path.join("templates", "cv_template.html")}
    ]

    templates_dir = Path("templates") / "cv_templates"
    if templates_dir.exists():
        for file in sorted(templates_dir.iterdir()):
            if file.suffix.lower() == ".html":
                templates.append({"name": file.stem.capitalize(), "path": str(file)})

    return templates


def generate_html_cv(data: Dict[str, Any], template_path: str) -> Optional[str]:
    """Render the CV using the selected template."""

    try:
        template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path) or ".")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(os.path.basename(template_path))
        return template.render(**data)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Error generating the CV: {exc}")
        return None


def get_html_download_link(html_string: str, filename: str = "cv.html") -> str:
    """Create a download link for generated HTML."""

    b64 = base64.b64encode(html_string.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}">Download CV (HTML)</a>'


__all__ = [
    "EditorCallbacks",
    "PreviewCallbacks",
    "render_data_editor",
    "render_cv_preview",
    "get_available_templates",
]
