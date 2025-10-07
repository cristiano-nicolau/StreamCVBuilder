from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st


def _normalize_section_key(sections: Dict[str, Any], preferred: str, legacy: str) -> List[Any]:
    if preferred not in sections and legacy in sections:
        sections[preferred] = sections.pop(legacy) or []
    value = sections.setdefault(preferred, [])
    if not isinstance(value, list):
        value = [value] if value else []
        sections[preferred] = value
    return value


def render_personal_info(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
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


def render_about_me(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
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
    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    educations = sections.setdefault("education", [])
    example_educations = example_data.get("sections", {}).get("education", []) if example_data else []

    if st.button("Add Education", key="btn_add_education"):
        educations.append({
            "institution": "", "location": "", "area": "", "degree": "",
            "start_date": "", "end_date": "", "grade": "", "highlights": []
        })

    remove_idx: Optional[int] = None
    for idx, edu in enumerate(educations):
        with st.expander(f"Education {idx + 1}", expanded=True):
            example_item = example_educations[idx] if idx < len(example_educations) else {}
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                edu["institution"] = st.text_input("Institution", value=edu.get("institution", ""),
                    placeholder=example_item.get("institution", ""), key=f"input_edu_institution_{idx}")
                edu["area"] = st.text_input("Field of Study", value=edu.get("area", ""),
                    placeholder=example_item.get("area", ""), key=f"input_edu_area_{idx}")
            with col2:
                edu["location"] = st.text_input("Location", value=edu.get("location", ""),
                    placeholder=example_item.get("location", ""), key=f"input_edu_location_{idx}")
                edu["degree"] = st.text_input("Degree", value=edu.get("degree", ""),
                    placeholder=example_item.get("degree", ""), key=f"input_edu_degree_{idx}")
            with col3:
                if st.button("Remove", key=f"btn_remove_education_{idx}"):
                    remove_idx = idx

            col4, col5, col6 = st.columns(3)
            with col4:
                edu["start_date"] = st.text_input("Start Date", value=edu.get("start_date", ""),
                    placeholder=example_item.get("start_date", "2020-09"), key=f"input_edu_start_{idx}")
            with col5:
                edu["end_date"] = st.text_input("End Date", value=edu.get("end_date", ""),
                    placeholder=example_item.get("end_date", "Present"), key=f"input_edu_end_{idx}")
            with col6:
                edu["grade"] = st.text_input("Grade/GPA", value=edu.get("grade", ""),
                    placeholder=example_item.get("grade", ""), key=f"input_edu_grade_{idx}")

            highlights_text = st.text_area("Highlights", value="\n".join(edu.get("highlights", [])),
                height=100, placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_edu_highlights_{idx}")
            edu["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(educations):
        educations.pop(remove_idx)


def render_experience(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    st.markdown('<div class="section-header">Professional Experience</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    experiences = sections.setdefault("experience", [])
    example_experiences = example_data.get("sections", {}).get("experience", []) if example_data else []

    if st.button("Add Experience", key="btn_add_experience"):
        experiences.append({
            "company": "", "position": "", "location": "",
            "start_date": "", "end_date": "", "highlights": []
        })

    remove_idx: Optional[int] = None
    for idx, exp in enumerate(experiences):
        with st.expander(f"Experience {idx + 1}", expanded=True):
            example_item = example_experiences[idx] if idx < len(example_experiences) else {}
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                exp["company"] = st.text_input("Company", value=exp.get("company", ""),
                    placeholder=example_item.get("company", ""), key=f"input_exp_company_{idx}")
                exp["location"] = st.text_input("Location", value=exp.get("location", ""),
                    placeholder=example_item.get("location", ""), key=f"input_exp_location_{idx}")
            with col2:
                exp["position"] = st.text_input("Role", value=exp.get("position", ""),
                    placeholder=example_item.get("position", ""), key=f"input_exp_position_{idx}")
            with col3:
                if st.button("Remove", key=f"btn_remove_experience_{idx}"):
                    remove_idx = idx

            col4, col5 = st.columns(2)
            with col4:
                exp["start_date"] = st.text_input("Start Date", value=exp.get("start_date", ""),
                    placeholder=example_item.get("start_date", ""), key=f"input_exp_start_{idx}")
            with col5:
                exp["end_date"] = st.text_input("End Date", value=exp.get("end_date", ""),
                    placeholder=example_item.get("end_date", ""), key=f"input_exp_end_{idx}")

            highlights_text = st.text_area("Responsibilities & Achievements",
                value="\n".join(exp.get("highlights", [])), height=120,
                placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_exp_highlights_{idx}")
            exp["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(experiences):
        experiences.pop(remove_idx)


def render_projects(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    projects = sections.setdefault("projects", [])
    example_projects = example_data.get("sections", {}).get("projects", []) if example_data else []

    if st.button("Add Project", key="btn_add_project"):
        projects.append({
            "name": "", "url": "", "start_date": "",
            "end_date": "", "summary": "", "highlights": []
        })

    remove_idx: Optional[int] = None
    for idx, proj in enumerate(projects):
        with st.expander(f"Project {idx + 1}", expanded=True):
            example_item = example_projects[idx] if idx < len(example_projects) else {}
            col1, col2 = st.columns([4, 1])
            with col1:
                proj["name"] = st.text_input("Project Name", value=proj.get("name", ""),
                    placeholder=example_item.get("name", ""), key=f"input_project_name_{idx}")
            with col2:
                if st.button("Remove", key=f"btn_remove_project_{idx}"):
                    remove_idx = idx

            proj["url"] = st.text_input("Project URL/Link", value=proj.get("url", ""),
                placeholder=example_item.get("url", "https://github.com/user/project"),
                key=f"input_project_url_{idx}")

            col3, col4 = st.columns(2)
            with col3:
                proj["start_date"] = st.text_input("Start Date", value=proj.get("start_date", ""),
                    placeholder=example_item.get("start_date", ""), key=f"input_project_start_{idx}")
            with col4:
                proj["end_date"] = st.text_input("End Date", value=proj.get("end_date", ""),
                    placeholder=example_item.get("end_date", ""), key=f"input_project_end_{idx}")

            proj["summary"] = st.text_area("Summary", value=proj.get("summary", ""),
                height=80, placeholder=example_item.get("summary", ""),
                key=f"textarea_project_summary_{idx}")

            highlights_text = st.text_area("Highlights", value="\n".join(proj.get("highlights", [])),
                height=100, placeholder="\n".join(example_item.get("highlights", [])),
                key=f"textarea_project_highlights_{idx}")
            proj["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(projects):
        projects.pop(remove_idx)


def render_publications(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
    st.markdown('<div class="section-header">Publications</div>', unsafe_allow_html=True)
    sections = cv_data.setdefault("sections", {})
    publications = _normalize_section_key(sections, "publications", "Publications")
    example_sections = example_data.get("sections", {}) if example_data else {}
    example_publications = example_sections.get("publications", [])

    if st.button("Add Publication", key="btn_add_publication"):
        publications.append({"title": "", "venue": "", "authors": [], "doi": "", "date": ""})

    remove_idx: Optional[int] = None
    for idx, pub in enumerate(publications):
        with st.expander(f"Publication {idx + 1}", expanded=True):
            example_item = example_publications[idx] if idx < len(example_publications) else {}
            col1, col2 = st.columns([4, 1])
            with col1:
                pub["title"] = st.text_input("Title", value=pub.get("title", ""),
                    placeholder=example_item.get("title", ""), key=f"input_publication_title_{idx}")
            with col2:
                if st.button("Remove", key=f"btn_remove_publication_{idx}"):
                    remove_idx = idx

            col3, col4 = st.columns([3, 2])
            with col3:
                pub["venue"] = st.text_input("Venue", value=pub.get("venue", ""),
                    placeholder=example_item.get("venue", ""), key=f"input_publication_venue_{idx}")
            with col4:
                pub["date"] = st.text_input("Date", value=pub.get("date", ""),
                    placeholder=example_item.get("date", ""), key=f"input_publication_date_{idx}")

            pub["doi"] = st.text_input("DOI or Identifier", value=pub.get("doi", ""),
                placeholder=example_item.get("doi", ""), key=f"input_publication_doi_{idx}")

            authors_text = st.text_area("Authors (one per line)",
                value="\n".join(pub.get("authors", [])), height=100,
                placeholder="\n".join(example_item.get("authors", [])),
                key=f"textarea_publication_authors_{idx}")
            pub["authors"] = [line.strip() for line in authors_text.splitlines() if line.strip()]

    if remove_idx is not None and 0 <= remove_idx < len(publications):
        publications.pop(remove_idx)


def render_skills(cv_data: Dict[str, Any], example_data: Dict[str, Any]) -> None:
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
                skill["label"] = st.text_input("Category", value=skill.get("label", ""),
                    placeholder=example_item.get("label", ""), key=f"input_skill_label_{idx}")
            with col2:
                if st.button("Remove", key=f"btn_remove_skill_{idx}"):
                    remove_idx = idx

            skill["details"] = st.text_area("Details", value=skill.get("details", ""),
                height=80, placeholder=example_item.get("details", ""),
                key=f"textarea_skill_details_{idx}")

    if remove_idx is not None and 0 <= remove_idx < len(skills):
        skills.pop(remove_idx)
