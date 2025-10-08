from __future__ import annotations

import os
import re
import streamlit as st
from weasyprint import HTML


def _inject_print_css(html_content: str) -> str:
    """Inject a compact print CSS into the provided HTML without altering templates.

    This keeps the HTML used for preview/download intact, while PDFs use tighter styles.
    """
    css_path = os.path.join("templates", "cv_templates", "pdf_base_styles.css")
    if not os.path.exists(css_path):
        return html_content

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    except Exception:
        return html_content

    style_tag = f"\n<style media=\"print\">\n{css}\n</style>\n"

    if "</head>" in html_content.lower():
        def repl(match):
            return style_tag + match.group(0)

        return re.sub(r"</head>", repl, html_content, count=1, flags=re.IGNORECASE)
    else:
        return style_tag + html_content


def html_to_pdf_bytes(html_content: str) -> bytes:
    """Convert HTML to PDF using WeasyPrint with print-optimized CSS injected.

    Args:
        html_content: Complete HTML document with CSS to convert to PDF

    Returns:
        PDF content as bytes, or empty bytes if conversion fails
    """
    try:
        html_with_print = _inject_print_css(html_content)
        return HTML(string=html_with_print).write_pdf()
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return b""

