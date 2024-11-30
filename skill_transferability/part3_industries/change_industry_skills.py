import pandas as pd
import re

# Load the CSV file
file_path = 'industry_top_skills.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Function to clean and deduplicate skills
def process_unique_skills(skills_str):
    try:
        # Remove irregular characters and extract all skills using regex
        skills = re.findall(r'\b\w+\b', skills_str)
        # Remove duplicates and sort
        unique_skills = sorted(set(skills))
        return ', '.join(unique_skills)
    except TypeError:
        # Handle any malformed strings
        return ''

# Process the 'unique_skills' column
df['unique_skills'] = df['unique_skills'].apply(process_unique_skills)

# Select only the desired columns
result = df[['industry_name', 'unique_skills']]

# Save the cleaned data to a new CSV file
output_path = 'cleaned_file.csv'
result.to_csv(output_path, index=False)

print(f"Cleaned data saved to {output_path}")
