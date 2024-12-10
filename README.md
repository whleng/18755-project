# About Project
#TODO
The purpose of the project is bla bla bla

# General Data Cleaning
- Download dataset from https://www.kaggle.com/datasets/arshkon/linkedin-job-postings/data
- Make sure the dataset is in the `data/` folder, named `data/postings.csv`

## Data Processing Scripts
Data processing scripts are located under `general_data_cleaning/`
- `job_scraper.ipynb`: Parses `postings.csv` to include the skills associated with each job posting. Output is `data/postings_parsed.csv` 
- `filter_swe_jobs.py`: Creates a filtered dataset of all the tech jobs, including jobs within the "Software Development" industry and jobs in all industries with titles related to "Software Engineer". 

## Processed Data
- `skills_lowercase.json`: Self-created list of common soft skills and technical skills. Used for `job_scraper.ipynb` to assign skills to each job posting.
- `combined_tech_postings.csv`: Filtered dataset of all the tech jobs ("Software Development" industry **and** job titles with "Software Engineer")
- `sde_postings_with_location.csv`: Filtered dataset of jobs in the "Software Development" industry.
- `swe_postings_with_location.csv`: Filtered dataset of jobs with job title related to "Software Engineer" across all industries. Location data (latitude and longitude is also included)
- `filtered_1000_postings_with_location.csv`: Filtered dataset by selecting top 1000 jobs in each industry from `swe_postings_with_location.csv`


# Complementary Skills

## Data Pre-processing

1. To create the .gml graph and view the basic results, run create_network.ipynb
2. To view the louvain clustering algorithm, enter the `louvain_clustering/` folder and run `louvain_clustering_plots.py`. THe output should be saved to `figures/`
3. To view the ravasz agglomerative clustering algorithm, enter the `agglomerative_clustering/` folder and run `ravasz_algorithm.py`

# Skill Transferability

- to find the code related to this section of the project, refer to the skill_transferability folder
- the different sub parts (jobs, companies, industries) are broken down into sub folders
- under each of the sub folders, there is a script called make_network.py to generate the network and corresponding metrics
- optionally, there is a function called highlight, which takes in an array of skills and highlights the edges containing these skills
- the remaining code is related to data filtering

# Regional Analysis
Supplementary data located under `txt_files/` folder

## Data Pre-processing
- Top 1000

## Clusters
Clusters generated from **Complementary Skills** and **Skills Transferability** sections were visualized.
- `location_clusters.txt`: Clusters generated based on ravasz algorithm using geographical coordinates 
- `skills_to_clusters.txt`: Clusters from Complementary Skills
- `titles_to_clusters.txt`: Clusters from Skills Transferability

## Analysis
- `basic_analysis.ipynb`: Milestone 1 basic analysis of distribution of jobs based on geolocation information.
- `ravasz_algorithm_for_location.py`: Applies the Ravasz algorithm to generate clusters based on the geographical distances between job postings. These clusters are used for visualization in `location_visualization.ipynb`
- `location_visualizations.ipynb`:
