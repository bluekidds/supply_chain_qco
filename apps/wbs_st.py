import streamlit as st
import pandas as pd
from pyvis.network import Network
import os

# WBS codes provided
wbs_codes = [
    "MJ",
    "MJ-RAY",
    "MJ-RAY-RRH",
    "MJ-RAY-RRH-FAE",
    "MJ-RAY-RRH-PCA",
    "MJ-RAY-RRH-JSI",
    "MJ-VDZ",
    "MJ-VDZ-RJI",
    "MJ-VDZ-RJI-FPR",
    "MJ-VDZ-RJI-FPR-AA",
    "MJ-VQP",
    "MJ-VQP-RJI-FPR-OC",
    "MJ-VQP-RJI-FPR-NU",
    "MJ-VQP-RJI-FPR-TF",
    "MJ-VQP-UDS",
    "MJ-VQP-UDS-GEBR",
    "MJ-VQP-UDS-GEBR-JL",
    "MJ-VQP-UDS-LMOL",
    "MJ-VQP-UDS-LMOL-SZJ",
    "MJ-VQP-UDS-LMOL-EE",
    "MJ-VQP-UDS-DRE",
    "MJ-VQP-UDS-DRE-NB",
    "MJ-VQP-UMN",
    "MJ-VQP-UMN-ZPH",
    "MJ-VQP-UMN-ZPH-ZV",
    "MJ-VQP-UMN-ZPH-FZ",
    "MJ-VQP-UMN-ZPH-XH",
    "MJ-VQP-UMN-ZPH-DA",
    "MJ-CHP",
    "MJ-CHP-KYU",
    "MJ-CHP-KYU-IMN",
    "MJ-CHP-KYU-CIMK",
    "MJ-CHP-KYU-CIMK-YB",
    "MJ-CHP-KYU-CIMK-YB-TNO",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX-XMTU",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX-RQXC",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX-DHNR",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX-XNOB",
    "MJ-CHP-KYU-CIMK-YB-TNO-DX-IUKK",
    "MJ-CHP-KYU-CIMK-YB-PIH",
    "MJ-CHP-KYU-CIMK-YB-PIH-YL",
    "MJ-CHP-KYU-CIMK-YB-PIH-YL-ORRM",
    "MJ-CHP-KYU-CIMK-YB-PIH-HV",
    "MJ-CHP-KYU-CIMK-YB-PIH-HV-SRVD",
    "MJ-CHP-KYU-CIMK-YB-PIH-RH",
    "MJ-CHP-KYU-CIMK-YB-PIH-RH-AWNK",
    "MJ-CHP-KYU-CIMK-YB-PIH-RH-LMWG",
    "MJ-CHP-KYU-CIMK-YB-PIH-RH-GIVB",
    "MJ-CHP-KYU-CIMK-YB-PIH-UN",
    "MJ-CHP-KYU-CIMK-YB-PIH-UN-LSAN",
    "MJ-CHP-KYU-CIMK-YB-LWO",
    "MJ-CHP-KYU-CIMK-YB-LWO-TE",
    "MJ-CHP-KYU-CIMK-YB-LWO-TE-REGS",
    "MJ-CHP-KYU-CIMK-YB-LWO-XS",
    "MJ-CHP-KYU-CIMK-YB-LWO-XS-QRDJ",
    "MJ-CHP-KYU-CIMK-YB-LWO-FM",
    "MJ-CHP-KYU-CIMK-YB-LWO-FM-QPAM",
    "MJ-CHP-KYU-CIMK-YB-LWO-FM-SESN",
    "MJ-CHP-KYU-CIMK-YB-LWO-FM-OXCM",
    "MJ-CHP-KYU-CIMK-YB-LWO-EH",
    "MJ-CHP-KYU-CIMK-YB-LWO-EH-HJAL",
    "MJ-CHP-KYU-CIMK-YB-LWO-EH-HKSV",
    "MJ-CHP-KYU-CIMK-YB-LWO-EH-XJYS",
    "MJ-CHP-KYU-CIMK-YB-JPM",
    "MJ-CHP-KYU-CIMK-YB-JPM-TV",
    "MJ-CHP-KYU-CIMK-YB-JPM-TV-CSJY",
    "MJ-CHP-KYU-CIMK-YB-JPM-XO",
    "MJ-CHP-KYU-CIMK-YB-JPM-XO-IGNR",
    "MJ-CHP-KYU-CIMK-YB-JPM-EG",
    "MJ-CHP-KYU-CIMK-YB-JPM-EG-SRPD",
    "MJ-CHP-KYU-CIMK-JE",
    "MJ-CHP-KYU-CIMK-JE-ACX",
    "MJ-CHP-KYU-CIMK-JE-ACX-DW",
    "MJ-CHP-KYU-CIMK-JE-ACX-DW-SLPI",
    "MJ-CHP-KYU-CIMK-JE-ACX-DW-XBNG",
    "MJ-CHP-KYU-CIMK-JE-ACX-DW-NZGV",
    "MJ-CHP-KYU-CIMK-JE-ACX-DW-INLT",
    "MJ-CHP-KYU-CIMK-JE-DAM",
    "MJ-CHP-KYU-CIMK-JE-DAM-GV",
    "MJ-CHP-KYU-CIMK-JE-DAM-GV-MFJO",
    "MJ-CHP-KYU-CIMK-JE-DAM-YE",
    "MJ-CHP-KYU-CIMK-JE-DAM-YE-RXPJ",
    "MJ-CHP-KYU-CIMK-JE-DAM-YE-ZOCL",
    "MJ-CHP-KYU-CIMK-JE-AEG",
    "MJ-CHP-KYU-CIMK-JE-AEG-DH",
    "MJ-CHP-KYU-CIMK-JE-AEG-DH-PYBM",
    "MJ-CHP-KYU-CIMK-JE-AEG-VJ",
    "MJ-CHP-KYU-CIMK-JE-AEG-VJ-FPXK",
    "MJ-CHP-KYU-CIMK-JE-AEG-KA",
    "MJ-CHP-KYU-CIMK-JE-AEG-KA-PWLZ",
    "MJ-CHP-KYU-CIMK-JE-AEG-KA-JEWF",
    "MJ-CHP-KYU-CIMK-JE-AEG-KA-OWAL",
    "MJ-CHP-KYU-CIMK-JE-AEG-VS",
    "MJ-CHP-KYU-CIMK-JE-AEG-VS-SXVP",
    "MJ-CHP-KYU-CIMK-JE-QAO",
    "MJ-CHP-KYU-CIMK-JE-QAO-JH",
    "MJ-CHP-KYU-CIMK-JE-QAO-TK",
    "MJ-CHP-KYU-CIMK-JE-BBV",
    "MJ-CHP-KYU-CIMK-JE-BBV-FX",
    "MJ-CHP-KYU-CIMK-JE-BBV-NN",
    "MJ-CHP-KYU-CIMK-SR",
    "MJ-CHP-KYU-CIMK-SR-XMT",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-MAGD",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-POXP",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-DJEN",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-TQUN",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-EINJ",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-MMFF",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-EBFX",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-TABT",
    "MJ-CHP-KYU-CIMK-SR-XMT-PO-JFKD",
    "MJ-CHP-KYU-CIMK-SR-RDM",
    "MJ-CHP-KYU-CIMK-SR-RDM-KC",
    "MJ-CHP-KYU-CIMK-SR-RDM-KC-SBYC",
    "MJ-CHP-KYU-CIMK-SR-RDM-WL",
    "MJ-CHP-KYU-CIMK-SR-RDM-WL-KUNP",
    "MJ-CHP-KYU-CIMK-SR-RDM-SO",
    "MJ-CHP-KYU-CIMK-SR-RDM-SO-GDOH",
    "MJ-CHP-KYU-CIMK-SR-RDM-SO-LWXT",
    "MJ-CHP-KYU-CIMK-SR-RDM-SO-OSFK",
    "MJ-CHP-KYU-CIMK-SR-RDM-DN",
    "MJ-CHP-KYU-CIMK-SR-RDM-DN-HTCL",
    "MJ-CHP-KYU-CIMK-SR-KCV",
    "MJ-CHP-KYU-CIMK-SR-KCV-CS",
    "MJ-CHP-KYU-CIMK-SR-KCV-CS-CCQK",
    "MJ-CHP-KYU-CIMK-SR-KCV-FR",
    "MJ-CHP-KYU-CIMK-SR-KCV-FR-HOCD",
    "MJ-CHP-KYU-CIMK-SR-KCV-FR-LTCN",
    "MJ-CHP-KYU-CIMK-SR-KCV-QH",
    "MJ-CHP-KYU-CIMK-SR-KCV-QH-JPZW",
    "MJ-CHP-KYU-CIMK-SR-KCV-QH-NXDQ",
    "MJ-CHP-KYU-CIMK-SR-TLN",
    "MJ-CHP-KYU-CIMK-SR-TLN-YM",
    "MJ-CHP-KYU-CIMK-SR-TLN-YM-VPET",
    "MJ-CHP-KYU-CIMK-SR-TLN-UZ",
    "MJ-CHP-KYU-CIMK-SR-TLN-UZ-RZSI",
    "MJ-CHP-KYU-CIMK-SR-TLN-UZ-RXOQ",
    "MJ-CHP-KYU-CIMK-SR-TLN-JF",
    "MJ-CHP-KYU-CIMK-SR-TLN-JF-XUKM",
    "MJ-CHP-KYU-CIMK-SR-TLN-JF-LCAO",
    "MJ-CHP-KYU-CIMK-SR-PZL",
    "MJ-CHP-KYU-CIMK-SR-PZL-KN",
    "MJ-CHP-KYU-CIMK-SR-PZL-KN-EFXH",
    "MJ-CHP-KYU-CIMK-SR-PZL-DO",
    "MJ-CHP-KYU-CIMK-SR-PZL-DO-DNSM",
    "MJ-CHP-KYU-CIMK-SR-PZL-RE",
    "MJ-CHP-KYU-CIMK-SR-PZL-RE-DSIH",
    "MJ-CHP-KYU-CIMK-SR-PZL-RE-TOYC",
    "MJ-CHP-KYU-CIMK-SR-PZL-RE-XUGI",
    "MJ-CHP-KYU-CIMK-SR-PZL-JP",
    "MJ-CHP-KYU-CIMK-SR-PZL-JP-PNCZ",
    "MJ-CHP-KYU-CIMK-SR-RVE",
    "MJ-CHP-KYU-CIMK-SR-RVE-JR",
    "MJ-CHP-KYU-CIMK-SR-RVE-JR-YALP",
    "MJ-CHP-KYU-CIMK-SR-RVE-FZ",
    "MJ-CHP-KYU-CIMK-SR-RVE-FZ-GJKX",
    "MJ-CHP-KYU-CIMK-SR-RVE-JU",
    "MJ-CHP-KYU-CIMK-SR-RVE-JU-EVNW",
    "MJ-CHP-KYU-CIMK-SR-RVE-JU-OIDL",
    "MJ-CHP-KYU-CIMK-SR-RVE-JU"
]

# Create the interactive network graph
def create_interactive_graph(wbs_codes):
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based()

    # Add nodes and edges
    for code in wbs_codes:
        path = code.split("-")
        for node in path:
            net.add_node(node, title=node)
        for i in range(len(path) - 1):
            parent = path[i]
            child = path[i + 1]
            net.add_edge(parent, child)

    # Save to HTML file and read back the content
    path = "wbs_network.html"
    net.save_graph(path)
    with open(path, "r") as file:
        html = file.read()
    os.remove(path)  # Clean up file after reading
    return html

# Generate interactive graph HTML
graph_html = create_interactive_graph(wbs_codes)

# Create a DataFrame for the table
def create_wbs_table(wbs_codes):
    data = []
    for code in wbs_codes:
        path = code.split("-")
        for i in range(len(path) - 1):
            parent = path[i]
            child = path[i + 1]
            data.append({'Node': child, 'Path': f'{parent} -> {child}'})
    df = pd.DataFrame(data)
    return df[['Node', 'Path']].drop_duplicates().sort_values(by='Node')

def print_hierarchy(hierarchy, indent=0):
    output = ""
    for key, value in hierarchy.items():
        output += "&nbsp;&nbsp;&nbsp;" * indent + f"└─ {key}<br>"
        output += print_hierarchy(value, indent + 1)
    return output

# Generate hierarchy
hierarchy = {}
for code in wbs_codes:
    path = code.split("-")
    current_level = hierarchy
    for level in path:
        current_level = current_level.setdefault(level, {})


# Prepare the data table
wbs_table = create_wbs_table(wbs_codes)

# Streamlit layout
st.title('Interactive WBS Visualization with Network and Table')
#col1, col2 = st.columns([2, 1])  # Adjust column widths as needed


#st.subheader('Interactive WBS Network')
#st.components.v1.html(graph_html, height=800)

st.subheader('WBS Hierarchy')
st.markdown(print_hierarchy(hierarchy), unsafe_allow_html=True)
st.subheader('WBS Path Table')
st.table(wbs_table) 