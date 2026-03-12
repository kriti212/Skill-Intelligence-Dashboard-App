# Skill-Intelligence-Dashboard-App

This project is a Streamlit-based web application that processes user activity logs, extracts candidate skills using NLP techniques, and visualizes a skill hierarchy dynamically based on configured thresholds.

## Features

- **Data Processing (`data_processor.py`)**: Reads activity logs from `status_updates_20260306_202707-1.csv`, cleans the text, and extracts technical skills based on predefined taxonomies (e.g., Large Language Models, Model Optimization, Prompt Engineering).
- **Skill Grouping (`skill_grouper.py`)**: Applies a configurable frequency threshold to merge specific child skills (e.g., `INT8`, `Qwen3`) into broader parent skills (e.g., `Model Optimization`, `Large Language Models`).
- **Interactive Dashboard (`app.py`)**: A Streamlit application that provides:
  - Dynamic KPI metrics (Experience Points, General Skills).
  - Configurable frequency thresholds via a sidebar slider.
  - Interactive Visualizations: 
    - Experience Distribution (Horizontal Bar Chart)
    - Skill Hierarchy (Treemap)
    - Skill Relationship Network (NetworkX + Plotly)
  - JSON output representations of merged skill mappings.

## Installation

1. Ensure you have Python 3 installed.
2. Navigate to the project directory:
   ```bash
   cd "c:\Users\Swikriti Paul\OneDrive\Desktop\Coriolis"
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the required Spacy English model (if not already installed):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

To start the Streamlit application, run the following command in your terminal:

```bash
cd "c:\Users\Swikriti Paul\OneDrive\Desktop\Coriolis"
streamlit run app.py
```

This will start a local web server and open the dashboard in your default web browser. You can then use the sidebar slider to adjust the skill frequency threshold and watch the visualizations update in real-time.

## Project Structure

- `app.py`: Main Streamlit application file containing the UI layout and Plotly visualizer configurations.
- `data_processor.py`: Contains the logic for reading the CSV files and extracting skill frequencies via matching logic.
- `skill_grouper.py`: Contains the logic to structure the extracted skills into hierarchies based on the set threshold.
- `requirements.txt`: Python package dependencies.
- `status_updates_20260306_202707-1.csv`: The provided dataset of user activity logs.
