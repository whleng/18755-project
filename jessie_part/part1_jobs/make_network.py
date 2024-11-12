import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Louvain community detection

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

# Apply Louvain community detection algorithm
partition = community_louvain.best_partition(G)

# Plot the graph with communities in different colors
plt.figure(figsize=(14, 14))  # Increased figure size

# Get positions for nodes using spring layout (better for readability)
pos = nx.spring_layout(G, k=2, iterations=100)  # Adjusted iterations and spring strength

# Draw the nodes with colors based on community assignment
community_colors = [partition[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.Rainbow, node_size=500)

# Draw the edges with transparency based on the weight of the edge (thicker for more common skills)
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.7, edge_color=weights, edge_cmap=plt.cm.Blues)

# Draw the labels (job titles)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='black')

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
