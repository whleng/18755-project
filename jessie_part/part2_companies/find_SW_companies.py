import pandas as pd

# Load the job postings dataset
df = pd.read_csv('../mappings/postings.csv')

# Normalize the job title column by converting all text to lowercase for case-insensitive matching
df['title_normalized'] = df['title'].str.lower()

# Define a list of keywords that represent "Software Engineer" roles, including variations
software_engineer_keywords = [
    'software engineer', 
    'senior software engineer', 
    'software dev', 
    'software developer', 
    'dev engineer', 
    'software engineer i', 
    'software engineer ii',
    'junior software engineer', 
    'sr software engineer', 
    'sr. software engineer',
]

# Create a filter that checks if the title contains any of the keywords
software_engineer_filter = df['title_normalized'].apply(lambda x: any(keyword in x for keyword in software_engineer_keywords))

# Filter the DataFrame to only include job postings for "Software Engineer" (or similar) roles
software_engineer_postings = df[software_engineer_filter]

# Count the number of unique companies with postings for "Software Engineer" roles
unique_companies = software_engineer_postings['company_name'].nunique()

print(f'Number of unique companies with at least one "Software Engineer" job posting: {unique_companies}')
