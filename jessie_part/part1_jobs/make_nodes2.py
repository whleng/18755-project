import pandas as pd

# Load the CSV files
postings_parsed_df = pd.read_csv('Postings_Parsed_Software_Development.csv')
postings_df = pd.read_csv('../mappings/postings.csv')

# Merge the dataframes on 'job_id' to access job titles and skills together
merged_df = pd.merge(postings_parsed_df[['job_id', 'skills']],
                     postings_df[['job_id', 'title']],
                     on='job_id')

# Clean up the 'skills' column by removing brackets and splitting skills into a flat list
def clean_skills(skills):
    if pd.isna(skills):
        return []
    # Remove unwanted characters like brackets and quotes
    skills = skills.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
    return skills.split(', ')

# Apply the cleaning function to the 'skills' column
merged_df['skills'] = merged_df['skills'].apply(clean_skills)

# Group by the 'title' column and coalesce unique skills for each title
grouped_df = merged_df.groupby('title')['skills'].apply(lambda x: sorted(set(skill for sublist in x for skill in sublist))).reset_index()

# Join skills back into a single comma-separated string per title
grouped_df['skills'] = grouped_df['skills'].apply(lambda skills: ', '.join(skills))

# Rename columns for clarity
grouped_df.columns = ['job_title', 'skills']

# Save the result to a new CSV file
grouped_df.to_csv('nodes2.csv', index=False)

print("Job titles with coalesced skills have been saved to 'nodes2.csv'.")
