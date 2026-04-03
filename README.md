# Smart Data Cleaning Advisor

A Streamlit-based intelligent data cleaning assistant that helps detect, understand, and fix data issues automatically, while generating clean and reusable pandas code.

---

## Overview

Smart Data Cleaning Advisor simplifies and accelerates the data preprocessing stage in machine learning and analytics workflows.

Instead of manually identifying issues in datasets, this tool:

* Detects common data problems
* Explains why they matter
* Suggests intelligent fixes
* Applies transformations safely
* Generates production-ready cleaning code

---

## Key Features

### Automatic Data Issue Detection

* Missing values (NaN, NULL, empty strings)
* Duplicate rows
* Invalid values (e.g., zero in age or salary)
* Data type mismatches
* Text inconsistencies (case, spacing)
* Outliers using statistical methods (IQR)

### Smart Recommendations

* Problem explanations in simple terms
* Suggested fixes with reasoning
* Severity-based prioritization

### Auto Code Generation

* Generates clean pandas scripts
* Reproducible data cleaning pipelines
* Ready for machine learning workflows

### Interactive Fix Engine

* Apply fixes per column or globally
* Preview changes before applying
* Safe in-memory processing (no data loss)

### Data Visualization and Insights

* Missing value heatmaps
* Distribution plots
* Correlation analysis
* Outlier visualization

### Export Options

* Cleaned dataset (CSV)
* ML-ready encoded dataset
* Python cleaning script
* Data quality report (HTML)
* Summary statistics (JSON)

---

## Project Structure

```
smart-data-cleaning-advisor/
│
├── app.py
├── pages/
├── utils/
│   ├── profiler.py
│   ├── rule_engine.py
│   ├── suggester.py
│   ├── executor.py
│   ├── code_generator.py
│   └── visualizer.py
│
├── data/
├── templates/
├── assets/
├── tests/
│
├── requirements.txt
├── README.md
└── .streamlit/config.toml
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/smart-data-cleaning-advisor.git
cd smart-data-cleaning-advisor
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Application

```
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## Workflow

1. Upload CSV file
2. Preview dataset
3. Detect issues automatically
4. Review explanations and suggestions
5. Apply fixes interactively
6. Visualize cleaned data
7. Export results and generated code

---

## Core Modules

| Module            | Purpose                          |
| ----------------- | -------------------------------- |
| profiler.py       | Detects data issues              |
| rule_engine.py    | Applies logic and prioritization |
| suggester.py      | Generates explanations and fixes |
| executor.py       | Applies transformations safely   |
| code_generator.py | Builds pandas pipeline           |
| visualizer.py     | Generates charts and dashboards  |

---

## Testing

Run tests to validate cleaning logic:

```
pytest tests/
```

---

## Use Cases

* Data preprocessing for machine learning projects
* Data cleaning automation
* Learning pandas and data handling
* Rapid dataset exploration
* Freelance or client data auditing

---

## Future Improvements

* AI-powered cleaning suggestions (LLM integration)
* Support for Excel, JSON, and SQL
* Automated feature engineering
* Pipeline versioning
* Cloud deployment (Streamlit Cloud)

---

## Contributing

Contributions are welcome.
Feel free to fork the repository, improve it, and submit a pull request.

---

## License

MIT License

---

## Author

Thameem
Building intelligent tools for developers and data workflows
