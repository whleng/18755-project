import pandas as pd
from collections import Counter

# Load the CSV data
df = pd.read_csv('industry_top_skills.csv')

# Function to process skills for each industry
def process_industry_skills(group):
    combined_skills = []
    
    # Iterate over each row in the group (for each industry)
    for _, row in group.iterrows():
        # Check if 'skills' column is not NaN and is a string
        if isinstance(row['skills'], str):
            # Remove the double quotes if they exist, then split by commas
            skill_list = [skill.strip() for skill in row['skills'].replace('"', '').split(',')]
            combined_skills.extend(skill_list)
    
    # # Count the frequency of each skill using Counter
    # skill_counts = Counter(combined_skills)
    
    # # Get the top 10 most common skills, based on their count
    # top_10_skills = [skill for skill, count in skill_counts.most_common(10)]
    
    # # Combine the top 10 skills into a string and return the processed result
    # return pd.Series({
    #     'top_10_skills': ', '.join(top_10_skills)  # Top 10 skills combined into a single string
    # })
    return combined_skills

# Group by industry_name and apply the process_industry_skills function
df_grouped = df.groupby('industry_name').apply(process_industry_skills)

# Reset the index to turn the 'industry_name' into a column again
df_grouped = df_grouped.reset_index()

# Save the updated DataFrame to a new CSV
df_grouped.to_csv('updated_industries_top_10_skills.csv', index=False)

# Print the first few rows to check the result
print(df_grouped.head())
