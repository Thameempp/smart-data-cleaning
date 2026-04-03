# imports remaining
import pandas as pd
# main entry function


def profile_data(df):
    issues = []

    numeric_cols = get_numeric_columns(df)

    issues.extend(detect_missing_values(df))
    issues.extend(detect_duplicates(df))
    issues.extend(detect_invalid_zeros(df, numeric_cols))
    issues.extend(detect_type_issues(df))
    issues.extend(detect_text_inconsistency(df))
    issues.extend(detect_outliers(df, numeric_cols))

    return issues

# helper funciton

def get_numeric_columns(df):
    numeric_cols = []

    for col in df.columns:
        try:
            pd.to_numeric(df[col])
            numeric_cols.append(col)
        except:
            continue
    return numeric_cols

def get_severity(count, total_rows):
    ratio = count / total_rows

    if ratio > 0.5:
        return 'high'
    elif ratio > 0.2:
        return 'medium'
    else:
        return 'low'
    
# detection funciton

def detect_missing_values(df):
    issues = []
    missing_tokens = ['', 'NA', 'N/A', 'NULL', 'null']

    for col in df.columns:
        series = df[col]

        null_count = series.isna().sum()

        str_missing = (
            series.astype(str)
            .str.strip()
            .isin(missing_tokens)
            .sum()
        )

        total_missing = null_count + str_missing

        if total_missing > 0 :
            issues.append({
                'column':col,
                'issue':'str_missing',
                'count':int(total_missing),
                'severity':get_severity(total_missing, len(df))
            })

    return issues


def detect_duplicates(df):
    issues = []

    dup_count = df.duplicated().sum()

    if dup_count > 0:
        issues.append({
            'column':'ALL',
            'issue':'duplicates',
            'count':int(dup_count),
            'severity':get_severity(dup_count, len(df))
        })    

    return issues


def detect_invalid_zeros(df,  numeric_cols):
    issues = []

    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce')

        zero_count = (series == 0).sum()

        if zero_count > 0:
            issues.append({
                'column':col,
                'issue':'invalid zeros',
                'count':int(zero_count),
                'severity':get_severity(zero_count, len(df))
            })
    return issues


def detect_type_issues(df):
    issues = []

    for col in df.columns:
        series = df[col]

        if series.dtype == 'object':
            try:
                converted = pd.to_numeric(series, errors='coerce')

                success_ratio = converted.notna().sum() / len(series)

                if success_ratio > 0.8 :
                    issues.append({
                        'column':col,
                        'issue':'numeric as text',
                        'count':int(len(series)),
                        'severity':'medium'
                    })
            except:
                pass

    return issues


def detect_text_inconsistency(df):
    issues = []

    for col in df.select_dtypes(include=['object']).columns:
        series = df[col].astype(str)

        space_issues = (series != series.str.strip()).sum()

        lower_unique = series.str.lower().nunique()
        original_unique = series.nunique()

        if space_issues > 0 or lower_unique < original_unique:
            issues.append({
                "column": col,
                "issue": "text_inconsistency",
                "count": int(space_issues),
                "severity": "low"
            })
    return issues


def detect_outliers(df, numeric_cols):
    issues = []

    for col in numeric_cols:
        series = pd.to_numeric(df[col],  errors='coerce').dropna()

        if len(series) ==0:
            continue

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((series < lower) | (series > upper)).sum()

        if outliers > 0 :
            issues.append({
                "column": col,
                "issue": "outliers",
                "count": int(outliers),
                "severity": get_severity(outliers, len(df))
            })

    return issues