import streamlit as st
from typing import Dict, List, Any
import markdown
import weasyprint
from streamlit_option_menu import option_menu

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

def render_cv_builder(data: Dict[str, Any]):
    st.header("CV Builder")
    
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
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize personal info in session state
    if "personal_info" not in st.session_state:
        st.session_state.personal_info = {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": ""
        }
    
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
        
        # Add Personal Information Form
        with st.expander("Personal Information"):
            st.session_state.personal_info["name"] = st.text_input("Name", st.session_state.personal_info["name"])
            st.session_state.personal_info["email"] = st.text_input("Email", st.session_state.personal_info["email"])
            st.session_state.personal_info["phone"] = st.text_input("Phone", st.session_state.personal_info["phone"])
            st.session_state.personal_info["location"] = st.text_input("Location", st.session_state.personal_info["location"])
            st.session_state.personal_info["linkedin"] = st.text_input("LinkedIn URL", st.session_state.personal_info["linkedin"])
            st.session_state.personal_info["github"] = st.text_input("GitHub URL", st.session_state.personal_info["github"])
            st.session_state.personal_info["website"] = st.text_input("Website URL", st.session_state.personal_info["website"])
    
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
                st.session_state.current_action = "remove_section"
                st.rerun()
            
            # Display items
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
                
                # Add personal information if available
                if st.session_state.personal_info["name"]:
                    preview_content += f"# {st.session_state.personal_info['name']}\n\n"
                    contact_info = []
                    if st.session_state.personal_info["email"]:
                        contact_info.append(f"📧 {st.session_state.personal_info['email']}")
                    if st.session_state.personal_info["phone"]:
                        contact_info.append(f"📱 {st.session_state.personal_info['phone']}")
                    if st.session_state.personal_info["location"]:
                        contact_info.append(f"📍 {st.session_state.personal_info['location']}")
                    
                    if contact_info:
                        preview_content += " | ".join(contact_info) + "\n\n"
                    
                    # Add social links
                    social_links = []
                    if st.session_state.personal_info["linkedin"]:
                        social_links.append(f"[LinkedIn]({st.session_state.personal_info['linkedin']})")
                    if st.session_state.personal_info["github"]:
                        social_links.append(f"[GitHub]({st.session_state.personal_info['github']})")
                    if st.session_state.personal_info["website"]:
                        social_links.append(f"[Website]({st.session_state.personal_info['website']})")
                    
                    if social_links:
                        preview_content += " | ".join(social_links) + "\n\n---\n\n"
                
                # Add section content
                for section in st.session_state.selected_sections:
                    selected_items = st.session_state.selected_items.get(section, [])
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
