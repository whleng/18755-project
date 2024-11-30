import pandas as pd

# Load the CSV files
industries_df = pd.read_csv('../mappings/industries.csv')  # Industry_id, industry_name
postings_parsed_df = pd.read_csv('../mappings/postings_parsed.csv')  # job_id, company_name, description, skills_desc, zip_code, skills
job_industries_df = pd.read_csv('../mappings/job_industries.csv')  # job_id, industry_id
postings_df = pd.read_csv('../mappings/postings.csv')  # job_id, company_name, title, description, max_salary, pay_period, location, company_id, views, med_salary, min_salary, formatted_work_type, applies, original_listed_time, remote_allowed, job_posting_url, application_url, application_type, expiry, closed_time, formatted_experience_level, skills_desc, listed_time, posting_domain, sponsored, work_type, currency, compensation_type, normalized_salary, zip_code, fips

# Merge Job_industries with Postings_parsed to get job_id and industry_id
job_industries_merged = job_industries_df.merge(postings_parsed_df[['job_id']], on='job_id', how='left')

# Merge with postings_df to get job titles
job_industries_with_titles = job_industries_merged.merge(postings_df[['job_id', 'title']], on='job_id', how='left')

# Count the number of unique industries each job title appears in
title_industry_counts = job_industries_with_titles.groupby('title')['industry_id'].nunique().reset_index(name='industry_count')

# Sort by the number of unique industries each job title appears in and select the top 25 job titles
top_25_titles = title_industry_counts.sort_values(by='industry_count', ascending=False).head(25)

# Display the top 25 job titles with their respective industry counts
print(top_25_titles[['title', 'industry_count']])

# Optionally, save the result to a CSV file
top_25_titles.to_csv('top_25_job_titles_with_industry_counts.csv', index=False)
