# Complementary Skills

## Data Pre-processing

1. Make sure the dataset is in the data/ folder, named "data/postings.csv"
2. Run the file job_scraper.ipynb
3. To create the .gml graph and view the basic results, run create_network.ipynb
4. To view the louvain clustering algorithm, enter the louvain_clustering/ folder and run louvain_clustering_plots.py. THe output should be saved to figures/
5. To view the ravasz agglomerative clustering algorithm, enter the agglomerative_clustering/ folder and run ravasz_algorithm.py

# Skill Transferability

- to find the code related to this section of the project, refer to the skill_transferability folder
- the different sub parts (jobs, companies, industries) are broken down into sub folders
- under each of the sub folders, there is a script called make_network.py to generate the network and corresponding metrics
- optionally, there is a function called highlight, which takes in an array of skills and highlights the edges containing these skills
- the remaining code is related to data filtering
