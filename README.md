# StreamCVBuilder

A modern, interactive CV builder powered by Streamlit. Create professional resumes with beautiful templates, granular content control, and instant preview.

## Features

- **Interactive Editor** - User-friendly web interface with tabbed navigation
- **Multiple Templates** - Choose from 4 professional CV designs (Clean, Professional, Modern, Sidebar)
- **Live Preview** - See your CV update in real-time as you edit
- **Granular Control** - Select exactly which items to include from each section
- **Easy Export** - Generate HTML or PDF
- **Data Persistence** - Your CV data is automatically saved locally
- **Example Data** - Start quickly with pre-filled example content

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/cristiano-nicolau/StreamCVBuilder.git
cd StreamCVBuilder
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

you also use the cloud version at **https://streamcvbuilder.streamlit.app/**, this version does not save your data locally, so every time you open it you will have to fill in your data again.

## How to Use

1. **Fill in your data** - Navigate to the "Data Editor" tab and enter your information:
   - Personal details (name, role, contact info)
   - Social networks (LinkedIn, GitHub, etc.)
   - About me summary
   - Education history
   - Work experience
   - Projects
   - Publications
   - Skills

2. **Generate your CV** - Switch to the "CV Generator" tab:
   - Choose a template from the dropdown
   - Select which sections and specific items to include
   - Preview your CV in real-time

3. **Export** - Click to generate:
   - **HTML** - Download a standalone HTML file
   - **PDF** - Download a PDF version of your CV

## Project Structure

```
StreamCVBuilder/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── ui/                        # UI module (modular architecture)
│   ├── __init__.py           # Module interface
│   ├── callbacks.py          # Callback dataclasses
│   ├── editor_sections.py    # All CV section editors
│   ├── preview.py            # Preview and export logic
│   └── templates.py          # Template management utilities
├── utils/                     # Utility modules
│   ├── __init__.py
│   └── yaml_utils.py         # YAML data loading/saving
├── templates/                 # CV templates
│   ├── cv_template.html      # Standard template
│   ├── example.yaml          # Example CV data
│   └── cv_templates/         # Additional templates
│       ├── clean.html        # Clean modern design
│       ├── professional.html # Professional layout
│       ├── modern.html       # Gradient header design
│       └── sidebar.html      # Two-column sidebar layout
└── data/                      # Data storage
    └── user_cv_data.yaml     # Your CV data (auto-created)
```

## Available Templates

- **Clean** - Ultra-modern minimalist design (recommended)
- **Standard** - Clean layout with centered header
- **Professional** - Clean layout with left-aligned header
- **Creative** - Gradient header with contemporary styling
- **Sidebar** - Two-column layout with sidebar

## Technologies

- **Streamlit** - Web application framework
- **Jinja2** - HTML template rendering
- **PyYAML** - YAML data handling


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
