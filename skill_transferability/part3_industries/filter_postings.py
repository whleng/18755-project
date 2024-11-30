import pandas as pd
import re

# Load the CSV files
industries_df = pd.read_csv('../mappings/industries.csv')  # Industry_id, industry_name
postings_parsed_df = pd.read_csv('../mappings/postings_parsed.csv')  # job_id, company_name, description, skills_desc, zip_code, skills
job_industries_df = pd.read_csv('../mappings/job_industries.csv')  # job_id, industry_id
postings_df = pd.read_csv('../mappings/postings.csv')  # job_id, company_name, title, description, max_salary, pay_period, location, company_id, views, med_salary, min_salary, formatted_work_type, applies, original_listed_time, remote_allowed, job_posting_url, application_url, application_type, expiry, closed_time, formatted_experience_level, skills_desc, listed_time, posting_domain, sponsored, work_type, currency, compensation_type, normalized_salary, zip_code, fips

# Step 1: Merge job_industries with postings_parsed to get job_id and industry_id
job_industries_merged = job_industries_df.merge(postings_parsed_df[['job_id', 'skills_desc', 'skills']], on='job_id', how='left')

# Step 2: Merge job_industries_merged with postings to get job title
job_industries_with_titles = job_industries_merged.merge(postings_df[['job_id', 'title']], on='job_id', how='left')

# Step 3: Define the pattern to match variations of "Software Engineer"
# The regex will account for variations like "Software Engineer", "software engineer", "Sr. Software Engineer", etc.
pattern = r'.*software\s*engineer.*'

# Step 4: Filter jobs that have "software engineer" in the title (case-insensitive)
filtered_jobs = job_industries_with_titles[job_industries_with_titles['title'].str.contains(pattern, case=False, na=False)]

# Step 5: Merge with industries_df to get the industry name from industry_id
final_jobs = filtered_jobs.merge(industries_df[['industry_id', 'industry_name']], left_on='industry_id', right_on='industry_id', how='left')

# Step 6: Select the required columns: industry, job_id, title, and skills
final_jobs_filtered = final_jobs[['industry_name', 'job_id', 'title', 'skills']]

# Step 7: Save the result to a new CSV file
final_jobs_filtered.to_csv('software_engineer_jobs.csv', index=False)

# Display the result
print(final_jobs_filtered.head())
