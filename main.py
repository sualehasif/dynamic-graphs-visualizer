import streamlit as st
import pandas as pd
import numpy as np
import json

production = False

config_name = "graph_config.json"
graph_config = json.load(open(config_name))

graph_names = {}
for key in graph_config:
    name = graph_config[key]["name"]
    graph_names[name] = key

# We start with a select box to choose what goes on the side.
graph_selected = st.sidebar.selectbox(
    "Which graph would you like to view?", tuple(graph_names.keys())
)

# TODO: Add a slider later for how much we should subsample?


def display_graph(name, config=graph_config):
    st.write(f"## {name} Graph")
    data = pd.read_csv(f"{name}/{name}.adj_stats.csv.0")
    data.rename(str.strip, axis="columns", inplace=True)

    if not production:
        data = data[:1000]

    st.write(data.head())
    st.write(data.describe())
    st.write(data.info())
    st.write(data.shape)

    st.line_chart(data)


graph_to_display = graph_names[graph_selected]
display_graph(graph_to_display)
