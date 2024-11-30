import pandas as pd
import re
from collections import Counter

# Load the datasets
postings = pd.read_csv('../mappings/postings.csv')
postings_parsed = pd.read_csv('../mappings/postings_parsed.csv')

# Regex pattern for matching variations of "Software Engineer" with abbreviations and suffixes
software_titles_pattern = re.compile(r'\b(?:software\s*engineer|swe|se|sw\s*engineer|junior\s*software\s*engineer|senior\s*software\s*engineer|software\s*engineer\s*(?:i{0,3}|[ivxlc]{1,3}))\b', re.IGNORECASE)

# Filter for "Software Engineer" or similar titles using regex matching from postings.csv
software_postings = postings[postings['title'].str.contains(software_titles_pattern)]

# Merge with Postings_parsed.csv to get skills
merged = pd.merge(software_postings[['job_id', 'company_name', 'title']], 
                  postings_parsed[['job_id', 'skills']], 
                  on='job_id', 
                  how='left')

# Function to clean and normalize the skills
def clean_and_normalize_skills(skills):
    if isinstance(skills, str):
        # Remove any unwanted characters like brackets and extra spaces
        skills = re.sub(r'[^\w\s,]', '', skills)  # Remove non-alphanumeric characters except space and comma
        skill_list = [skill.strip().lower() for skill in skills.split(',')]
        return skill_list
    return []

# Clean and normalize the skills column
merged['skills'] = merged['skills'].apply(clean_and_normalize_skills)

# Coalesce skills by company and job title (combine lists of skills)
coalesced = merged.groupby(['company_name', 'title'])['skills'].apply(lambda x: sum(x, []))  # Combine lists of skills
coalesced = coalesced.reset_index()

# Function to get the top 10 most popular skills
def top_10_skills(skills_list):
    skill_counter = Counter(skills_list)
    # Get the 10 most common skills, sorted by frequency
    top_skills = [skill for skill, _ in skill_counter.most_common(10)]
    return ', '.join(top_skills)

# Apply the top_10_skills function to get the top 10 skills for each group
coalesced['top_skills'] = coalesced['skills'].apply(top_10_skills)

# Save the result to a new CSV file with company_name, title, and top_skills
coalesced[['company_name', 'title', 'top_skills']].to_csv('software_engineering_skills.csv', index=False)

# Show the result for a quick check
print(coalesced[['company_name', 'title', 'top_skills']].head(10))
