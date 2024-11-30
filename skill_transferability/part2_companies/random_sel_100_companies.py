import pandas as pd

# Load the coalesced skills by company data
coalesced_skills = pd.read_csv('coalesced_skills_by_company.csv')

# Randomly select 100 entries
sampled_data = coalesced_skills.sample(n=100, random_state=42)  # random_state for reproducibility

# Save the sampled data to a new CSV file
sampled_data.to_csv('sampled_skills_100.csv', index=False)

# Show a preview of the selected data
print(sampled_data.head())
