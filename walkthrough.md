# Skill Extractor & Analyzer Dashboard Walkthrough

## What Was Accomplished
Built a complete pipeline and Streamlit dashboard to process user activity logs, extract technical skills using NLP methods, and visualize the extracted skills based on configurable hierarchies and thresholds.

### Components Built
1. **[data_processor.py](file:///c:/Users/Swikriti%20Paul/OneDrive/Desktop/Coriolis/data_processor.py)**
   - Processes `status_updates_20260306_202707-1.csv`.
   - Uses text extraction (regex parsing over normalized strings) to find technical skills from a pre-defined domain dictionary (e.g., LLMs, Model Optimization, Prompt Engineering).
2. **[skill_grouper.py](file:///c:/Users/Swikriti%20Paul/OneDrive/Desktop/Coriolis/skill_grouper.py)**
   - Implements the grouping logic using the `SKILL_HIERARCHY`.
   - Allows a dynamic `threshold` configuration to merge specific child skills (e.g., `int8`, `qwen`) into their broader parent mappings (e.g., `Model Optimization`, `Large Language Models`) if they fall below the configured frequency.
   - Outputs the exact specified JSON format including `general_skills` and `merged_skills` objects.
3. **[app.py](file:///c:/Users/Swikriti%20Paul/OneDrive/Desktop/Coriolis/app.py)**
   - Interactive Streamlit Application wrapping the logic.
   - Contains a dynamic threshold slider, KPI Metrics, Experience Distribution Bar Charts, Skill Hierarchy visualization (Plotly Treemap), and Network Relationship Graphs.

## Validation Results
- Executed `data_processor.py` successfully over the CSV dataset; accurately mapped 26 unique skills with correct semantic frequencies (e.g., `llm`: 39, `finetuning`: 39, `int8`: 18, `qwen`: 4).
- Executed `skill_grouper.py` with dynamic thresholds successfully allocating experience points and accurately marking merged vs specific skills.

To run the dashboard locally, use the following command in your terminal:
```bash
cd "c:\Users\Swikriti Paul\OneDrive\Desktop\Coriolis"
streamlit run app.py
```
