import streamlit as st
import pandas as pd
import io
import unicodedata
import os
from collections import defaultdict
from utils import process_dataframe

def main():
    st.title("Radiomics Data Transformer")
    
    # File Upload Section
    st.header("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Read the uploaded file
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Feuil1')
            st.success("File uploaded successfully!")
            
            # Display file details
            st.write("File Details:")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"File Size: {uploaded_file.size} bytes")
            st.write(f"Number of Rows: {len(df)}")
            st.write(f"Number of Columns: {len(df.columns)}")
            
            # Transform Button
            if st.button("Extract and Transform Data"):
                # Process the dataframe
                try:
                    flat_df = process_dataframe(df)
                    
                    # Display first few rows of transformed data
                    st.subheader("Transformed Data Preview")
                    st.dataframe(flat_df.head())
                    
                    # Prepare download
                    csv = flat_df.to_csv(index=False)
                    
                    # Create an in-memory Excel file
                    excel_buffer = io.BytesIO()
                    flat_df.to_excel(excel_buffer, index=False)
                    excel_buffer.seek(0)
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"transformed_{uploaded_file.name.replace('.xlsx', '.csv')}",
                            mime='text/csv'
                        )
                    with col2:
                        st.download_button(
                            label="Download as Excel",
                            data=excel_buffer,
                            file_name=f"transformed_{uploaded_file.name}",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                    
                    st.success("Data transformed successfully!")
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()