from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import jinja2
import streamlit as st


def get_available_templates() -> List[Dict[str, str]]:
    templates: List[Dict[str, str]] = [
        {"name": "Standard", "path": os.path.join("templates", "cv_templates", "Standard.html")},
    ]

    templates_dir = Path("templates") / "cv_templates"
    if templates_dir.exists():
        for file in sorted(templates_dir.iterdir()):
            if file.suffix.lower() == ".html" and file.stem.lower() != "standard":
                templates.append({"name": file.stem.capitalize(), "path": str(file)})

    return templates


def generate_html_cv(data: Dict[str, Any], template_path: str) -> Optional[str]:
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path) or ".")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(os.path.basename(template_path))
        return template.render(**data)
    except Exception as exc:
        st.error(f"Error generating the CV: {exc}")
        return None
