import pandas as pd

# Load the necessary CSV files
industries = pd.read_csv('../mappings/industries.csv')
postings_parsed = pd.read_csv('../mappings/postings_parsed.csv')
postings = pd.read_csv('../mappings/postings.csv')
job_industries = pd.read_csv('../mappings/job_industries.csv')

# Find the Industry_id for 'Software Development'
software_dev_industry_id = industries[industries['industry_name'] == 'Software Development']['industry_id'].values[0]

# Filter job IDs that are related to 'Software Development' by matching Job_industries
software_dev_job_ids = job_industries[job_industries['industry_id'] == software_dev_industry_id]['job_id']

# Filter the postings_parsed dataframe to get only postings related to 'Software Development'
software_dev_postings = postings_parsed[postings_parsed['job_id'].isin(software_dev_job_ids)]

# Merge the filtered postings_parsed with postings to get the 'title' column
software_dev_postings_with_titles = pd.merge(software_dev_postings, postings[['job_id', 'title']], on='job_id', how='left')

# Get the number of unique job titles
unique_job_titles = software_dev_postings_with_titles['title'].nunique()

print(f"Number of unique job titles in Software Development: {unique_job_titles}")
