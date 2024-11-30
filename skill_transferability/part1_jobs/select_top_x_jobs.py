import pandas as pd

# Load the necessary CSV files
cleaned_postings = pd.read_csv('cleaned_coalesced_software_dev_postings.csv')
# postings = pd.read_csv('../../../mappings/postings.csv')

# Merge the dataframes on 'job_id' to get titles and skills in one dataframe
# merged_postings = pd.merge(cleaned_postings[['job_id', 'filtered_skills']], 
#                            postings[['job_id', 'title']], on='job_id', how='left')

# Count the number of occurrences of each job title
job_counts = cleaned_postings['title'].value_counts()

# Get the top 100 job titles
top_100_jobs = job_counts.head(200).index

# Filter the merged dataframe to keep only the top 100 job titles
top_100_postings = cleaned_postings[cleaned_postings['title'].isin(top_100_jobs)]

# For each job title, coalesce the skills (merge skills and remove duplicates)
top_100_postings_grouped = top_100_postings.groupby('title').agg({
    'filtered_skills': lambda x: ' '.join(set(' '.join(x).split()))  # Merge skills and remove duplicates
}).reset_index()

# Save the result to a new CSV file
top_100_postings_grouped.to_csv('top_100_most_popular_jobs.csv', index=False)

print("Top 100 most popular jobs have been saved to 'top_100_most_popular_jobs.csv'.")
