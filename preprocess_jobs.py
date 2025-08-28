import pandas as pd

def clean_location(loc):
    # Remove extra spaces, standardize commas, and handle nulls
    if pd.isnull(loc):
        return "Unknown"
    return ','.join([part.strip().title() for part in str(loc).split(',') if part.strip()])

def is_generic_description(desc):
    # Checks for very short or generic descriptions
    if pd.isnull(desc):
        return True
    desc = str(desc).strip().lower()
    return len(desc) < 15 or desc in ["nan", "not available", "no description", ""]

# Load your job data
job_df = pd.read_csv('linkdin_Job_data.csv')

# Remove duplicates based on job title, company name, and location
job_df = job_df.drop_duplicates(subset=['job', 'company_name', 'location'])

# Remove rows with missing job titles or company names
job_df = job_df.dropna(subset=['job', 'company_name'])

# Standardize location formatting
job_df['location'] = job_df['location'].apply(clean_location)

# Fill missing job descriptions with a placeholder
job_df['job_details'] = job_df['job_details'].fillna("Description not provided.")

# Remove jobs with generic or too-short descriptions
job_df = job_df[~job_df['job_details'].apply(is_generic_description)]

# Optionally, reset index
job_df = job_df.reset_index(drop=True)

# Save to a new file
job_df.to_csv('cleaned_linkedin_jobs.csv', index=False)
print("✅ Advanced cleaned job data saved as cleaned_linkedin_jobs.csv")