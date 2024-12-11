import pandas as pd
import re
from collections import Counter


import pandas as pd

# Load CSV files
industries = pd.read_csv("../data/mappings/industries.csv")
postings_parsed = pd.read_csv("../data/postings_parsed.csv")
job_industries = pd.read_csv("../data/jobs/job_industries.csv")
raw_postings = pd.read_csv("../data/postings.csv")

# Remove any leading/trailing whitespace around column names
industries.columns = industries.columns.str.strip()
postings_parsed.columns = postings_parsed.columns.str.strip()
job_industries.columns = job_industries.columns.str.strip()

############################################################################################
# Filter jobs within the "Software Development industry"
############################################################################################

# Find the Industry_id for "Software Development"
software_dev_industry = industries[industries['industry_name'] == "Software Development"]
software_dev_industry_id = software_dev_industry['industry_id'].values[0]

# Merge postings_parsed with job_industries on job_id
postings_with_industries = pd.merge(postings_parsed, job_industries, on="job_id")

# Filter for postings in the "Software Development" industry
software_dev_postings = postings_with_industries[postings_with_industries['industry_id'] == software_dev_industry_id]

# Add in the title to postings_parsed
software_dev_postings = pd.merge(software_dev_postings[['job_id', 'skills', 'zip_code']], 
                                    raw_postings[['title', 'job_id']], on="job_id")

software_dev_postings.to_csv('sde_postings.csv', index=False)
print(software_dev_postings.head(5))


############################################################################################
# Filter jobs with "software engineering" or its variation in the title
############################################################################################


# Regex pattern for matching variations of "Software Engineer" with abbreviations and suffixes
software_titles_pattern = re.compile(r'\b(?:software\s*engineer|swe|se|sw\s*engineer|junior\s*software\s*engineer|senior\s*software\s*engineer|software\s*engineer\s*(?:i{0,3}|[ivxlc]{1,3}))\b', re.IGNORECASE)

# Filter for "Software Engineer" or similar titles using regex matching from postings.csv
raw_postings = raw_postings[raw_postings['title'].str.contains(software_titles_pattern)]
raw_postings = raw_postings[['job_id', 'company_name', 'title', 'description']]

# Merge with Postings_parsed.csv to get skills
swe_postings = pd.merge(raw_postings, 
                  postings_parsed[['job_id', 'skills', 'zip_code']], 
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
swe_postings['skills'] = swe_postings['skills'].apply(clean_and_normalize_skills)

swe_postings.to_csv('swe_postings.csv', index=False)
print(swe_postings.head(5))

############################################################################################
# Combine all jobs related to tech into one large dataset
############################################################################################

all_software_postings = pd.concat([software_dev_postings, swe_postings], ignore_index=True)

# Save the result to a new CSV file 
all_software_postings.to_csv('combined_tech_postings.csv', index=False)
