import pandas as pd

# Load the existing coalesced software dev postings CSV
coalesced_postings = pd.read_csv('coalesced_software_dev_postings.csv')

# Function to remove duplicates from the 'filtered_skills' column
def remove_duplicates(skills):
    # Check if the skills value is a string (not NaN or non-string)
    if isinstance(skills, str):
        skills_list = skills.split()  # Split by spaces (skills are separated by spaces in your data)
        unique_skills = sorted(set(skills_list))  # Remove duplicates and sort alphabetically
        return ' '.join(unique_skills)  # Join back into a single string
    else:
        return ''  # Return an empty string for non-string values (NaN)

# Apply the remove_duplicates function to the 'filtered_skills' column
coalesced_postings['filtered_skills'] = coalesced_postings['filtered_skills'].apply(remove_duplicates)

# Drop rows where 'filtered_skills' is empty or NaN
coalesced_postings = coalesced_postings[coalesced_postings['filtered_skills'].notna() & (coalesced_postings['filtered_skills'] != '')]

# Save the cleaned file back to a new CSV (or overwrite if you prefer)
coalesced_postings.to_csv('cleaned_coalesced_software_dev_postings.csv', index=False)

print("Duplicates removed and empty rows with no skills deleted. New file 'cleaned_coalesced_software_dev_postings.csv' has been saved.")
