
### 1. Project setup and environment

1. **Create a new project folder**
   - Pick final project title (for now, we’ll use `smart-data-cleaning-advisor`).
   - Make directory:
     ```text
     smart-data-cleaning-advisor/
     ```

2. **Set up Python environment**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate   # Linux/macOS
     # or venv\Scripts\activate  # Windows
     ```
   - Install core dependencies:
     ```bash
     pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn
     pip install streamlit-extras  # optional for nicer UI components
     ```
   - Save requirements:
     ```bash
     pip freeze > requirements.txt
     ```

3. **Initialize basic files**
   - Create:
     - `app.py` (main Streamlit entry point)
     - `README.md` (project summary, tech stack, how to run)
     - `.streamlit/config.toml` (theme, server settings, etc.)
   - Add typical Streamlit run script:
     ```bash
     streamlit run app.py
     ```

***

### 2. Folder structure (final layout)

Organize like this (you can adjust later, but start strict):

```text
smart-data-cleaning-advisor/
│
├── app.py                       # Streamlit main UI orchestrator
│
├── pages/                       # Optional: if you grow to multi-page
│   ├── upload.py                
│   ├── scan.py                  
│   └── explore.py               
│
├── utils/
│   ├── profiler.py             # Step 1: detect issues (nulls, zeros, dupes, outliers, types, text)
│   ├── rule_engine.py          # Step 2: severity scores, priority rules
│   ├── suggester.py            # Problem statement + explanation + recommended fix
│   ├── executor.py             # Step 3: apply fixes safely (preview, rollback simulation)
│   ├── code_generator.py       # Step 4: generate full pandas pipeline script
│   └── visualizer.py           # Build plots and dashboards
│
├── data/
│   ├── sample_datasets/        # Pre‑made problematic CSVs for testing
│   ├── temp_uploads/           # User‑uploaded files (cleared on server restart)
│   └── processed/              # Cleaned outputs & reports
│
├── templates/
│   ├── code_templates/         # Snippet templates per issue type
│   │   ├── missing_values.txt
│   │   ├── invalid_values.txt
│   │   ├── duplicates.txt
│   │   └── ...
│   └── report_templates/       # HTML report scaffolds
│
├── assets/
│   ├── css/                    # Custom CSS (via Streamlit‑style HTML)
│   └── images/                 # Logos / icons / screenshots
│
├── tests/
│   ├── test_cleaning.py        # Unit tests for core logic
│   └── test_code_generation.py # Pandas code correctness
│
├── requirements.txt
├── README.md
└── .streamlit/config.toml      # Theme, server, etc.
```

***

### 3. Step‑by‑step implementation (Phase 1 → Phase 3)

Below, each item is **a concrete, actionable step**, not abstract features.

***

#### Phase 1: Core detection (upload + preview + basic issues)

1. **Implement `app.py` skeleton**
   - Import libraries:
     ```python
     import streamlit as st
     import pandas as pd
     import os
     ```
   - Create sections:
     - `st.title("Smart Data Cleaning Advisor")`
     - Upload area (`st.file_uploader` with CSV only)
     - Data preview (show first 1000 rows with `st.dataframe`)

2. **Handle CSV upload and preview**
   - Save uploaded file to `data/temp_uploads/` with a unique name.
   - Use `pandas.read_csv` with safe defaults:
     - `low_memory=False`
     - `dtype=str` for first load (later refine types in `profiler`).
   - Show:
     - Shape: `rows × cols`
     - Memory usage via `df.memory_usage(deep=True).sum()`
     - File size via `os.path.getsize()`

3. **Create `utils/profiler.py` – core detection engine**
   - Function ideas:
     - `detect_missing_values(df)`:  
       Check for `NaN`, `None`, `""`, `"NA"`, `"NULL"`, etc., per column.
     - `detect_invalid_zeros(df)`:  
       For numeric columns, count `0` in `age`, `salary`, etc.
     - `detect_duplicates(df)`:  
       Count exact row duplicates.
     - `detect_type_issues(df)`:  
       Flag numeric columns stored as `object`, strings that look like dates.
     - `detect_text_inconsistency(df)`:  
       Check case variation, extra spaces in text columns.
     - `detect_outliers(df, numeric_cols)`:  
       Use IQR (1.5×) per column.
   - Return a list of issues like:
     ```python
     [
       {"col": "age", "issue": "missing", "count": 25, "severity": "high"},
       {"col": "salary", "issue": "outlier", "count": 10, "severity": "medium"},
       ...
     ]
     ```

4. **Show issue summary table in UI**
   - In `app.py`, call `profiler.detect_...` functions.
   - Build a `st.dataframe` with columns:
     - `Column`
     - `Issue`
     - `Count`
     - `Severity`
     - A button column (e.g., `Quick Fix` placeholder for now).

5. **Implement suggestion UI for each issue**
   - In `utils/suggester.py`:
     - `generate_problem_statement(issue)`:  
       “Age column contains 2 invalid zero values.”
     - `generate_explanation(issue)`:  
       “Zero ages are logically impossible and should be treated as missing.”
     - `generate_recommendation(issue)`:  
       “Replace zeros with NaN, then impute with median.”
   - In `app.py`, for each row:
     - Show expander with:
       - Problem statement
       - Explanation
       - Recommended fix (as text)

***

#### Phase 2: Cleaning engine + code generation (core logic)

1. **Build `utils/rule_engine.py`**
   - Define rules:
     - If numeric column and contains `0` → suggest `replace(0, np.nan)`.
     - If >70% missing → suggest flag for possible drop.
     - If categorical, low cardinality → suggest `get_dummies`.
     - If date‑like string → suggest `pd.to_datetime(..., errors='coerce')`.
   - Add severity scoring:
     - `severity = rule["severity"] * impact_factor` (e.g., % of column affected).
   - Return a list of **actionable rules** for each issue:
     ```python
     {
       "col": "age",
       "action_type": "replace_zeros_with_nan",
       "priority": "high"
     }
     ```

2. **Implement `utils/suggester.py` – pandas code snippets**
   - For each rule type, map to a template:
     - `replace_zeros_with_nan` → snippet text in `templates/code_templates/invalid_values.txt`.
   - At runtime:
     - Interpolate `df['{col}']` into the template.
   - In `app.py`, under each issue:
     - Show:
       - `st.code("pandas snippet")`
       - [Copy] button (via `st.code + copy_to_clipboard` logic or hint)

3. **Build `utils/executor.py` – safe execution**
   - Create a `CleaningSession` class:
     - Hold `df_raw` (original) and `df` (working copy).
   - Implement methods:
     - `apply_single_fix(issue, rule)`:
       - Modify `df` in memory.
       - Return a preview of affected rows.
     - `apply_all_high_priority()`:
       - Loop over rules marked `"high"` priority.
   - In UI:
     - Add buttons:
       - `Apply to 'age'`
       - `Apply All High Priority`
       - `Apply All`
     - Show side‑by‑side raw vs. cleaned (first N rows) after each apply.

4. **Create `utils/code_generator.py` – pipeline script**
   - Take all applied rules and generate a **single `.py` script**.
   - Structure:
     - Header comment: filename, timestamp.
     - Import block (`pandas`, `numpy`).
     - Load block:
       ```python
       df = pd.read_csv('employee_data.csv')
       ```
     - Sections:
       1. Handle invalid values
       2. Fill missing values
       3. Fix data types
       4. Text normalization
       5. Remove duplicates
       6. Encoding
   - Use `st.download_button` to let user download:
     - Cleaned CSV
     - Encoded CSV
     - Python pipeline script

***

#### Phase 3: UI polish + visualization + downloads

1. **Build `utils/visualizer.py`**
   - Functions:
     - `plot_missing_heatmap(df, caption="Before cleaning")`
     - `plot_data_quality_score(before_score, after_score)`
     - `plot_distributions(df, cols=['age', 'salary'])`
     - `plot_outlier_scatter(df, col_x, col_y)`
     - `plot_correlation_heatmap(df)`
     - `plot_categorical_bars(df, cols=['city', 'department'])`
   - Call them:
     - After scan → before‑cleaning dashboard
     - After apply → after‑cleaning dashboard

2. **Create EDA dashboard UI**
   - In `app.py`, add a section:
     - `st.subheader("Explore cleaned data")`
     - Tabs or sections:
       - `📊 Data Quality Dashboard`
       - `📈 Distribution & Outliers`
       - `🔗 Correlation & Encoding Preview`
   - Use Plotly or Matplotlib via `st.plotly_chart` or `st.pyplot`.

3. **Implement multiple download options**
   - Generate:
     - `cleaned_employee_data.csv` → via `df.to_csv(...)`
     - `ml_ready_encoded.csv` → after `pd.get_dummies()`.
     - `data_cleaning_pipeline.py` → from `code_generator`.
     - `data_quality_report.html`:
       - Use Jinja2 or basic HTML + CSS; fill with stats, tables, and images.
     - `summary_stats.json`:
       - Dictionary of shape, memory, missing counts, etc.
   - Add multiple `st.download_button` widgets in the Export section.

4. **Polish UI and UX**
   - Use:
     - `st.sidebar` for navigation / file upload.
     - `st.info`, `st.success`, `st.warning` for status.
   - Add:
     - Loading spinners (`st.spinner("Analyzing data...")`)
     - Progress bars for long detection steps.
     - Error handling:
       - Catch malformed CSV, encoding errors, huge files.
   - Style:
     - Use `assets/css/custom.css` injected via `st.markdown("<style>...</style>", unsafe_allow_html=True)`.

***

### 4. Technical architecture inside the app

1. **Processing flow (per dataset)**
   - User uploads → save to `data/temp_uploads/`.
   - Load into `df` → show preview.
   - Call `profiler.py` → return list of issues.
   - Pass to `rule_engine.py` → get rules + severity.
   - Feed to `suggester.py` → problem + explanation + code snippet.
   - Let user:
     - Apply fixes (via `executor.py`).
     - Generate script (via `code_generator.py`).
     - View dashboard (via `visualizer.py`).
   - Allow export via `st.download_button`.

2. **Sandboxing**
   - Never mutate the original file on disk until user explicitly exports.
   - All operations are in‑memory on `df` until download.
   - For “rollback”‑like behavior, keep a copy of `df_raw` and explain it’s not persisted.

***

### 5. Testing and success metrics (how to implement tests)

1. **Create `tests/test_cleaning.py`**
   - Sample problematic CSVs in `data/sample_datasets/`:
     - `missing_salaries.csv`
     - `zero_ages.csv`
     - `duplicates.csv`
     - `mixed_types.csv`
   - For each file:
     - Run `profiler.detect_...`.
     - Assert expected issues are found.
     - Run `executor.apply_all_high_priority()` and check:
       - No data loss (rows drop only when `drop_duplicates` is applied).
       - Correct pandas syntax when you regenerate code.

2. **Performance checks**
   - For 1M‑row dataset:
     - Time detection step (`profiler.py`) and confirm it finishes in <30s.
   - Use `time.time()` or `time.perf_counter()` in `app.py` for light metrics.

***

### 6. How to structure your development days

- **Day 1–2**
  - Folder structure + `app.py` skeleton + CSV upload + preview.
- **Day 3–4**
  - Implement `profiler.py` (missing, zeros, dupes, types).
  - Add issue table + basic suggested fixes (text only).
- **Day 5–6**
  - Write `rule_engine.py` + `suggester.py` (code snippets).
  - Implement `executor.py` (apply fixes, live preview).
- **Day 7**
  - Build `code_generator.py` and add download buttons.
- **Day 8–9**
  - Implement `visualizer.py` + dashboard.
  - Add severity scoring, prioritization, error handling.
- **Day 10**
  - Write tests in `tests/`, polish UI, write `README.md`.

***
