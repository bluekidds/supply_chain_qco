import streamlit as st
import pandas as pd
import sqlite3
from st_aggrid import AgGrid, JsCode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme

# Load the Excel data
excel_file = '../data/AMTO_Import_3327_2022-12-06T00_46_31.291870 (1) (3).xlsx'

# Read specific sheets
commodity_data = pd.read_excel(excel_file, sheet_name='commodity data')
equipment_data = pd.read_excel(excel_file, sheet_name='Equipment Tag')
MTO_data = pd.read_excel(excel_file, sheet_name='AMTO', skiprows=6)

excel_data = pd.ExcelFile(excel_file)

# Create a SQLite database
conn = sqlite3.connect('project_database.db')

# Write the data to SQL
# Write all sheets to SQL
for sheet_name in excel_data.sheet_names:
    if sheet_name=='AMTO':
        df = pd.read_excel(excel_file, sheet_name='AMTO', skiprows=6) 
    else:
        df = pd.read_excel(excel_data, sheet_name=sheet_name)
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)

#commodity_data.to_sql('commodity_data', conn, if_exists='replace', index=False)
#equipment_data.to_sql('equipment_data', conn, if_exists='replace', index=False)
def load_data(file):
    if file is not None:
        # Load data starting from row 6 (7th row, as indexing starts at 0)
        # and assuming the headers are at this row.
        df = pd.read_excel(file, skiprows=6)
        return df
    else:
        return None

def display_project_details(file):
    if file is not None:
        # Load only the first three rows to display project details
        project_details = pd.read_excel(file, nrows=3)
        st.write("## Project Details")
        for index, row in project_details.iterrows():
            st.text(f"{row[0]}: {row[1]}")

def display_wbs_structure(df):
    if df is not None:
        st.write("## Full MTO List")
        st.dataframe(df)

        st.write("## MTO Breakdown by WBS")
        if 'WBS' in df.columns and 'Material Code' in df.columns and 'Quantity' in df.columns:
            grouped_data = df.groupby('WBS')
            for name, group in grouped_data:
                st.subheader(f"WBS: {name}")
                st.table(group[['Material Code', 'Quantity']])
        else:
            st.error("The required columns ('WBS', 'Material Code', 'Quantity') are not present in the uploaded file.")
    else:
        st.warning("No file uploaded. Please upload an Excel file containing the MTO data.")


def draw_hierarchy(wbs_code):
    # Parse the WBS code to extract hierarchy
    parts = wbs_code.split('-')
    G = nx.DiGraph()
    # Add nodes and edges based on hierarchy
    for i in range(len(parts)):
        node = '-'.join(parts[:i+1])
        if i > 0:
            parent = '-'.join(parts[:i])
            G.add_edge(parent, node)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 5))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=2000, font_size=10, font_color='black')
    plt.title('Work Breakdown Structure Hierarchy')
    plt.show()
    st.pyplot(plt)



# Streamlit application
def app():
    st.title('MTO Viewer')

    # Connect to the database
    conn = sqlite3.connect('project_database.db')

    # Allow the user to select a sheet to view
    sheet_name = st.selectbox('Select a sheet to display', excel_data.sheet_names)

    # Load and display the selected sheet
    query = f"SELECT * FROM `{sheet_name}`"
    df = pd.read_sql(query, conn)
    # Load and display the selected sheet
    # Special handling for the 'wbs data' sheet
    if sheet_name == 'wbs data':
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection('single', use_checkbox=False)
        grid_options = gb.build()

        response = AgGrid(
            df, 
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True
        )

        #selected = response['selected_rows'][0]
        
        if response['selected_rows']:  # Check if any row is selected
            selected_row_data = response['selected_rows']
            wbs_code = selected_row_data['Work Breakdown Structure']
            st.table(wbs_code)
            draw_hierarchy(wbs_code)


    else:
        #query = f"SELECT * FROM `{sheet_name}`"
        #df = pd.read_sql(query, conn)
        gb = GridOptionsBuilder.from_dataframe(df)
        grid_res = AgGrid(
            df,
            gridOptions=gb.build(),
            theme=AgGridTheme.BALHAM,
            height=800,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            width='100%'
        )
    #AgGrid(df)
def app2():
    st.title('Project Data Viewer')

    # Connect to the database
    conn = sqlite3.connect('project_database.db')
    query = "SELECT * FROM commodity_data"
    query_equipment = "SELECT * FROM equipment_data"

    # Load and display commodity data
    st.subheader('Commodity Data')
    commodity_df = pd.read_sql(query, conn)
    gd_commodity = GridOptionsBuilder.from_dataframe(commodity_df)
    gd_commodity.configure_pagination(enabled=True)
    #gd_commodity.configure_selection(selection_mode='single', use_checkbox=True)
    gridOptions = gd_commodity.build()
    grid_commodity_table = AgGrid(commodity_df, 
                                  gridOptions=gridOptions,
                                  fit_columns_on_grid_load=True,
                                  height=500,
                                  width='100%',
                                  theme="streamlit",
                                  update_mode=GridUpdateMode.GRID_CHANGED,
                                  reload_data=True,
                                  allow_unsafe_jscode=True,
                                  editable=True)
    # Load and display equipment data
    st.subheader('Equipment Data')
    
    equipment_df = pd.read_sql(query_equipment, conn)
    gd_equipment = GridOptionsBuilder.from_dataframe(equipment_df)
    gd_equipment.configure_pagination(enabled=True)
    gd_equipment.configure_selection(selection_mode='single', use_checkbox=True)
    gridOptions_equipment = gd_equipment.build()
    grid_commodity_table = AgGrid(equipment_df, 
                                  gridOptions=gridOptions_equipment,
                                  fit_columns_on_grid_load=True,
                                  height=500,
                                  width='100%',
                                  theme="streamlit",
                                  update_mode=GridUpdateMode.GRID_CHANGED,
                                  reload_data=True,
                                  allow_unsafe_jscode=True,
                                  editable=True)
    #AgGrid(equipment_df)

if __name__ == "__main__":
    app()
