import streamlit as st
import pandas as pd
import io
import unicodedata
import os
import secrets
import tempfile
from collections import defaultdict
from utils import process_dataframe

# Security configuration
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB maximum
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}

def is_safe_filename(filename):
    """Validate filename to prevent directory traversal"""
    return all(
        part not in {'', '.', '..'}
        for part in filename.split(os.path.sep)
    )

def validate_file(uploaded_file):
    """Perform multiple security checks on uploaded file"""
    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)} MB")
    
    # Check file extension
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type. Only Excel files are allowed.")
    
    return True

def secure_file_processing(uploaded_file):
    """Securely process uploaded file with temporary storage"""
    # Generate a secure random filename
    secure_filename = f"{secrets.token_hex(16)}{os.path.splitext(uploaded_file.name)[1]}"
    
    # Use a temporary directory for file storage
    with tempfile.TemporaryDirectory() as tmpdir:
        # Construct full secure path
        file_path = os.path.join(tmpdir, secure_filename)
        
        # Write uploaded file securely
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        # Read and process file
        df = pd.read_excel(file_path, sheet_name='Feuil1')
    
    return df

def main():
    st.title("Secure Radiomics Data Transformer")
    
    # Add security warning
    st.warning("🔒 Your files are processed securely and not stored permanently.")
    
    # File Upload Section
    st.header("Upload Excel File")
    uploaded_file = st.file_uploader(
        "Choose an Excel file", 
        type=['xlsx', 'xls'],
        help="Maximum file size: 100 MB. Only .xlsx and .xls files allowed."
    )
    
    if uploaded_file is not None:
        try:
            # Validate file before processing
            validate_file(uploaded_file)
            
            # Securely process file
            df = secure_file_processing(uploaded_file)
            
            st.success("File uploaded successfully!")
            
            # Display file details with minimal information
            st.write("File Details:")
            st.write(f"Rows: {len(df)}")
            st.write(f"Columns: {len(df.columns)}")
            
            # Transform Button
            if st.button("Extract and Transform Data"):
                try:
                    flat_df = process_dataframe(df)
                    
                    st.subheader("Transformed Data Preview")
                    st.dataframe(flat_df.head())
                    
                    # Prepare secure downloads
                    csv = flat_df.to_csv(index=False)
                    excel_buffer = io.BytesIO()
                    flat_df.to_excel(excel_buffer, index=False)
                    excel_buffer.seek(0)
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"transformed_{secrets.token_hex(8)}.csv",
                            mime='text/csv'
                        )
                    with col2:
                        st.download_button(
                            label="Download Excel",
                            data=excel_buffer,
                            file_name=f"transformed_{secrets.token_hex(8)}.xlsx",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                    
                    st.success("Data transformed successfully!")
                
                except Exception as e:
                    st.error(f"Processing error: {str(e)}")
        
        except Exception as e:
            st.error(f"File upload error: {str(e)}")

if __name__ == "__main__":
    main()