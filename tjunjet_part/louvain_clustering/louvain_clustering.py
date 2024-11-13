"""
This file uses Louvain clustering to cluster the graph into different communities.

We will then analyze the graph and 
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Reading the graph
G = nx.read_gml('../../graphs/skills_graph.gml')

# (a) Forming the louvain communities and saving the graph
communities = nx.algorithms.community.louvain_communities(G, seed=18755)


top_nodes = []

# Part (a): Print the number of nodes in each community.
# In addition, print the labels of the top 10 nodes with the highest
# degree of each community
print("================ Part (a) ================\n")
for i, community in enumerate(communities):
    community_subgraph = G.subgraph(community)
    print(f"Community {i+1}: {len(community)} nodes")

    # Sort based on their degrees
    # x[1] in the lambda function gives you the degree
    top_10_nodes = sorted(
        [(node, G.degree[node]) for node in community],
         key=lambda x: x[1], 
         reverse=True)[:10]

    # For part (c): Remove the other nodes that are not in the top_10
    for node, degree in top_10_nodes:
        top_nodes.append(node)

    # Printing the top 10 nodes
    print("Top 10 nodes by degree:")
    for node, degree in top_10_nodes:
        print(f"Node: {node}, Degree: {degree}")
    print("=========================================\n")

top_graph = G.subgraph(top_nodes)
colors = ['red', 'lightblue', 'green', 'yellow', 'pink']
# Create a color map for the nodes based on their community assignment

# Create a color map dictionary to store the color for each node in the top graph
color_map = {}
for i, community in enumerate(communities):
    community_color = colors[i % len(colors)]
    for node in community:
        if node in top_nodes:  # Only add color for nodes in the top_nodes subgraph
            color_map[node] = community_color

# Generate a list of colors in the correct order for the top_graph nodes
node_colors = [color_map[node] for node in top_graph.nodes]

# Visualize the network
plt.figure(figsize=(12, 12))
# Spring layout for better readability
pos = nx.spring_layout(top_graph, seed=42)
nx.draw_networkx_nodes(top_graph, pos, node_color=node_colors, node_size=2000)
nx.draw_networkx_edges(top_graph, pos, alpha=0.5)
nx.draw_networkx_labels(top_graph, pos, font_size=8, font_family="sans-serif")

plt.title("Top 10 Nodes by Degree in Each Community")
plt.savefig("figures/louvain_visualization.jpg")