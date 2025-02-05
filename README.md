
# Radiomics Data Transformer Streamlit App

## Overview
This app loads an Excel document, processes it by setting a hierarchical index, converting the data into a nested structure, and finally flattening it to a single row per patient.

## Features
- Upload Excel files
- Preview file details
- Transform data with a single click
- Download transformed data as CSV or Excel

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App
```bash
streamlit run app.py
```

## Usage
1. Upload your Excel file
2. Click "Extract and Transform Data"
3. Download the transformed file
