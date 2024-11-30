import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Louvain community detection
from igraph import Graph as IGraph
import leidenalg
from infomap import Infomap
from collections import Counter

# Load the dataset with job titles and skills
df = pd.read_csv('top_100_most_popular_jobs.csv')

# Create a graph
G = nx.Graph()

# Add nodes (job titles)
for index, row in df.iterrows():
    title = row['title']
    G.add_node(title)

# Calculate shared skills between job titles and add edges with weights
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i >= j:  # Avoid duplicate pairs (i, j) and (j, i)
            continue
        # Find common skills
        skills1 = set(row1['filtered_skills'].split())
        skills2 = set(row2['filtered_skills'].split())
        common_skills = skills1.intersection(skills2)
        if len(common_skills) > 0:  # Only add an edge if there are common skills
            G.add_edge(row1['title'], row2['title'], weight=len(common_skills))

# Remove disconnected nodes (degree == 0)
nodes_to_remove = [node for node, degree in G.degree() if degree == 0]
G.remove_nodes_from(nodes_to_remove)

G.remove_edges_from(nx.selfloop_edges(G))

##### Run Different Clustering Algorithms #####

# # Relabel nodes to integers for clustering algorithms
# node_mapping = {node: idx for idx, node in enumerate(G.nodes())}
# reverse_mapping = {idx: node for node, idx in node_mapping.items()}
# G_int = nx.relabel_nodes(G, node_mapping)

# # Convert to igraph
# igraph_g = IGraph.TupleList(G_int.edges(), directed=False)

# # --- Leiden ---
# leiden_partition = leidenalg.find_partition(igraph_g, leidenalg.ModularityVertexPartition)
# leiden_communities = {reverse_mapping[node]: i for i, cluster in enumerate(leiden_partition) for node in cluster}

# --- Louvain ---
louvain_partition = community_louvain.best_partition(G)

# # --- Infomap ---
# infomap = Infomap()
# for u, v in G_int.edges():
#     infomap.addLink(u, v)

# infomap.run()
# infomap_partition = {reverse_mapping[node.node_id]: node.module_id for node in infomap.nodes}

# # --- Walktrap ---
# walktrap_partition = igraph_g.community_walktrap().as_clustering()
# walktrap_communities = {reverse_mapping[node]: i for i, cluster in enumerate(walktrap_partition) for node in cluster}

# # --- Label Propagation ---
# label_partition = nx.algorithms.community.label_propagation.label_propagation_communities(G)
# label_communities = {node: i for i, community in enumerate(label_partition) for node in community}

# Intra-community ratio metric
def intra_community_ratio(G, partition):
    score = 0
    for node, community in partition.items():
        neighbors = list(G.neighbors(node))
        same_community = sum(1 for n in neighbors if partition.get(n) == community)
        score += same_community / len(neighbors) if neighbors else 0
    return score / len(partition)  # Average across all nodes

# # Evaluate each algorithm
# algorithms = {
#     "Leiden": leiden_communities,
#     "Louvain": louvain_partition,
#     "Infomap": infomap_partition,
#     "Walktrap": walktrap_communities,
#     "Label Propagation": label_communities
# }

# for name, partition in algorithms.items():
#     score = intra_community_ratio(G, partition)
#     size = Counter(partition.values())
#     print(f"{name}: {score:.4f} | {size}")

# Plot the graph with communities in different colors
plt.figure(figsize=(14, 14))  # Increased figure size

# Get positions for nodes using spring layout (better for readability)
pos = nx.spring_layout(G, k=2, iterations=100)  # Adjusted iterations and spring strength

# Draw the nodes with colors based on community assignment
community_colors = [louvain_partition[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.rainbow, node_size=500)

# Draw the edges with transparency based on the weight of the edge (thicker for more common skills)
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.7, edge_color=weights, edge_cmap=plt.cm.Blues)

# Draw the labels (job titles)
nx.draw_networkx_labels(G, pos, font_size=6, font_weight='bold', font_color='black')

plt.title('Job Titles Network with Louvain Communities (No Disconnected Nodes)')
plt.axis('off')  # Turn off axis
