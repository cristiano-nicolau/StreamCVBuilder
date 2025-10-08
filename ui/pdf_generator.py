from __future__ import annotations

import streamlit as st
from weasyprint import HTML


def html_to_pdf_bytes(html_content: str) -> bytes:
    """Convert HTML to PDF using WeasyPrint.
    
    Supports modern CSS including flexbox, gradients, shadows, and more.
    
    Args:
        html_content: Complete HTML document with CSS to convert to PDF
        
    Returns:
        PDF content as bytes, or empty bytes if conversion fails
    """
    try:
        return HTML(string=html_content).write_pdf()
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return b""

