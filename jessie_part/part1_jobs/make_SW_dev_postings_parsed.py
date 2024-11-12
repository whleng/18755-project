import pandas as pd

# Load CSV files
industries = pd.read_csv("../mappings/industries.csv")
postings_parsed = pd.read_csv("../mappings/postings_parsed.csv")
job_industries = pd.read_csv("../mappings/job_industries.csv")

# Remove any leading/trailing whitespace around column names
industries.columns = industries.columns.str.strip()
postings_parsed.columns = postings_parsed.columns.str.strip()
job_industries.columns = job_industries.columns.str.strip()

# Find the Industry_id for "Software Development"
software_dev_industry = industries[industries['industry_name'] == "Software Development"]
if software_dev_industry.empty:
    print("Error: 'Software Development' industry not found in Industries.csv.")
else:
    software_dev_industry_id = software_dev_industry['industry_id'].values[0]

    # Merge postings_parsed with job_industries on job_id
    postings_with_industries = pd.merge(postings_parsed, job_industries, on="job_id")

    # Filter for postings in the "Software Development" industry
    software_dev_postings = postings_with_industries[postings_with_industries['industry_id'] == software_dev_industry_id]

    # Save the filtered DataFrame to a new CSV file
    software_dev_postings.to_csv("Postings_Parsed_Software_Development.csv", index=False)

    print("Filtered CSV created: 'Postings_Parsed_Software_Development.csv'")
