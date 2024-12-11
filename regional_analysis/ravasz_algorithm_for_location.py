"""
This file applies the Ravasz algorithm 
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist

# Load the graph
G = nx.read_gml('../graphs/location_graph_latlong.gml')

# Define the similarity metric based on Ravasz's idea:
def calculate_similarity(u, v):
    if G.has_edge(u, v):
        print(G[u][v])
        edge_weight = G[u][v]['weight']
        print(edge_weight)
        if edge_weight < 5:
            return 1
        else:
            return 0
    else:
        return 0

# Create a similarity matrix for hierarchical clustering
nodes = list(G.nodes())
similarity_matrix = np.zeros((len(nodes), len(nodes)))

for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        if i < j:  # Avoid redundant calculations
            print(u, v)
            similarity = calculate_similarity(u, v)
            similarity_matrix[i, j] = similarity
            similarity_matrix[j, i] = similarity  # Symmetric matrix

# Convert similarity to distance (1 - similarity) for clustering
distance_matrix = 1 - similarity_matrix
distance_array = pdist(distance_matrix)

# Form the dendrogram using hierarchical clustering (average linkage)
Z = linkage(distance_array, method='average')

# Plot dendrogram
plt.figure(figsize=(12, 8))
dendrogram(Z, labels=nodes, leaf_rotation=90)
plt.title("Dendrogram of Skill Similarities (Ravasz Approximation)")
plt.xlabel("Skills")
plt.ylabel("Distance (1 - Similarity)")
# plt.savefig("figures/ravasz_dendrogram.jpg")

# Define a parameter to "cut" the dendrogram and form communities
cut_threshold = 1  # Adjust this to control the community granularity
clusters = fcluster(Z, cut_threshold, criterion='distance')

# Print out the communities in the same format
community_dict = {}
for node, cluster_id in zip(nodes, clusters):
    if cluster_id not in community_dict:
        community_dict[cluster_id] = []
    community_dict[cluster_id].append(node)

print("================ Community Analysis ================\n")
for i, (cluster_id, community_nodes) in enumerate(community_dict.items(), 1):
    community_subgraph = G.subgraph(community_nodes)
    print(f"Community {i}: {len(community_nodes)} nodes")
    print(f"Cut threshold: {cut_threshold}")
    
    # Sort nodes by degree and select top 10 by degree within the community
    top_10_nodes = sorted(
        [(node, G.degree[node]) for node in community_nodes],
        key=lambda x: x[1],
        reverse=True
    )[:10]

    print("Top 10 nodes by degree:")
    for node, degree in top_10_nodes:
        state = G.nodes()[node]["state"]
        print(f"Node: {state}, Degree: {degree}")
    print("=========================================\n")