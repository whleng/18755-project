import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Louvain community detection

def create_network_with_highlighted_edges(input_csv, highlight_skill, output_pdf="job_titles_network_with_highlighted_edges.pdf"):
    # Load the dataset with job titles and skills
    df = pd.read_csv(input_csv)

    # Create a graph
    G = nx.Graph()

    # Add nodes (job titles)
    for index, row in df.iterrows():
        title = row['title']
        G.add_node(title)

    # Calculate shared skills between job titles and add edges with weights
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i >= j:  # Avoid duplicate pairs (i, j)
                continue
            # Find common skills
            skills1 = set(row1['filtered_skills'].split())
            skills2 = set(row2['filtered_skills'].split())
            common_skills = skills1.intersection(skills2)
            if len(common_skills) > 0:  # Only add an edge if there are common skills
                G.add_edge(row1['title'], row2['title'], weight=len(common_skills), common_skills=common_skills)

    # Remove disconnected nodes (degree == 0)
    nodes_to_remove = [node for node, degree in G.degree() if degree == 0]
    G.remove_nodes_from(nodes_to_remove)

    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))

    # Apply Louvain community detection algorithm
    partition = community_louvain.best_partition(G, resolution=1.25)

    # Plot the graph with communities in different colors
    plt.figure(figsize=(14, 14))  # Increased figure size

    # Get positions for nodes using spring layout (better for readability)
    pos = nx.spring_layout(G, k=6, iterations=100)  # Adjusted iterations and spring strength

    # Draw the nodes with colors based on community assignment
    community_colors = [partition[node] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=community_colors, cmap=plt.cm.rainbow, node_size=500)

    # Separate edges by color
    edges = G.edges()
    red_edges = [(u, v) for u, v in edges if highlight_skill in G[u][v].get('common_skills', set())]
    gray_edges = [(u, v) for u, v in edges if highlight_skill not in G[u][v].get('common_skills', set())]

    # Draw red edges with higher transparency
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, width=[G[u][v]['weight'] for u, v in red_edges],
                           alpha=0.9, edge_color='red')

    # Draw gray edges with lower transparency
    nx.draw_networkx_edges(G, pos, edgelist=gray_edges, width=[G[u][v]['weight'] for u, v in gray_edges],
                           alpha=0.1, edge_color='gray')

    # Draw the labels (job titles)
    nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold', font_color='black')

    # Title of the plot
    plt.title(f'Job Titles Network with Louvain Communities (Highlighted Skill: {highlight_skill})')

    # Turn off axis
    plt.axis('off')

    # Save the figure as a PDF file
    # plt.savefig(output_pdf, format="pdf")

    # Optionally, you can save it as PNG or JPEG as well
    # plt.savefig("job_titles_network_with_highlighted_edges.png", format="png")
    # plt.savefig("job_titles_network_with_highlighted_edges.jpeg", format="jpeg")

    # Close the plot to free up memory
    # plt.close()
    plt.show()


# Example usage:
create_network_with_highlighted_edges(
    input_csv="top_100_most_popular_jobs.csv",  # Your input CSV file
    highlight_skill="programming",            # Skill you want to highlight in edges
    output_pdf="highlighted_network.pdf"       # Output PDF file (can be PNG/JPEG as well)
)
