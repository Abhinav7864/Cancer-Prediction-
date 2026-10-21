# Cancer-Prediction-
## Tableau & SQL Function Analysis Pipeline

This repository implements **10 categories of data analysis functions** (Mathematical, String, Date, Type Conversion, Aggregations, Logical/Conditional, Window/Table Calculations, User Session, Spatial, and Predictive Analytics) on the **Appendix Cancer Prediction Dataset** downloaded dynamically via `kagglehub`.

## Project Structure

- `tableau_functions.py`: Comprehensive Python function library implementing all 30+ Tableau / SQL functions.
- `run_analysis.py`: Main executable pipeline that downloads dataset via `kagglehub`, computes all 63 calculated fields, prints styled ASCII tables, and exports the enriched dataset to CSV.
- `generate_pdf_report.py`: ReportLab PDF report generator that produces a publication-ready PDF document summarizing all calculations and sample data.
- `Appendix_Cancer_Function_Analysis_Report.pdf`: Generated PDF report.
- `.gitignore`: Configured to exclude virtual environments (`venv/`) and large dataset CSV files.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhinav7864/Cancer-Prediction-.git
   cd Cancer-Prediction-
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install kagglehub pandas numpy reportlab pillow
   ```

## Usage

### Run Data Analysis
```bash
python3 run_analysis.py
```

### Generate PDF Report
```bash
python3 generate_pdf_report.py
```

## Dataset Information
- **Source**: Kaggle `ankushpanday1/appendix-cancer-prediction-dataset`
- **Rows**: 260,000
- **Columns**: 88 (25 Original + 63 Calculated Fields)
