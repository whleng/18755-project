import pandas as pd

# Load the job postings dataset
df = pd.read_csv('../mappings/postings.csv')

# Count the frequency of each job title
title_counts = df['title'].value_counts()

# Get the top 20 most popular job titles
top_20_titles = title_counts.head(20)

# Create a new DataFrame with the top 20 titles and their counts
top_20_df = top_20_titles.reset_index()
top_20_df.columns = ['Job Title', 'Frequency']

# Save the result to a new CSV file
top_20_df.to_csv('top_20_popular_job_titles.csv', index=False)

print("Top 20 most popular job titles have been saved to 'top_20_popular_job_titles.csv'")
