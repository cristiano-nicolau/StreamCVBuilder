from __future__ import annotations

import io
from typing import Any, Dict

import streamlit as st


def generate_pdf_optimized_html(data: Dict[str, Any]) -> str:
    name = data.get('name', '')
    role = data.get('role', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    location = data.get('location', '')
    social_networks = data.get('social_networks', [])
    sections = data.get('sections', {})
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{name} - CV</title>
    <style>
        @page {{
            size: A4;
            margin: 1.5cm;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
        }}
        h1 {{
            font-size: 24pt;
            margin-bottom: 5pt;
            color: #1a1a1a;
        }}
        h2 {{
            font-size: 12pt;
            margin-top: 10pt;
            margin-bottom: 5pt;
            padding-bottom: 3pt;
            border-bottom: 1pt solid #ccc;
            color: #1a1a1a;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }}
        .role {{
            font-size: 13pt;
            color: #666;
            margin-bottom: 5pt;
        }}
        .contact {{
            font-size: 9pt;
            color: #666;
            margin-bottom: 5pt;
        }}
        .links {{
            font-size: 9pt;
            margin-bottom: 7pt;
        }}
        .links a {{
            color: #0066cc;
            text-decoration: none;
            margin-right: 10pt;
        }}
        .entry {{
            margin-bottom: 10pt;
            page-break-inside: avoid;
        }}
        .entry-header {{
            margin-bottom: 3pt;
        }}
        .entry-title {{
            font-weight: bold;
            font-size: 11pt;
            display: inline;
        }}
        .entry-date {{
            float: right;
            color: #666;
            font-size: 9pt;
        }}
        .entry-subtitle {{
            color: #555;
            font-size: 10pt;
            margin-bottom: 5pt;
            clear: both;
        }}
        .entry-content {{
            margin-bottom: 5pt;
        }}
        ul {{
            margin-left: 15pt;
            margin-top: 3pt;
        }}
        li {{
            margin-bottom: 3pt;
        }}
        .skill-item {{
            margin-bottom: 5pt;
        }}
        .skill-label {{
            font-weight: bold;
            display: inline;
        }}
        .summary {{
            margin-bottom: 5pt;
            text-align: justify;
        }}
    </style>
</head>
<body>
    <h1>{name}</h1>
"""
    
    if role:
        html += f"    <div class='role'>{role}</div>\n"
    
    contact_parts = []
    if email:
        contact_parts.append(email)
    if phone:
        contact_parts.append(phone)
    if location:
        contact_parts.append(location)
    
    if contact_parts:
        html += f"    <div class='contact'>{' • '.join(contact_parts)}</div>\n"
    
    if social_networks:
        html += "    <div class='links'>\n"
        for social in social_networks:
            if social.get('url'):
                html += f"        <a href='{social['url']}'>{social.get('network', 'Link')}</a>\n"
        html += "    </div>\n"
    
    aboutme = sections.get('aboutme', [])
    if aboutme:
        html += "    <h2>Summary</h2>\n"
        for paragraph in aboutme:
            if paragraph:
                html += f"    <div class='summary'>{paragraph}</div>\n"
    
    experience = sections.get('experience', [])
    if experience:
        html += "    <h2>Experience</h2>\n"
        for exp in experience:
            html += "    <div class='entry'>\n"
            html += "        <div class='entry-header'>\n"
            html += f"            <div class='entry-date'>{exp.get('start_date', '')} — {exp.get('end_date', '')}</div>\n"
            html += f"            <div class='entry-title'>{exp.get('position', '')}</div>\n"
            html += "        </div>\n"
            
            subtitle_parts = [exp.get('company', '')]
            if exp.get('location'):
                subtitle_parts.append(exp['location'])
            html += f"        <div class='entry-subtitle'>{' • '.join(subtitle_parts)}</div>\n"
            
            if exp.get('highlights'):
                html += "        <ul>\n"
                for highlight in exp['highlights']:
                    html += f"            <li>{highlight}</li>\n"
                html += "        </ul>\n"
            html += "    </div>\n"
    
    education = sections.get('education', [])
    if education:
        html += "    <h2>Education</h2>\n"
        for edu in education:
            html += "    <div class='entry'>\n"
            html += "        <div class='entry-header'>\n"
            html += f"            <div class='entry-date'>{edu.get('start_date', '')} — {edu.get('end_date', '')}</div>\n"
            html += f"            <div class='entry-title'>{edu.get('degree', '')} in {edu.get('area', '')}</div>\n"
            html += "        </div>\n"
            
            subtitle_parts = [edu.get('institution', '')]
            if edu.get('location'):
                subtitle_parts.append(edu['location'])
            if edu.get('grade'):
                subtitle_parts.append(edu['grade'])
            html += f"        <div class='entry-subtitle'>{' • '.join(subtitle_parts)}</div>\n"
            
            if edu.get('highlights'):
                html += "        <ul>\n"
                for highlight in edu['highlights']:
                    html += f"            <li>{highlight}</li>\n"
                html += "        </ul>\n"
            html += "    </div>\n"
    
    projects = sections.get('projects', [])
    if projects:
        html += "    <h2>Projects</h2>\n"
        for proj in projects:
            html += "    <div class='entry'>\n"
            html += "        <div class='entry-header'>\n"
            html += f"            <div class='entry-date'>{proj.get('start_date', '')} — {proj.get('end_date', '')}</div>\n"
            
            if proj.get('url'):
                html += f"            <div class='entry-title'><a href='{proj['url']}'>{proj.get('name', '')}</a></div>\n"
            else:
                html += f"            <div class='entry-title'>{proj.get('name', '')}</div>\n"
            html += "        </div>\n"
            
            if proj.get('summary'):
                html += f"        <div class='entry-content'>{proj['summary']}</div>\n"
            
            if proj.get('highlights'):
                html += "        <ul>\n"
                for highlight in proj['highlights']:
                    html += f"            <li>{highlight}</li>\n"
                html += "        </ul>\n"
            html += "    </div>\n"
    
    publications = sections.get('publications', [])
    if publications:
        html += "    <h2>Publications</h2>\n"
        for pub in publications:
            html += "    <div class='entry'>\n"
            html += f"        <div class='entry-title'>{pub.get('title', '')}</div>\n"
            
            subtitle_parts = []
            if pub.get('venue'):
                subtitle_parts.append(pub['venue'])
            if pub.get('date'):
                subtitle_parts.append(pub['date'])
            if subtitle_parts:
                html += f"        <div class='entry-subtitle'>{' • '.join(subtitle_parts)}</div>\n"
            
            if pub.get('authors'):
                html += f"        <div class='entry-content'>{', '.join(pub['authors'])}</div>\n"
            
            if pub.get('doi'):
                html += f"        <div class='entry-content' style='font-size: 9pt; color: #666;'>DOI: {pub['doi']}</div>\n"
            html += "    </div>\n"
    
    skills = sections.get('skills', [])
    if skills:
        html += "    <h2>Skills</h2>\n"
        for skill in skills:
            html += "    <div class='skill-item'>\n"
            html += f"        <div class='skill-label'>{skill.get('label', '')}:</div> {skill.get('details', '')}\n"
            html += "    </div>\n"
    
    html += """</body>
</html>"""
    
    return html

def html_to_pdf_bytes(html_content: str) -> bytes:
    """Convert an HTML string to PDF bytes using xhtml2pdf.

    Note: xhtml2pdf supports a subset of CSS. For best results, prefer simple, inline CSS
    in templates (avoid flexbox/grid). If conversion fails, returns empty bytes.
    """
    try:
        from xhtml2pdf import pisa

        pdf_buffer = io.BytesIO()
        # xhtml2pdf accepts a file-like object; ensure utf-8 encoding
        pisa_status = pisa.CreatePDF(src=io.BytesIO(html_content.encode("utf-8")), dest=pdf_buffer)

        if pisa_status.err:
            return b""
        return pdf_buffer.getvalue()
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")
        return b""


def generate_pdf_bytes(data: Dict[str, Any]) -> bytes:
    """Legacy helper: build a simple HTML from data and convert to PDF.

    Prefer rendering a specific template to HTML and then calling html_to_pdf_bytes(html).
    """
    pdf_html = generate_pdf_optimized_html(data)
    return html_to_pdf_bytes(pdf_html)
