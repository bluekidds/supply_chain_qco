from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
from hydralit import HydraApp
from streamlit_agraph import agraph, Node, Edge
try:
    st.set_page_config(layout="wide")
except:
    pass

def load_data(file):
    if file is not None:
        # Adjusted to load data from the 'MTO' sheet starting from row 10 (0-indexed to 11th row)
        df = pd.read_excel(file, sheet_name='MTO', skiprows=10)
        return df
    else:
        return None

def display_project_details(details):
    with st.container():
        
        col1, col2 = st.columns([1, 2])
        with col2:
            st.markdown("""
                <div style="text-align: right;">
                    <p><b>Project No.:</b> {0}</p>
                    <p><b>MTO Description:</b> {1}</p>
                    <p><b>Project Name:</b> {2}</p>
                    <p><b>MTO Status:</b> {3}</p>
                    <p><b>Design Status:</b> {4}</p>
                    <p><b>Version No.:</b> {5}</p>
                </div>
            """.format(
                details["Project No."], details["MTO Description"],
                details["Project Name"], details["MTO Status"],
                details["Design Status"], details["Version No."]
            ), unsafe_allow_html=True)
        st.divider()

def display_wbs_structure(df):
    with st.container():
        if df is not None:
            
            st.table(df)
            st.divider()

            
        if df is not None and 'WBS' in df.columns:
            st.subheader("MTO Breakdown by WBS")
            grouped_data = df.groupby('WBS')
            for name, group in grouped_data:
                with st.expander(f"WBS: {name}"):
                    st.table(group[['Comcode / Equip Tag', 'Qty']])
        else:
            st.error("The required columns are not present in the uploaded file.")
class Config:
    def __init__(self, height, width, directed, nodeHighlightBehavior, highlightColor):
        self.height = height
        self.width = width
        self.directed = directed
        self.nodeHighlightBehavior = nodeHighlightBehavior
        self.highlightColor = highlightColor


def prepare_graph_data(df):
    # Initialize lists for nodes and edges
    nodes = []
    edges = []

    # Assume we have columns 'ID', 'ParentID' for simplicity
    for index, row in df.iterrows():
        node_id = str(row['ID'])
        parent_id = str(row['ParentID']) if 'ParentID' in row and pd.notna(row['ParentID']) else None
        
        # Create a node for each entry
        nodes.append(Node(id=node_id, label=node_id, size=400, color="#B3B3B3"))
        
        # Create an edge if there's a parent ID
        if parent_id:
            edges.append(Edge(source=parent_id, target=node_id, type="CURVE_SMOOTH"))

    return nodes, edges




def main():
    st.title("Material Takeoff (MTO) Report")

    # File uploader in the sidebar
    with st.sidebar:
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
        upload_clicked = st.button('Upload and Process MTO')

    # Display functions in the main page
    if upload_clicked:
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            # Extract project details
            project_details_df = pd.read_excel(uploaded_file, sheet_name='MTO', skiprows=2, nrows=3, header=None, usecols="B,G")
            details = {
                "Project No.": project_details_df.iloc[0, 0],  # Assuming second column of first row
                "MTO Description": project_details_df.iloc[0, 1],  # Assuming sixth column of first row
                "Project Name": project_details_df.iloc[1, 0],  # Second column of second row
                "MTO Status": project_details_df.iloc[1, 1],  # Sixth column of second row
                "Design Status": project_details_df.iloc[2, 0],  # Second column of third row
                "Version No.": project_details_df.iloc[2, 1]  # Sixth column of third row
            }
            display_project_details(details)
            display_wbs_structure(df)
        else:
            st.error("Please upload a file to process.")

        # Prepare nodes and edges lists
    
        df = pd.read_csv('../data/wbs.csv', header=None, names=['Child', 'Parent'])
        
        # Create a set of unique nodes
        node_ids = pd.concat([df['Child'], df['Parent']]).unique()
        
        nodes = []
        edges = []
        
        # Generate nodes with a label and id
        for node_id in node_ids:
            nodes.append(Node(id=node_id, label=node_id, color="skyblue"))
        
        # Generate edges from the parent to the child
        for _, row in df.iterrows():
            edges.append(Edge(source=row['Parent'], target=row['Child'], type='CURVE_SMOOTH'))
        
        # Hierarchical layout configuration
        config = Config(width=1000, height=600, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6", hierarchical=True, hierarchicalConfig={
            "direction": "UD",  # Direction can be UD (up-down), DU (down-up), LR (left-right), RL (right-left)
            "sortMethod": "directed"  # directed or hubsize
        })

        
        return_value = agraph(nodes=nodes, edges=edges, config=config)
    
    

if __name__ == "__main__":
    main()