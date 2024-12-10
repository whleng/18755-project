import networkx as nx
import plotly.graph_objs as go
import numpy as np

# Read the graph
G = nx.read_gml('../../graphs/skills_graph.gml')

# Perform Louvain clustering
communities = nx.algorithms.community.louvain_communities(G, seed=42)

# Create a 3D layout for the graph
pos_3d = nx.spring_layout(G, dim=3, seed=42)  # 3D spring layout

# Normalize positions for Plotly
node_x = np.array([pos_3d[node][0] for node in G.nodes])
node_y = np.array([pos_3d[node][1] for node in G.nodes])
node_z = np.array([pos_3d[node][2] for node in G.nodes])

# Generate colors for nodes with gradual color change based on their community
color_gradient = [
    "#FF9999",  # Light red
    "#99CCFF",  # Light blue
    "#FFFF99",  # Light yellow
    "#CCFF99",  # Light green
    "#99FFCC",  # Aquamarine
    "#CC99FF",  # Lavender
    "#FF99CC",  # Pink
    "#FF6666",  # Red
    "#66B2FF",  # Sky blue
]


node_colors = []
node_size = 15  # Larger node size for better visibility

for i, community in enumerate(communities):
    community_color = color_gradient[i % len(color_gradient)]  # Cycle through gradient colors
    for node in community:
        node_colors.append(community_color)  # Assign the community's color to each node

# Create edge traces with color based on edge weights
edge_x = []
edge_y = []
edge_z = []
edge_weights = []

# Normalize edge weights for coloring
max_weight = max(nx.get_edge_attributes(G, "weight").values(), default=1)
min_weight = min(nx.get_edge_attributes(G, "weight").values(), default=0)

for edge in G.edges(data=True):
    x0, y0, z0 = pos_3d[edge[0]]
    x1, y1, z1 = pos_3d[edge[1]]
    edge_x.extend([x0, x1, None])  # None separates each line segment
    edge_y.extend([y0, y1, None])
    edge_z.extend([z0, z1, None])
    # Normalize edge weight for coloring
    weight = edge[2].get("weight", 1)
    normalized_weight = (weight - min_weight) / (max_weight - min_weight)
    edge_weights.append(normalized_weight)

# Map normalized weights to colors
edge_colors = [
    f"rgba({255 - int(w * 255)}, {int(w * 255)}, 150, 0.8)" for w in edge_weights
]

edge_trace = go.Scatter3d(
    x=edge_x,
    y=edge_y,
    z=edge_z,
    mode="lines",
    line=dict(width=2, color=edge_colors),
    hoverinfo="none",
)

# Create node traces with uniform sizes and interactive labels
node_trace = go.Scatter3d(
    x=node_x,
    y=node_y,
    z=node_z,
    mode="markers+text",  # Add both markers and labels
    marker=dict(
        size=node_size,
        color=node_colors,
        opacity=0.8,
        line=dict(width=0.5, color="black"),  # Add border to nodes for better visibility
    ),
    text=[f"{node}" for node in G.nodes],  # Node labels
    textposition="top center",  # Position the labels above the nodes
    hoverinfo="text",  # Show node details on hover
)

# Create the layout
layout = go.Layout(
    title="3D Interactive Louvain Communities with Weighted Edges and Labeled Nodes",
    titlefont=dict(size=16),
    showlegend=False,
    scene=dict(
        xaxis=dict(showbackground=True, backgroundcolor="white", showgrid=False, showticklabels=False),
        yaxis=dict(showbackground=True, backgroundcolor="white", showgrid=False, showticklabels=False),
        zaxis=dict(showbackground=True, backgroundcolor="white", showgrid=False, showticklabels=False),
    ),
    margin=dict(l=0, r=0, b=0, t=40),
)

# Combine traces and plot
fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
fig.show()