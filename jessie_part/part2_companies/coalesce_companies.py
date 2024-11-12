import pandas as pd
import re
from collections import Counter

# Load the previously outputted file
coalesced_skills = pd.read_csv('software_engineering_skills.csv')

# Function to clean and normalize skills
def clean_and_normalize_skills(skills):
    if isinstance(skills, str):
        # Remove any unwanted characters like brackets and extra spaces
        skills = re.sub(r'[^\w\s,]', '', skills)  # Remove non-alphanumeric characters except space and comma
        skill_list = [skill.strip().lower() for skill in skills.split(',')]
        return skill_list
    return []

# Clean and normalize the skills column
coalesced_skills['top_skills'] = coalesced_skills['top_skills'].apply(clean_and_normalize_skills)

# Coalesce skills by company (combine lists of skills for the same company)
coalesced_by_company = coalesced_skills.groupby('company_name')['top_skills'].apply(lambda x: sum(x, []))  # Combine lists of skills
coalesced_by_company = coalesced_by_company.reset_index()

# Function to get the top 10 most popular skills
def top_10_skills(skills_list):
    skill_counter = Counter(skills_list)
    # Get the 10 most common skills, sorted by frequency
    top_skills = [skill for skill, _ in skill_counter.most_common(10)]
    return ', '.join(top_skills)

# Apply the top_10_skills function to get the top 10 skills for each company
coalesced_by_company['top_skills'] = coalesced_by_company['top_skills'].apply(top_10_skills)

# Remove any companies that have no skills
coalesced_by_company = coalesced_by_company[coalesced_by_company['top_skills'].str.strip() != '']

# Save the result to a new CSV file with company_name and top_skills
coalesced_by_company.to_csv('coalesced_skills_by_company.csv', index=False)

# Show the result for a quick check
print(coalesced_by_company.head(10))
