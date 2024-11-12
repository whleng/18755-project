import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Louvain community detection

# Read the CSV file with proper handling for quoted text
df = pd.read_csv("well_known_company.csv", quotechar='"', on_bad_lines='skip')

# Create a graph
G = nx.Graph()

# Add nodes (companies)
for index, row in df.iterrows():
    company = row['company_name']
    G.add_node(company)

# Calculate shared skills between job companies and add edges with weights
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i >= j:  # Avoid duplicate pairs (i, j) and (j, i)
            continue
        # Find common skills
        skills1 = set(row1['top_skills'].split())
        skills2 = set(row2['top_skills'].split())
        common_skills = skills1.intersection(skills2)
        if len(common_skills) > 0:  # Only add an edge if there are common skills
            G.add_edge(row1['company_name'], row2['company_name'], weight=len(common_skills))

# Remove disconnected nodes (degree == 0)
nodes_to_remove = [node for node, degree in G.degree() if degree == 0]
G.remove_nodes_from(nodes_to_remove)

G.remove_edges_from(nx.selfloop_edges(G))

# Apply Louvain community detection algorithm
partition = community_louvain.best_partition(G)

# Plot the graph with communities in different colors
plt.figure(figsize=(14, 14))  # Increased figure size

# Get positions for nodes using spring layout (better for readability)
pos = nx.spring_layout(G, k=4, iterations=100)  # Adjusted iterations and spring strength

# Draw the nodes with colors based on community assignment
community_colors = [partition[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.rainbow, node_size=500)

# Draw the edges with transparency based on the weight of the edge (thicker for more common skills)
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.7, edge_color=weights, edge_cmap=plt.cm.Blues)

# Draw the labels (job titles)
nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold', font_color='black')

plt.title('Companies Network with Louvain Communities (No Disconnected Nodes)')
plt.axis('off')  # Turn off axis

# Save the figure as a PDF file
# plt.savefig("companies_network.pdf", format="pdf")

# Optionally, you can save it as PNG or JPEG as well
# plt.savefig("ompanies_network.png", format="png")
# plt.savefig("ompanies_network.jpeg", format="jpeg")

# Close the plot to free up memory
# plt.close()

plt.show()
