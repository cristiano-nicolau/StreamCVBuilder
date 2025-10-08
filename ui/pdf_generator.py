from __future__ import annotations

import io

import streamlit as st
from weasyprint import HTML


def html_to_pdf_bytes(html_content: str) -> bytes:
    """Convert an HTML string to PDF bytes using WeasyPrint.
    
    WeasyPrint provides excellent support for modern CSS including:
    - Flexbox and Grid layouts
    - CSS gradients, shadows, and transforms
    - Custom fonts via @font-face
    - Media queries for print
    - And much more
    
    Args:
        html_content: The HTML content with embedded CSS to convert to PDF
        
    Returns:
        PDF content as bytes, or empty bytes if conversion fails
    """
    try:
        # Create PDF from HTML string with WeasyPrint
        # write_pdf() returns bytes directly
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
        
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return b""


def generate_pdf_bytes(html_content: str) -> bytes:
    """Generate PDF from HTML content.
    
    This is the main entry point for PDF generation. It takes rendered HTML
    (typically from a Jinja2 template) and converts it to PDF format.
    
    Args:
        html_content: The complete HTML document with CSS to convert
        
    Returns:
        PDF content as bytes
    """
    return html_to_pdf_bytes(html_content)
