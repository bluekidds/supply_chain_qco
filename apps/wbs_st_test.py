import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def draw_wbs_tree():
    tree_dict = {
        "Root": {
            "MJ": None
        },
        "MJ": {
            "RAY": None,
            "VDZ": None,
            "VQP": None,
            "CHP": None
        },
        "RAY": {
            "RRH": None
        },
        "VDZ": {
            "RJI": None
        },
        "VQP": {
            "RJI": None,
            "UDS": None,
            "UMN": None
        },
        "CHP": {
            "KYU": None
        },
        "RRH": {
            "FAE": None,
            "PCA": None,
            "JSI": None
        },
        "RJI": {
            "FPR": None,
            "UMN": None
        },
        "UDS": {
            "GEBR": None,
            "LMOL": None,
            "DRE": None
        },
        "UMN": {
            "ZPH": None
        },
        "KYU": {
            "CIMK": None
        },
        "CIMK": {
            "YB": None,
            "JE": None,
            "SR": None
        }
    }

    # Create a NextworkX directed graph
    g = nx.DiGraph()
    g.add_node("Root", subset=0)
    g.add_node("MJ", subset=1)
    g.add_nodes_from(tree_dict["MJ"].keys(), subset=2)
    g.add_nodes_from([node for child in tree_dict["MJ"].keys() for node in tree_dict[child].keys()], subset=3)


    # Set the node positions
    pos = nx.multipartite_layout(g, subset_key="layer")

    # Draw the graph
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw(g, pos, with_labels=True, node_size=1500, font_size=8, node_color='lightblue', edge_color='gray', arrowsize=20, ax=ax)
    plt.title('WBS Tree Graph')
    st.pyplot(fig)

def main():
    st.title('Interactive WBS Tree Graph')
    st.sidebar.markdown('### Controls')
    st.sidebar.info("This app visualizes a Work Breakdown Structure (WBS) as a tree graph.")

    draw_wbs_tree()

if __name__ == "__main__":
    main()
