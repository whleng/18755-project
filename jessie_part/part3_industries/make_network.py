import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Louvain community detection
import numpy as np
import random
import re

random.seed(18755)
np.random.seed(18755)

# Read the CSV file with proper handling for quoted text
df = pd.read_csv("nodes.csv", quotechar='"', on_bad_lines='skip')

# Create a graph
G = nx.Graph()

# Add nodes (job titles)
for index, row in df.iterrows():
    title = row['industry_name']
    G.add_node(title)

# Calculate shared skills between job titles and add edges with weights
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i >= j:  # Avoid duplicate pairs (i, j)
            continue
        # Find common skills
        skills1 = set(re.split(r',\s*', row1['top_10_skills']))
        skills2 = set(re.split(r',\s*', row2['top_10_skills']))
        common_skills = skills1.intersection(skills2)
        if len(common_skills) > 0:  # Only add an edge if there are common skills
            G.add_edge(row1['industry_name'], row2['industry_name'], weight=len(common_skills), common_skills=common_skills)

# Remove disconnected nodes (degree == 0)
nodes_to_remove = [node for node, degree in G.degree() if degree == 0]
G.remove_nodes_from(nodes_to_remove)

G.remove_edges_from(nx.selfloop_edges(G))

# Apply Louvain community detection algorithm
partition = community_louvain.best_partition(G, weight="weight", resolution=1.1)

def cluster_connection_strength(G, cluster_nodes):
    """
    Measures how strong or weak the connections are within a cluster.
    The cluster is passed as an array of nodes. The function computes 
    the average edge weight and the variance of edge weights within the cluster.
    
    :param G: The graph (NetworkX graph object)
    :param cluster_nodes: A list of nodes in the cluster.
    :return: A tuple (average_edge_weight, edge_weight_variance)
    """
    total_weight = 0  # To accumulate the total weight of edges within the cluster
    num_edges = 0  # Count the number of edges
    edge_weights = []  # Store all the edge weights to calculate variance
    
    # Iterate over all pairs of nodes in the cluster
    for i, node_u in enumerate(cluster_nodes):
        for node_v in cluster_nodes[i+1:]:  # Ensure no duplicate pairs (i, j) and (j, i)
            if G.has_edge(node_u, node_v):  # Check if there is an edge
                edge_weight = G[node_u][node_v].get('weight', 1)  # Default weight 1 if no weight exists
                total_weight += edge_weight
                edge_weights.append(edge_weight)
                num_edges += 1
    
    # Calculate the average edge weight
    avg_edge_weight = total_weight / num_edges if num_edges > 0 else 0
    
    # Calculate the variance of the edge weights to assess consistency
    if num_edges > 1:
        edge_weight_variance = sum((w - avg_edge_weight) ** 2 for w in edge_weights) / num_edges
    else:
        edge_weight_variance = 0  # No variance if there is only one edge
    
    return edge_weight_variance

def cluster_betweenness_centrality(G, cluster_nodes):
    """
    Calculates the betweenness centrality of a cluster by averaging the betweenness centrality of all nodes.
    
    :param G: The graph (NetworkX graph object)
    :param cluster_nodes: List of nodes in the cluster
    :return: Betweenness centrality score for the cluster
    """
    # Compute betweenness centrality for all nodes in the graph
    betweenness_scores = nx.betweenness_centrality(G)
    
    # Filter the betweenness scores to only include the cluster nodes
    cluster_betweenness_scores = [betweenness_scores[node] for node in cluster_nodes if node in betweenness_scores]
    
    # If the cluster has no nodes, return 0 (or handle as needed)
    if not cluster_betweenness_scores:
        return 0
    
    # Return the average betweenness centrality of the cluster
    return sum(cluster_betweenness_scores) / len(cluster_betweenness_scores)

def calculate_cluster_density(G, cluster):
    # Get the nodes in the cluster
    nodes_in_cluster = list(cluster)
    
    # Get the subgraph of the cluster
    subgraph = G.subgraph(nodes_in_cluster)
    
    # Calculate the number of actual edges in the cluster
    actual_edges = subgraph.number_of_edges()
    
    # Calculate the possible number of edges in the cluster (complete graph)
    n = len(nodes_in_cluster)
    possible_edges = n * (n - 1) / 2
    
    # Calculate density
    density = actual_edges / possible_edges if possible_edges > 0 else 0
    return density

def calculate_avg_weight(G, cluster):
    # Get the list of nodes in the cluster
    nodes_in_cluster = list(cluster)
    
    # Get the subgraph of the cluster
    subgraph = G.subgraph(nodes_in_cluster)
    
    # Calculate the sum of the weights of actual edges in the cluster
    total_weight = sum(weight for u, v, weight in subgraph.edges(data='weight', default=0))
    
    # Calculate the total number of edges in the cluster (for average calculation)
    num_edges = len(subgraph.edges())
    
    # Calculate average edge weight
    average_weight = total_weight / num_edges if num_edges > 0 else 0
    return average_weight

def print_communities(partition):
    """
    Prints the nodes in each community from a partition.

    :param partition: A dictionary mapping nodes to community IDs,
                      or a list of sets where each set represents a community.
    """
    communities = {}
    for node, community in partition.items():
        if community not in communities:
            communities[community] = []
        communities[community].append(node)

    # Print communities
    for community_id, nodes in communities.items():
        density = calculate_cluster_density(G, nodes)
        avg_weight = calculate_avg_weight(G, nodes)
        strength = cluster_connection_strength(G, nodes)
        btwn_cent = cluster_betweenness_centrality(G, nodes)
        print(f"Community {community_id}: density {density} avg_weight {avg_weight} weight_var {strength} btwn_cent{btwn_cent} \n{nodes}")

def get_degree_info():
    # Calculate the degree distribution
    degree_sequence = [d for n, d in G.degree()]

    # Plot the degree distribution
    plt.figure(figsize=(8, 6))
    plt.hist(degree_sequence, bins=30, color='skyblue', edgecolor='black')
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Calculate the average degree
    average_degree = sum(degree_sequence) / len(degree_sequence)
    print(f"Average degree: {average_degree:.2f}")

    # Find the top 10 nodes with the highest degree
    top_20_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:20]

    # Print the top 10 nodes and their degrees
    print("\nTop 10 nodes with the highest degree:")
    for node, degree in top_20_nodes:
        print(f"Node: {node}, Degree: {degree}")

def find_avg_similarity():
    # Set the weight for missing edges (non-existing edges) as 0
    # First, we need to calculate the total number of possible edges
    n = len(G.nodes)
    total_possible_edges = n * (n - 1) / 2

    # Calculate the sum of weights of the existing edges
    total_weight = sum(weight for u, v, weight in G.edges(data='weight', default=0))

    # Calculate the average edge weight, including non-connected nodes with weight 0
    average_edge_weight = total_weight / total_possible_edges if total_possible_edges > 0 else 0

    # Print the average edge weight
    print(f"Average edge weight (including disconnected edges): {average_edge_weight:.4f}")

print("\nLouvain Communities:")
print_communities(partition)

find_avg_similarity()

# this is not super useful since it just counts all the nodes with the most popular skill
# get_degree_info()

# Plot the graph with communities in different colors
plt.figure(figsize=(14, 14))  # Increased figure size

# Get positions for nodes using spring layout (better for readability)
pos = nx.spring_layout(G, k=6, iterations=100)  # Adjusted iterations and spring strength

# Draw the nodes with colors based on community assignment
community_colors = [partition[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.rainbow, node_size=500)

# Draw the edges with transparency based on the weight of the edge (thicker for more common skills)
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.7, edge_color=weights, edge_cmap=plt.cm.Blues)

# Draw the labels (job titles)
nx.draw_networkx_labels(G, pos, font_size=6, font_weight='bold', font_color='black')

plt.title('Job Titles Network with Louvain Communities (No Disconnected Nodes)')
plt.axis('off')  # Turn off axis

# Save the figure as a PDF file
# plt.savefig("job_titles_network.pdf", format="pdf")

# Optionally, you can save it as PNG or JPEG as well
# plt.savefig("job_titles_network.png", format="png")
# plt.savefig("job_titles_network.jpeg", format="jpeg")

# Close the plot to free up memory
# plt.close()

plt.show()

def highlight(highlight_skill):
    plt.figure(figsize=(14, 14))  # Increased figure size
    # Get positions for nodes using spring layout (better for readability)
    pos = nx.spring_layout(G, k=6, iterations=100)  # Adjusted iterations and spring strength

    # Draw the nodes with colors based on community assignment
    community_colors = [partition[node] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.rainbow, node_size=500)

    # Separate edges by color
    edges = G.edges()
    red_edges = [(u, v) for u, v in edges if any(skill in G[u][v].get('common_skills', set()) for skill in highlight_skill)]

    # Draw gray edges with lower transparency
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.7, edge_color=weights, edge_cmap=plt.cm.Blues)
    # Draw red edges with higher transparency
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, width=[G[u][v]['weight'] for u, v in red_edges],
                           alpha=0.5, edge_color='yellow')

    # Draw the labels (job titles)
    nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold', font_color='black')

    # Title of the plot
    plt.title(f'Job Titles Network with Louvain Communities (Highlighted Skill: {highlight_skill})')

    # Turn off axis
    plt.axis('off')

    plt.show()

highlight(["hardware"])