import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm

# Read the graph
G = nx.read_gml('../../graphs/skills_graph.gml')

# Create a copy of the graph for plotting without self-loops
G_no_self_loops = G.copy()
G_no_self_loops.remove_edges_from(nx.selfloop_edges(G))

# Perform Louvain clustering on the original graph (with self-loops)
resolution = 1.0
communities = nx.algorithms.community.louvain_communities(G, resolution=resolution, seed=42)

# Calculate the total number of nodes
total_nodes = len(G.nodes)

# Generate node colors and sizes based on community membership
cmap = [
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

color_map = {}
node_colors = []
node_sizes = []

# Calculate community percentages for legend
community_percentages = []

for i, community in enumerate(communities):
    community_color = cmap[i]  # Assign color from colormap
    community_percent = (len(community) / total_nodes) * 100
    community_percentages.append((i + 1, community_percent))
    
    for node in community:
        color_map[node] = community_color
        # Scale node size by degree (smaller size for better readability)
        node_sizes.append(G.degree[node] * 5)  # Use original graph for size
        node_colors.append(community_color)

    # Print top 10 nodes in the current community by degree
    top_nodes = sorted(community, key=lambda n: G.degree[n], reverse=True)[:10]
    print(f"\nTop 10 nodes in Community {i + 1}:")
    for rank, node in enumerate(top_nodes, 1):
        print(f"{rank}. Node: {node}, Degree: {G.degree[node]}")

# Create spring layout for visualization
pos = nx.spring_layout(G_no_self_loops, seed=42)  # Use the graph without self-loops for layout

# Plot the graph
plt.figure(figsize=(10, 10))

# Draw nodes with community colors and scaled sizes
nx.draw_networkx_nodes(
    G_no_self_loops, pos,
    node_color=node_colors,
    node_size=node_sizes,
    alpha=0.8
)

# Draw edges with transparency for readability
nx.draw_networkx_edges(
    G_no_self_loops, pos,
    alpha=0.2, edge_color="gray"
)

# Add a legend for communities
handles = []
labels = ["Leadership and Soft Skills", "Automation and System Programming", "Software Development and Engineering", "Cybersecurity", "Cutting-Edge Technology"]
for i, (community_id, percentage) in enumerate(community_percentages):
    handles.append(plt.scatter([], [], color=cmap[i], label=f"{labels[i]}: {percentage:.2f}%"))

plt.legend(
    handles=handles, 
    scatterpoints=1, 
    frameon=True, 
    fontsize=10, 
    loc="lower left", 
    title="Communities by Percentage"
)

# Add title
plt.title("Louvain Communities Visualization", fontsize=16)

# Save the figure
plt.savefig("figures/louvain_community_visualization_no_self_loops.png", dpi=300)
plt.show()