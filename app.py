import streamlit as st
import pandas as pd
import os
from utils.profiler import profile_data


st.title('Smart Data Cleaning Advisor')

# file uploading

uploaded_file = st.file_uploader("upload you csv file", type=['csv'])

# reading and analyzing uploaded file

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, low_memory=False)
        
        # showing basic info

        st.subheader('Dataset Preview (first 5 row)')
        st.dataframe(df.head())

        # show shape of dataset

        st.write(f'shape: {df.shape[0]} rows x {df.shape[1]} columns')

        # memory usage

        memory_bytes = df.memory_usage(deep=True).sum()
        memory_mb = memory_bytes / (1024 * 1024)
        st.write(f'memory usage: {memory_mb:.2f} MB')

        # detected issues
        issues = profile_data(df)

        issues_df = pd.DataFrame(issues)

        st.subheader('Detected Issues')

        if not issues_df.empty:
            st.dataframe(issues_df, use_container_width=True)
        else:
            st.success('No Issues Found.')


    except Exception as e:
        st.error(f'error reading file: {e}')

