import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
import json

def load_data(filename):
    try:
        return pd.read_csv(filename, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(filename, encoding='ISO-8859-1')  #

# Parse data into a hierarchical JSON for eCharts
def parse_wbs_data2(df):
    tree = {}
    for index, row in df.iterrows():
        parts = row['wbs-code'].split('-')
        current_dict = tree
        for part in parts:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        # Assume 'description' column exists in your dataframe
        current_dict['description'] = row['Description']
        
        # Optionally set 'name' to use as label in the tree
        current_dict['name'] = part

    return tree
def parse_wbs_data(df):
    tree = {}

    for index, row in df.iterrows():
        parts = row['wbs-code'].split('-')
        current_level = tree

        for i, part in enumerate(parts):
            if part not in current_level:
                current_level[part] = {}

            # Move deeper in the hierarchy
            current_level = current_level[part]

            # Assign descriptions at L3 and L4 levels based on the index
            if i == 2:  # L3 level
                current_level['description'] = row.get('L3 Desc', 'No L3 Description')
            elif i == 3:  # L4 level
                current_level['description'] = row.get('L4 Desc', 'No L4 Description')
            else:
                current_level['description'] = row.get('Description', '')  # Other levels use the general description

    return tree



def parse_wbs_data1(df):
    tree = {}
    for index, row in df.iterrows():
        parts = row['wbs-code'].split('-')
        current_level = tree
        depth = 1  # Start depth from 1 as the root level
        
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
            depth += 1  # Increase depth as we go deeper in the hierarchy
        st.write(str(depth)+' '+row.get('L3 Desc', ''))
        # Assign description based on depth
        if depth == 3:  # Third level
            current_level['description'] = row.get('L3 Desc', '')
            
        elif depth == 4:  # Fourth level
            current_level['description'] = row.get('L4 Desc', '')
            
        else:
            current_level['description'] = row.get('Description', '')  # Other levels use the general description
            
    return tree

def build_tree_structure(data, parent_name='', depth=0):
    """ Recursive function to build the tree structure for eCharts.
    Args:
        data (dict or str): The hierarchical data.
        parent_name (str): The name of the current node.
        depth (int): Current depth in the tree to handle specific layers.
    Returns:
        dict: A dictionary representing the node in eCharts compatible format.
    """
    # Check if the input data is a dictionary and iterate through it
    if isinstance(data, dict):
        children = []
        node_description = data.get('description', 'No description available')

        # Iterate through keys in the dictionary, skipping the description key
        for key, value in data.items():
            if key == 'description':
                continue
            # Increase the depth as we go one level deeper in the hierarchy
            child = build_tree_structure(value, key, depth + 1)
            if child:
                children.append(child)
        
        # Create the node with or without children
        node = {
            'name': parent_name,
            'children': children if children else None,
            'value': node_description
        }
        return node

    # Base case: if the data is a string, it's assumed to be the description
    elif isinstance(data, str):
        return {
            'name': parent_name,
            'value': data
        }


def build_tree_structure1(tree, parent_name=''):
    node_list = []
    for key, value in tree.items():
        if isinstance(value, dict):
            child = build_tree_structure(value, key)
            node_list.append({
                "name": key,
                "description": value.get('description', 'No description'),
                "children": child
            })
    return node_list


def build_tree_structure3(data, parent_name=''):
    """ Recursive function to build the tree structure for eCharts """
    if isinstance(data, dict):
        children = []
        for key, value in data.items():
            if key == 'description':  # Skip the description at current node level
                continue
            child = build_tree_structure(value, key)
            if child:
                children.append(child)
        node = {
            'name': parent_name,
            'children': children,
            'value': data.get('description', 'No description available')  # Use description if available
        }
        return node
    elif isinstance(data, str):  # Base case: when the data is just the description
        return {
            'name': parent_name,
            'value': data  # Setting the node's description as value
        }


def build_tree_structure2(d, parent_name=""):
    node_data = {}
    if 'description' in d:
        node_data['name'] = f"{parent_name} - {d['description']}"  # Detailed name with description
    else:
        node_data['name'] = parent_name

    # Collect children
    children = [build_tree_structure(value, f"{parent_name}-{key}" if parent_name else key)
                for key, value in d.items() if key not in ['name', 'description']]
    if children:
        node_data['children'] = children
    
    return node_data


# Generate eCharts options
def generate_chart_options(data):
    return {
        "tooltip": {
        "trigger": 'item',
        "triggerOn": 'mousemove',
        "formatter": "{b}"
        },
        "series": [
            {
                "type": 'tree',
                "data": data,
                "top": '1%',
                "left": '7%',
                "bottom": '1%',
                "right": '20%',
                "symbolSize": 7,
                "label": {
                    "position": 'left',
                    "verticalAlign": 'middle',
                    "align": 'right',
                    "fontSize": 9,
                },
                "leaves": {
                    "label": {
                        "position": 'right',
                        "verticalAlign": 'middle',
                        "align": 'left'
                    }
                },
                "emphasis": {
                    "focus": 'descendant'
                },
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750
            }
        ]
    }
def render_chart(tree_data):
    options = {
        "tooltip": {
            "trigger": 'item',
            "triggerOn": 'mousemove'
        },
        "series": [
            {
                "type": 'tree',
                "data": [tree_data],
                "top": '1%',
                "left": '7%',
                "bottom": '1%',
                "right": '20%',
                "symbolSize": 10,
                "label": {
                    "position": 'left',
                    "verticalAlign": 'middle',
                    "align": 'right',
                    "fontSize": 9
                },
                "leaves": {
                    "label": {
                        "position": 'right',
                        "verticalAlign": 'middle',
                        "align": 'left'
                    }
                },
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750
            }
        ]
    }
    st_echarts(options=options, height="800px")



def main():
    st.title('WBS Visualization')
    
    df = load_data('../data/wbs_source_formatted.csv')
    wbs_tree = parse_wbs_data(df)
    tree = build_tree_structure(wbs_tree)
    #tree = build_tree_structure(wbs_tree['BR'])  # Assuming the root key is 'BR' based on your data
    options = {
    'tooltip': {
        'trigger': 'item',
        'triggerOn': 'mousemove',
        'formatter': '{b}: {c}'  # Here, {b} is the node's name, and {c} is the value (description)
    },
    'series': [{
        'type': 'tree',
        'data': [tree],
        'top': '1%',
        'left': '7%',
        'bottom': '1%',
        'right': '20%',
        'symbolSize': 10,
        'label': {
            'position': 'left',
            'verticalAlign': 'middle',
            'align': 'right',
            'fontSize': 9
        },
        'leaves': {
            'label': {
                'position': 'right',
                'verticalAlign': 'middle',
                'align': 'left'
            }
        },
        'expandAndCollapse': True,
        'animationDuration': 550,
        'animationDurationUpdate': 750
    }]
}

    options2 = {
        'tooltip': {
            'trigger': 'item',
            'triggerOn': 'mousemove',
            'formatter': '{b}: {c}'
        },
        'series': [{
            'type': 'tree',
            'data': [tree],
            'top': '5%',
            'left': '7%',
            'bottom': '2%',
            'right': '20%',
            'symbolSize': 10,
            'label': {
                'position': 'left',
                'verticalAlign': 'middle',
                'align': 'right',
                'fontSize': 9
            },
            'leaves': {
                'label': {
                    'position': 'right',
                    'verticalAlign': 'middle',
                    'align': 'left'
                }
            },
            'expandAndCollapse': True,
            'animationDuration': 550,
            'animationDurationUpdate': 750,
            'roam': True,
            'levels': [  # Define the style for each level
                {'depth': 0, 'color': '#ccccff', 'itemStyle': {'borderColor': '#777', 'borderWidth': 2, 'gapWidth': 3}},
                {'depth': 1, 'color': '#99ccff', 'itemStyle': {'borderColor': '#555', 'borderWidth': 2, 'gapWidth': 2}},
                {'depth': 2, 'color': '#99cccc', 'itemStyle': {'borderColor': '#333', 'borderWidth': 1, 'gapWidth': 1}}
            ]
        }]
    }

    st_echarts(options=options2, height="800px")
if __name__ == "__main__":
    
    main()
