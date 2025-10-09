import streamlit as st
from typing import Dict, List, Any
import markdown
import weasyprint
from streamlit_option_menu import option_menu
from .callbacks import EditorCallbacks

import streamlit as st
from typing import Dict, List, Any
from weasyprint import HTML
import markdown

def get_section_items(data: Dict[str, Any], section_name: str) -> List[Dict[str, Any]]:
    """Get items for a specific section."""
    sections = data.get("sections", {})
    if section_name == "aboutme":
        return [{"content": item} for item in sections.get("aboutme", [])]
    elif section_name in ["education", "experience", "projects", "skills", "publications"]:
        return sections.get(section_name, [])
    return []

def get_section_content(data: Dict[str, Any], section_name: str, selected_items: List[int] = None) -> str:
    """Generate markdown content for a specific section."""
    content = []
    items = get_section_items(data, section_name)
    
    if not items:
        return ""

    if selected_items is None:
        selected_items = list(range(len(items)))
    
    if section_name == "aboutme":
        content.append("## About Me\n")
        for i in selected_items:
            if i < len(items):
                content.extend([items[i]["content"]])
        
    elif section_name == "education":
        content.append("## Education\n")
        for i in selected_items:
            if i < len(items):
                edu = items[i]
                content.append(f"### {edu['institution']}")
                content.append(f"_{edu['degree']} in {edu['area']}_")
                content.append(f"{edu['start_date']} - {edu['end_date']}")
                if "highlights" in edu:
                    for highlight in edu["highlights"]:
                        content.append(f"- {highlight}")
                content.append("")
            
    elif section_name == "experience":
        content.append("## Experience\n")
        for i in selected_items:
            if i < len(items):
                exp = items[i]
                content.append(f"### {exp['position']} at {exp['company']}")
                content.append(f"{exp['start_date']} - {exp['end_date']}")
                if "highlights" in exp:
                    for highlight in exp["highlights"]:
                        content.append(f"- {highlight}")
                content.append("")
            
    elif section_name == "projects":
        content.append("## Projects\n")
        for i in selected_items:
            if i < len(items):
                proj = items[i]
                content.append(f"### {proj['name']}")
                if "url" in proj:
                    content.append(f"[Project Link]({proj['url']})")
                content.append(f"{proj['start_date']} - {proj['end_date']}")
                if "highlights" in proj:
                    for highlight in proj["highlights"]:
                        content.append(f"- {highlight}")
                content.append("")
            
    elif section_name == "skills":
        content.append("## Skills\n")
        for i in selected_items:
            if i < len(items):
                skill = items[i]
                content.append(f"### {skill['label']}")
                content.append(skill['details'])
                content.append("")
            
    elif section_name == "publications":
        content.append("## Publications\n")
        for i in selected_items:
            if i < len(items):
                pub = items[i]
                content.append(f"### {pub['title']}")
                content.append(f"_{pub['venue']}_")
                if "authors" in pub:
                    content.append("Authors: " + ", ".join(pub["authors"]))
                content.append("")
            
    return "\n".join(content)

def render_cv_builder(data: Dict[str, Any], callbacks: EditorCallbacks) -> None:
    st.header("CV Builder")
    
    # Check if there's data to work with
    has_user_data = data and data.get("name")
    
    if not data or not data.get("name"):
        st.warning("No CV data available. Please fill in the Data Editor tab or load example data.")
        if st.button("Load Example Data", use_container_width=True, type="primary"):
            callbacks.on_load_example()
            st.rerun()
        return
    
    # Add CSS for column separation and better layout
    st.markdown("""
        <style>
        .stColumn {
            border-right: 2px solid #e6e6e6;
            padding-right: 15px;
            margin-right: 15px;
        }
        .download-buttons {
            border-top: 1px solid #e6e6e6;
            padding-top: 15px;
            margin-top: 15px;
        }
        .personal-info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 5px 0;
            padding: 8px;
            border: 1px solid #eee;
            border-radius: 4px;
            background-color: #f9f9f9;
        }
        .social-network-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 5px 0;
            padding: 8px;
            border: 1px solid #eee;
            border-radius: 4px;
            background-color: #f0f8ff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize personal info and social networks in session state
    if "personal_info_selected" not in st.session_state:
        st.session_state.personal_info_selected = {}
    
    if "social_networks_selected" not in st.session_state:
        st.session_state.social_networks_selected = []
    
    # Available sections
    available_sections = {
        "About Me": "aboutme",
        "Education": "education",
        "Experience": "experience", 
        "Projects": "projects",
        "Skills": "skills",
        "Publications": "publications"
    }
    
    # Initialize session state
    if "selected_sections" not in st.session_state:
        st.session_state.selected_sections = []
    if "selected_items" not in st.session_state:
        st.session_state.selected_items = {}
    if "current_action" not in st.session_state:
        st.session_state.current_action = None
    
    # Create three columns with custom widths
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.subheader("Available Sections")
        
        # Personal Information Section
        with st.expander("Personal Information", expanded=True):
            st.markdown("**Select which personal info to include:**")
            
            # Available personal info fields from data
            personal_fields = {
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "phone": data.get("phone", ""),
                "location": data.get("location", ""),
                "role": data.get("role", "")
            }
            
            for field, value in personal_fields.items():
                if value:  # Only show fields that have data
                    field_label = field.replace("_", " ").title()
                    is_selected = st.session_state.personal_info_selected.get(field, True)  # Default to selected
                    
                    # Create checkbox for each field
                    if st.checkbox(f"{field_label}: {value}", value=is_selected, key=f"personal_{field}"):
                        st.session_state.personal_info_selected[field] = True
                        if field not in st.session_state.selected_sections:
                            if "personal_info" not in st.session_state.selected_sections:
                                st.session_state.selected_sections.insert(0, "personal_info")
                    else:
                        st.session_state.personal_info_selected[field] = False
                        # Remove personal_info section if no fields are selected
                        if not any(st.session_state.personal_info_selected.values()):
                            if "personal_info" in st.session_state.selected_sections:
                                st.session_state.selected_sections.remove("personal_info")
        
        # Social Networks Section
        social_networks = data.get("social_networks", [])
        if social_networks:
            with st.expander("Social Networks"):
                st.markdown("**Select which social networks to include:**")
                
                for idx, network in enumerate(social_networks):
                    network_label = f"{network.get('network', 'Network')}: {network.get('username', network.get('url', 'Link'))}"
                    is_selected = idx in st.session_state.social_networks_selected
                    
                    if st.checkbox(network_label, value=is_selected, key=f"social_{idx}"):
                        if idx not in st.session_state.social_networks_selected:
                            st.session_state.social_networks_selected.append(idx)
                            if "social_networks" not in st.session_state.selected_sections:
                                # Insert after personal_info if it exists, otherwise at the beginning
                                insert_pos = 1 if "personal_info" in st.session_state.selected_sections else 0
                                st.session_state.selected_sections.insert(insert_pos, "social_networks")
                    else:
                        if idx in st.session_state.social_networks_selected:
                            st.session_state.social_networks_selected.remove(idx)
                            # Remove social_networks section if no networks are selected
                            if not st.session_state.social_networks_selected:
                                if "social_networks" in st.session_state.selected_sections:
                                    st.session_state.selected_sections.remove("social_networks")
    
        # Display available sections as expandable sections
        for section_name, section_key in available_sections.items():
            items = get_section_items(data, section_key)
            if items:  # Only show sections that have items
                with st.expander(section_name):
                    for idx, item in enumerate(items):
                        # Get a descriptive label for the item
                        label = item.get('institution', item.get('company', item.get('name',
                                item.get('label', item.get('title', item.get('content', f'Item {idx + 1}'))))))
                        
                        # Create a clickable button for each item
                        if section_key not in st.session_state.selected_sections or \
                           idx not in st.session_state.selected_items.get(section_key, []):
                            st.markdown(f'<div class="section-item">', unsafe_allow_html=True)
                            if st.button(f"➕ {label}", key=f"add_{section_key}_{idx}"):
                                if section_key not in st.session_state.selected_sections:
                                    st.session_state.selected_sections.append(section_key)
                                    st.session_state.selected_items[section_key] = []
                                if section_key in st.session_state.selected_items:
                                    st.session_state.selected_items[section_key].append(idx)
                                st.session_state.current_action = "add_item"
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Selected Items")
        st.markdown('<div class="selected-sections">', unsafe_allow_html=True)
        
        # Display selected sections
        for i, section in enumerate(st.session_state.selected_sections):
            # Get section title
            section_title = ""
            
            if section == "personal_info":
                section_title = "Personal Information"
            elif section == "social_networks":
                section_title = "Social Networks"
            else:
                for name, key in available_sections.items():
                    if key == section:
                        section_title = name
                        break
            
            # Header with controls
            cols = st.columns([4, 1, 1, 1])
            cols[0].markdown(f"### {section_title}")
            
            # Up button
            if i > 0:
                if cols[1].button("↑", key=f"up_{section}"):
                    st.session_state.selected_sections[i], st.session_state.selected_sections[i-1] = \
                        st.session_state.selected_sections[i-1], st.session_state.selected_sections[i]
                    st.session_state.current_action = "reorder"
                    st.rerun()
            
            # Down button
            if i < len(st.session_state.selected_sections) - 1:
                if cols[2].button("↓", key=f"down_{section}"):
                    st.session_state.selected_sections[i], st.session_state.selected_sections[i+1] = \
                        st.session_state.selected_sections[i+1], st.session_state.selected_sections[i]
                    st.session_state.current_action = "reorder"
                    st.rerun()
            
            # Remove button
            if cols[3].button("✕", key=f"remove_section_{section}"):
                st.session_state.selected_sections.remove(section)
                if section in st.session_state.selected_items:
                    del st.session_state.selected_items[section]
                # Clear personal info or social networks selections if removed
                if section == "personal_info":
                    st.session_state.personal_info_selected = {}
                elif section == "social_networks":
                    st.session_state.social_networks_selected = []
                st.session_state.current_action = "remove_section"
                st.rerun()
            
            # Display items based on section type
            if section == "personal_info":
                # Display selected personal info fields
                for field, is_selected in st.session_state.personal_info_selected.items():
                    if is_selected:
                        field_label = field.replace("_", " ").title()
                        value = data.get(field, "")
                        st.markdown(
                            f"""
                            <div class="personal-info-item">
                                <div>• {field_label}: {value}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            
            elif section == "social_networks":
                # Display selected social networks
                social_networks = data.get("social_networks", [])
                for idx in st.session_state.social_networks_selected:
                    if idx < len(social_networks):
                        network = social_networks[idx]
                        network_label = f"{network.get('network', 'Network')}: {network.get('username', network.get('url', 'Link'))}"
                        st.markdown(
                            f"""
                            <div class="social-network-item">
                                <div>• {network_label}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            
            else:
                # Display regular section items
                items = get_section_items(data, section)
                selected_items = st.session_state.selected_items.get(section, [])
                
                if selected_items:
                    for idx in selected_items:
                        if idx < len(items):
                            item = items[idx]
                            label = item.get('institution', item.get('company', item.get('name',
                                    item.get('label', item.get('title', item.get('content', f'Item {idx + 1}'))))))
                            
                            # Use HTML para layout inline
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; 
                                    margin: 5px 0; padding: 5px; border: 1px solid #eee; border-radius: 4px;">
                                    <div style="flex-grow: 1;">• {label}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            if st.button("✕", key=f"remove_item_{section}_{idx}"):
                                st.session_state.selected_items[section].remove(idx)
                                if not st.session_state.selected_items[section]:
                                    st.session_state.selected_sections.remove(section)
                                    del st.session_state.selected_items[section]
                                st.session_state.current_action = "remove_item"
                                st.rerun()
            
            st.markdown("---")
    
    with col3:
        # Create tabs for Preview and MD Editor
        preview_tab, md_editor_tab = st.tabs(["Preview", "MD Editor"])
        
        with preview_tab:
            st.subheader("Preview")
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            
            # Generate preview content
            if st.session_state.selected_sections:
                preview_content = ""
                
                # Process sections in order
                for section in st.session_state.selected_sections:
                    if section == "personal_info":
                        # Add personal information
                        selected_personal = {k: v for k, v in st.session_state.personal_info_selected.items() if v}
                        if selected_personal:
                            if st.session_state.personal_info_selected.get("name", True):
                                name = data.get("name", "")
                                if name:
                                    preview_content += f"# {name}\n\n"
                            
                            contact_info = []
                            if st.session_state.personal_info_selected.get("email", True) and data.get("email"):
                                contact_info.append(f"📧 {data.get('email')}")
                            if st.session_state.personal_info_selected.get("phone", True) and data.get("phone"):
                                contact_info.append(f"📱 {data.get('phone')}")
                            if st.session_state.personal_info_selected.get("location", True) and data.get("location"):
                                contact_info.append(f"📍 {data.get('location')}")
                            if st.session_state.personal_info_selected.get("role", True) and data.get("role"):
                                contact_info.append(f"💼 {data.get('role')}")
                            
                            if contact_info:
                                preview_content += " | ".join(contact_info) + "\n\n"
                    
                    elif section == "social_networks":
                        # Add selected social networks
                        social_networks = data.get("social_networks", [])
                        if st.session_state.social_networks_selected:
                            social_links = []
                            for idx in st.session_state.social_networks_selected:
                                if idx < len(social_networks):
                                    network = social_networks[idx]
                                    network_name = network.get('network', 'Link')
                                    network_url = network.get('url', '#')
                                    social_links.append(f"[{network_name}]({network_url})")
                            
                            if social_links:
                                preview_content += "**Social Networks:** " + " | ".join(social_links) + "\n\n---\n\n"
                    
                    else:
                        # Add regular section content
                        selected_items = st.session_state.selected_items.get(section, [])
                        if selected_items:
                            preview_content += get_section_content(data, section, selected_items) + "\n\n"
            
                # Convert markdown to HTML and display preview
                html = markdown.markdown(preview_content)
                st.markdown(html, unsafe_allow_html=True)
                
                # Add download buttons within preview tab
                st.markdown('<div class="download-buttons">', unsafe_allow_html=True)
                dcol1, dcol2 = st.columns(2)
                
                with dcol1:
                    st.download_button(
                        "Download as Markdown",
                        preview_content,
                        file_name="cv.md",
                        mime="text/markdown"
                    )
                
                with dcol2:
                    if st.button("Convert to PDF"):
                        try:
                            # Convert markdown to HTML with styling
                            html_content = f"""
                            <html>
                            <head>
                                <meta charset="UTF-8">
                                <style>
                                    body {{
                                        font-family: 'Arial', sans-serif;
                                        line-height: 1.6;
                                        max-width: 800px;
                                        margin: 40px auto;
                                        padding: 20px;
                                        color: #333;
                                    }}
                                    h1 {{
                                        color: #2c3e50;
                                        border-bottom: 2px solid #3498db;
                                        padding-bottom: 10px;
                                    }}
                                    h2 {{
                                        color: #34495e;
                                        margin-top: 25px;
                                    }}
                                    h3 {{
                                        color: #2c3e50;
                                    }}
                                    a {{
                                        color: #3498db;
                                        text-decoration: none;
                                    }}
                                    a:hover {{
                                        text-decoration: underline;
                                    }}
                                    ul {{
                                        margin: 10px 0;
                                        padding-left: 20px;
                                    }}
                                    li {{
                                        margin: 5px 0;
                                    }}
                                    hr {{
                                        border: none;
                                        border-top: 1px solid #eee;
                                        margin: 20px 0;
                                    }}
                                </style>
                            </head>
                            <body>
                                {html}
                            </body>
                            </html>
                            """
                            
                            # Convert HTML to PDF using WeasyPrint
                            pdf = HTML(string=html_content).write_pdf()
                            
                            # Offer the PDF for download
                            st.download_button(
                                "Download PDF",
                                pdf,
                                file_name="cv.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"Error generating PDF: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with md_editor_tab:
            st.subheader("Markdown Editor")
            if st.session_state.selected_sections:
                edited_content = st.text_area("Edit Markdown", value=preview_content, height=400)
                preview_content = edited_content  # Update preview content with edited content
        
        st.markdown('</div>', unsafe_allow_html=True)
