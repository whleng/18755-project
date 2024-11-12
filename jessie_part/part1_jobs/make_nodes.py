import pandas as pd
from collections import Counter

# Load the necessary CSV files
postings_parsed_software_dev = pd.read_csv('postings_parsed_software_development.csv')
postings = pd.read_csv('../mappings/postings.csv')

# Merge the two DataFrames to include titles for the Software Development jobs
postings_parsed_software_dev = pd.merge(postings_parsed_software_dev, postings[['job_id', 'title']], on='job_id', how='left')

# Group by 'title', and merge the skills into a single list for each job title
grouped_postings = postings_parsed_software_dev.groupby('title')['skills'].apply(lambda x: ' '.join(x)).reset_index()

# Split the skills into individual skills for each job posting
grouped_postings['skills_list'] = grouped_postings['skills'].apply(lambda x: x.replace('[','').replace(']','').replace("'",'').split(','))

# Flatten the list of all skills to count frequencies
all_skills = [skill.strip() for sublist in grouped_postings['skills_list'] for skill in sublist if skill.strip()]  # Remove extra spaces
skill_counts = Counter(all_skills)

# Get the top 10 most common skills
top_10_skills = [skill for skill, _ in skill_counts.most_common(10)]

# Function to filter skills to only include the top 10 most common, and remove duplicates
def filter_top_10_skills(skills_list):
    # Remove duplicates before filtering and only keep skills that are in the top 10 most common
    filtered_skills = [skill for skill in set(skills_list) if skill.strip() in top_10_skills]
    return filtered_skills

# Apply the filtering to each job's skill list
grouped_postings['filtered_skills'] = grouped_postings['skills_list'].apply(filter_top_10_skills)

# Create a new DataFrame with job_id, title, and filtered skills (top 10 skills)
final_postings = pd.merge(postings_parsed_software_dev[['job_id', 'title']], grouped_postings[['title', 'filtered_skills']], on='title', how='left')

# Clean the filtered_skills column into a single string
final_postings['filtered_skills'] = final_postings['filtered_skills'].apply(lambda x: ' '.join(sorted(set(x))))  # Ensure no duplicates here

# Drop duplicates, as we only want one entry per job_id
final_postings = final_postings.drop_duplicates(subset=['job_id'])

# Save the result to a new CSV file
final_postings[['job_id', 'title', 'filtered_skills']].to_csv('coalesced_software_dev_postings.csv', index=False)

print("New CSV file 'coalesced_software_dev_postings.csv' created with job_id, title, and top 10 filtered skills.")
