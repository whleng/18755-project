import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm

# Read the graph
G = nx.read_gml('../../graphs/skills_graph.gml')

# Perform Louvain clustering
communities = nx.algorithms.community.louvain_communities(G, seed=42)

# Calculate the total number of nodes
total_nodes = len(G.nodes)

# Generate node colors and sizes based on community membership
cmap = cm.get_cmap('tab20', len(communities))
color_map = {}
node_colors = []
node_sizes = []

# Calculate community percentages for legend
community_percentages = []

for i, community in enumerate(communities):
    community_color = cmap(i)  # Assign color from colormap
    community_percent = (len(community) / total_nodes) * 100
    community_percentages.append((i + 1, community_percent))
    
    for node in community:
        color_map[node] = community_color
        # Scale node size by degree (smaller size for better readability)
        node_sizes.append(G.degree[node] * 5)
        node_colors.append(community_color)

# Create spring layout for visualization
pos = nx.spring_layout(G, seed=42)  # Use the entire graph for layout

# Plot the graph
plt.figure(figsize=(10, 10))

# Draw nodes with community colors and scaled sizes
nx.draw_networkx_nodes(
    G, pos,
    node_color=node_colors,
    node_size=node_sizes,
    alpha=0.8
)

# Draw edges with transparency for readability
nx.draw_networkx_edges(
    G, pos,
    alpha=0.2, edge_color="gray"
)

# Add a legend for communities
handles = []
for i, (community_id, percentage) in enumerate(community_percentages):
    handles.append(plt.scatter([], [], color=cmap(i), label=f"Community {community_id}: {percentage:.2f}%"))

plt.legend(
    handles=handles, 
    scatterpoints=1, 
    frameon=True, 
    fontsize=10, 
    loc="lower left", 
    title="Communities by Percentage"
)

# Add title
plt.title("Louvain Communities Visualization (All Nodes)", fontsize=16)

# Save the figure
plt.savefig("figures/louvain_community_visualization_all_nodes.png", dpi=300)
plt.show()