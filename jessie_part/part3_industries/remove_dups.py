import pandas as pd

# Load the CSV file generated previously
filtered_jobs_df = pd.read_csv('software_engineer_jobs.csv')

# Step 1: Count the occurrences of each job_id
job_id_counts = filtered_jobs_df['job_id'].value_counts()

# Step 2: Find job_ids that appear more than once
duplicate_job_ids = job_id_counts[job_id_counts > 1].index

# Step 3: Filter out the rows with duplicate job_ids
filtered_jobs_no_duplicates = filtered_jobs_df[~filtered_jobs_df['job_id'].isin(duplicate_job_ids)]

# Step 4: Save the result to a new CSV file without duplicates
filtered_jobs_no_duplicates.to_csv('software_engineer_jobs_no_duplicates.csv', index=False)

# Display the result
print(filtered_jobs_no_duplicates.head())
