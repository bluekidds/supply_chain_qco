# app.py
import streamlit as st
from visualization import display_tree
from db_operations import read_excel_and_populate_db, print_schema, print_table_contents, create_table

create_table(dbname='wbs.db')
read_excel_and_populate_db('../../data/wbs_code_final.xlsx')  # Ensure the Excel file path is correct

def main():
    st.title('WBS Visualization')
        
    
    if st.button('Print Database Schema'):
        print_schema()

    if st.button('Print Table Contents'):
        print_table_contents()
    
    tree = display_tree()
    st_pyecharts(tree)  # Assuming this function exists to render Pyecharts in Streamlit


if __name__ == "__main__":
    main()
