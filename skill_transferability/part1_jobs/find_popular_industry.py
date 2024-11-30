import pandas as pd

# Load CSV files
industries = pd.read_csv("../mappings/industries.csv")
postings_parsed = pd.read_csv("../mappings/postings_parsed.csv")
job_industries = pd.read_csv("../mappings/job_industries.csv")
postings = pd.read_csv("../mappings/postings.csv")

# Remove any leading/trailing whitespace around column names
industries.columns = industries.columns.str.strip()
job_industries.columns = job_industries.columns.str.strip()
postings.columns = postings.columns.str.strip()

# Merge postings_parsed with job_industries on job_id
postings_with_industries = pd.merge(postings_parsed, job_industries, on="job_id")
# Count the number of postings per industry_id
industry_counts = postings_with_industries['industry_id'].value_counts().head(10)

# Retrieve the industry names for the top 10 industries
top_industries = industries.set_index('industry_id').loc[industry_counts.index]
top_industries['postings_count'] = industry_counts.values

# Merge to get job titles associated with top industries
postings_with_titles = pd.merge(postings_with_industries, postings[['job_id', 'title']], on='job_id')

# Print top 10 industries with the most job postings
print("Top 10 industries with the most job postings:")
print(top_industries[['industry_name', 'postings_count']])

# For each top industry, get the 10 most common job titles
for industry_id in industry_counts.index:
    industry_name = top_industries.loc[industry_id, 'industry_name']
    # Filter postings for the current industry
    industry_postings = postings_with_titles[postings_with_titles['industry_id'] == industry_id]
    # Find the top 10 most common job titles
    top_titles = industry_postings['title'].value_counts().head(10)
    print(f"\nTop 10 job titles for industry: {industry_name}")
    print(top_titles)
