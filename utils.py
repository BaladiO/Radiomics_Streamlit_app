import pandas as pd
import unicodedata
from collections import defaultdict

def clean_text(text):
    """Normalize and clean text values"""
    return unicodedata.normalize("NFKC", str(text)).strip()

def process_dataframe(df):
    """
    Process the input DataFrame following the original script's logic
    
    Args:
        df (pd.DataFrame): Input DataFrame
    
    Returns:
        pd.DataFrame: Transformed, flattened DataFrame
    """
    # Configuration
    INDEX_COLUMNS = [
        'PatientID',
        'PatientName',
        'AcquisitionDate',  # Should contain values like 'Baseline', 'Mid-Treatment', etc.
        'ObjectDescription',
        'SeriesDataRole'
    ]

    # Clean all index columns
    for col in INDEX_COLUMNS:
        df[col] = df[col].astype(str).apply(clean_text)

    # Set hierarchical index
    df.set_index(INDEX_COLUMNS, inplace=True)

    # Define categorical sorting
    nature_order = ['Baseline', 'Mid-treatment', 'Post-treatment']
    object_order = ['Tumor', 'Peritumoral']
    series_order = ['T2', 'SUB', 'T1']

    # Convert to categorical types for proper sorting
    df.index = df.index.set_levels([
        pd.Categorical(df.index.levels[0], ordered=True),
        pd.Categorical(df.index.levels[1], ordered=True),
        pd.Categorical(df.index.levels[2], categories=nature_order, ordered=True),
        pd.Categorical(df.index.levels[3], categories=object_order, ordered=True),
        pd.Categorical(df.index.levels[4], categories=series_order, ordered=True)
    ])

    # Sort by the custom categories
    df = df.sort_index()

    # Convert to Nested Structure
    def dataframe_to_nested_dict(df):
        """Convert DataFrame to nested dictionary structure"""
        nested_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
        
        for idx, row in df.iterrows():
            patient_id, patient_name, nature, obj_desc, series_role = idx
            nested_dict[patient_id][patient_name][nature][obj_desc][series_role] = row.to_dict()
        
        return nested_dict

    hierarchical_dict = dataframe_to_nested_dict(df)

    # Flatten to Excel
    flattened_data = []

    for patient_id, patient_data in hierarchical_dict.items():
        base_row = {'PatientID': patient_id}
        
        for patient_name, nature_data in patient_data.items():
            base_row['PatientName'] = patient_name
            
            for nature, obj_data in nature_data.items():
                for obj_desc, series_data in obj_data.items():
                    for series, values in series_data.items():
                        for metric, value in values.items():
                            column_name = f"{nature}_{obj_desc}_{series}_{metric}"
                            base_row[column_name] = value

        flattened_data.append(base_row)

    # Create DataFrame
    flat_df = pd.DataFrame(flattened_data)
    
    return flat_df