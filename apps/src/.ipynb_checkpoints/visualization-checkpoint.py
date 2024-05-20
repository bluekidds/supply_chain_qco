# visualization.py
import sqlite3
from pyecharts import options as opts
from pyecharts.charts import Tree
import streamlit as st

def fetch_data():
    conn = sqlite3.connect('wbs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, parent_id FROM WBS_Elements ORDER BY level")
    records = cursor.fetchall()
    conn.close()
    return build_tree(records)

def build_tree(records):
    tree = {}
    for id, name, description, parent_id in records:
        node = {'name': name, 'value': description, 'children': []}
        if parent_id is None:
            tree[id] = node
        else:
            tree[parent_id]['children'].append(node)
    root = next(iter(tree.values()))  # Assumes there is only one root
    return root

def display_tree():
    tree_data = [fetch_data()]
    tree = (
        Tree()
        .add("", tree_data, orient="LR", initial_tree_depth=-1)
        .set_global_opts(title_opts=opts.TitleOpts(title="WBS Tree"))
        .set_series_opts(
            label_opts=opts.LabelOpts(position="right", vertical_align="middle", align="left", font_size=9),
            leaves_opts=opts.LeavesOpts(label_opts=opts.LabelOpts(position="right", vertical_align="middle", align="left")),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"),
        )
    )
    return tree
