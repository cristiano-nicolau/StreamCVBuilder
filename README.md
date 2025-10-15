# StreamCVBuilder

A modern, interactive CV builder powered by Streamlit. Create professional resumes with beautiful templates, granular content control, and instant preview.

## Features

- **Interactive Editor** - User-friendly web interface with tabbed navigation
- **Multiple Templates** - Choose from professional CV designs (Clean, Professional, Creative, Sidebar)
- **Live Preview** - See your CV update in real-time as you edit
- **Granular Control** - Select exactly which items to include from each section
- **Easy Export** - Generate HTML or PDF versions of your CV
- **Data Management** - Download your CV data as YAML or upload previous data
- **Example Data** - Start quickly with pre-filled example content
- **Cloud Ready** - Works both locally and in cloud deployment

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

You can also use the cloud version at **https://streamcvbuilder.streamlit.app/**

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

2. **Data Management**:
   - **Download Data** - Save your CV data as a YAML file for backup
   - **Upload Data** - Restore your CV by uploading a previously saved YAML file
   - **Delete All** - Clear all current data and start fresh

3. **Generate your CV** - Switch to the "CV Generator" tab:
   - Choose a template from the dropdown
   - Select which sections and specific items to include
   - Preview your CV in real-time
  
4. **Build your CV** - Switch to the "CV Builder" tab:
   - Construct your CV with mardown language
   - Preview CV in real-time

5. **Export** - Click to generate:
   - **HTML** - Download a standalone HTML file
   - **PDF** - Download a PDF version of your CV
   - **Markdown** - Download a .md version of your CV

## Project Structure

```
StreamCVBuilder/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── ui/                        # UI module (modular architecture)
│   ├── __init__.py           # Module interface and main UI components
│   ├── callbacks.py          # Callback dataclasses
│   ├── editor_sections.py    # All CV section editors
│   ├── preview.py            # Preview and export logic
│   └── templates.py          # Template management utilities
├── utils/                     # Utility modules
│   ├── __init__.py
│   └── yaml_utils.py         # YAML data handling utilities
├── templates/                 # CV templates
│   ├── example.yaml          # Example CV data
│   └── cv_templates/         # CV template designs
│       ├── clean.html        # Clean modern design
│       ├── creative.html     # Creative layout with gradients
│       ├── professional.html # Professional layout
│       └── sidebar.html      # Two-column sidebar layout
```


## Available Templates

- **Clean** - Ultra-modern minimalist design (recommended)
- **Professional** - Clean layout with professional styling
- **Creative** - Gradient header with contemporary styling
- **Sidebar** - Two-column layout with sidebar navigation

## Technologies

- **Streamlit** - Web application framework
- **Jinja2** - HTML template rendering
- **PyYAML** - YAML data handling


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
