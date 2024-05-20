import pandas as pd
import sqlite3
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Initialize the page setup
st.set_page_config(layout="wide")  # Set layout to wide mode

# Function to get table names from the database
def get_table_names():
    conn = sqlite3.connect('Supply_chain_db.db')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    table_names_df = pd.read_sql_query(query, conn)
    conn.close()
    return table_names_df['name'].tolist()

# Function to get table data
def get_table_data(table_name):
    conn = sqlite3.connect('Supply_chain_db.db')
    query = f"SELECT * FROM `{table_name}` LIMIT 50;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Streamlit app setup

# Sidebar for table selection
table_names = get_table_names()
selected_table = st.sidebar.radio("Select a Table to View", table_names)

# Configure grid options for AgGrid

if selected_table:
    st.subheader(f"Displaying {selected_table}")
    df = get_table_data(selected_table)

    grid_options = GridOptionsBuilder.from_dataframe(df)
    grid_options.configure_grid_options(domLayout='normal')  # Adjust layout as needed
    grid_options.configure_column("all", autoSize=True, autoSizePadding=10)  # Automatically size all columns with additional padding
    grid_response = AgGrid(
        df,
        gridOptions=grid_options.build(),
        fit_columns_on_grid_load=False,  # Turn off fit columns on load if using autoSize
        height=300,  # Set a fixed height or use 'autoHeight'
        theme='material'  # Use a valid theme
    )

