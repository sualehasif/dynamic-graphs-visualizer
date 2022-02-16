from random import sample
import streamlit as st
import pandas as pd
import numpy as np
import os
import json

production = True

# """
# DONE: side by side comparison of graphs
# DONE: choose which graphs to view with radio buttons
# TODO: link sharing
# TODO: put data per graph
# """

data_directory = "compressed-data"
config_name = "graph_config.json"

graph_config = json.load(open(config_name))
st.set_page_config(layout="wide")

all_fields = [
    "num_nodes", "num_edges", "average_degree", "max_degree", "num_triangles",
    "new_edges"
]

graph_names = {}
for key in graph_config:
    name = graph_config[key]["name"]
    graph_names[name] = key

# We start with a select box to choose what goes on the side.

side_by_side = st.sidebar.checkbox("Open a side by side comparison",
                                   value=False)

if not side_by_side:
    graph_selected = st.sidebar.selectbox(
        "Which graph would you like to view?", tuple(graph_names.keys()))
else:
    graph_selected = 0
    side_graph_1 = st.sidebar.selectbox(
        "Which graph would you like to view on the left?",
        tuple(graph_names.keys()))
    side_graph_2 = st.sidebar.selectbox(
        "Which graph would you like to view on the right?",
        tuple(graph_names.keys()))

    fields = all_fields.copy()

    props_to_display = [False] * len(fields)

    st.sidebar.markdown("Which properties would you like to view?")
    for i, field in enumerate(fields):
        props_to_display[i] = st.sidebar.checkbox(field)

# TODO: Add a slider later for how much we should subsample?


def get_data(graph_name, col=None, config=graph_config, props_selected=None):
    dir_name = os.path.join(data_directory, config[graph_name]["directory"])

    files = [f for f in os.listdir(dir_name)]

    fields = all_fields.copy()

    # overwrite with props if necessary
    new_fields = []
    if props_selected is not None:
        for i, prop in enumerate(props_selected):
            if prop:
                new_fields.append(fields[i])
        if len(new_fields) != 0:
            fields = new_fields

    # dont display many fields if not in production.
    if not production:
        files = files[:4]

    dfs = []
    for fname in files:
        df_file = os.path.join(dir_name, fname)
        dfs.append((fname, pd.read_csv(df_file, skipinitialspace=True)))

    for field in fields:
        longest_df = dfs[0][1]
        for d in dfs[1:]:
            if len(d[1].index) > len(longest_df.index):
                longest_df = d[1]
        df = pd.DataFrame(longest_df["timestep"])
        for d in dfs:
            df[d[0]] = d[1][field]
        # set the index to be the timestep
        df.set_index("timestep", inplace=True)

        # subsample the data

        df_size = len(df.index)
        if df_size > 10**8:
            sample_rate = 400
        else:
            sample_rate = 50
        df = df.iloc[::sample_rate]

        if col is not None:
            with col:
                st.write(f"### {field}")
                with st.spinner(f"Calculating {field} for {name} ..."):
                    st.line_chart(df)
        else:
            st.write(f"### {field}")
            with st.spinner(f"Calculating {field} for {name} ..."):
                st.line_chart(df, width=700, use_container_width=False)

        # df.plot(x="timestep", legend=False)
        # plt.ylim(ymin=0)
        # plt.title(output_prefix.split("/")[-1]+"_"+field)
        # plt.savefig(output_prefix+"_"+field+".png", bbox_inches="tight")

    # for file in files:
    #     data = pd.read_csv(os.path.join(dir_name, file))
    #     data.rename(str.strip, axis="columns", inplace=True)

    # data = pd.read_csv(f"{data_directory}/{dir_name}/{graph_name}.adj_stats.csv.0")


# @st.cache
def make_line_chart(data):
    """
    Makes a line chart from the data.
    """
    with st.spinner("Making the line graph slowly ..."):
        st.line_chart(data)


def graph_displayer(graph_name,
                    col=None,
                    config=graph_config,
                    props_selected=None):

    # check if the description exists and if so display it
    if "description" in config[graph_name]:
        st.write(config[graph_name]["description"])

    get_data(graph_name, col, config, props_selected=props_selected)

    # st.write(data.head())
    # st.write(data.describe())

    # make_line_chart(data)


if graph_selected:
    graph_to_display = graph_names[graph_selected]
    title = graph_config[graph_to_display]["name"]
    st.title(f"{title} Graph")

    graph_displayer(graph_to_display)

if side_by_side:
    col1, col2 = st.columns(2)

    left_graph = graph_names[side_graph_1]
    left_name = graph_config[left_graph]["name"]
    col1.title(f"{left_name}")

    graph_displayer(left_graph, col=col1, props_selected=props_to_display)

    right_graph = graph_names[side_graph_2]
    right_name = graph_config[right_graph]["name"]
    col2.title(f"{right_name}")

    graph_displayer(right_graph, col=col2, props_selected=props_to_display)
