import pandas as pd

# Load the CSV file
df = pd.read_csv('updated_industries_top_10_skills.csv')

# Function to remove duplicates in the specified column
def remove_duplicates_in_column(column_name):
    for idx, value in df[column_name].items():
        # Remove the single quotes and split by ', ' to get the individual skills
        value = value.replace("'", "")  # Remove single quotes
        skills_list = value.split(', ')  # Split the string by commas
        unique_skills = ', '.join(sorted(set(skills_list)))  # Remove duplicates and join back
        df.at[idx, column_name] = unique_skills  # Update the value in the DataFrame

# Specify the column where you want to remove duplicates (e.g., 'skills')
remove_duplicates_in_column('top_skills')

# Save the updated DataFrame to a new CSV file
df.to_csv('nodes.csv', index=False)

# Print the first few rows to check the result
print(df.head())
