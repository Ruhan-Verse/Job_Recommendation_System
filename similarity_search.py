import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def extract_state(location):
    try:
        parts = str(location).split(',')
        if len(parts) >= 2:
            return parts[-2].strip()
    except Exception:
        pass
    return None

# Load embeddings
student_embeddings = np.load('student_embeddings.npy')
job_embeddings = np.load('job_embeddings.npy')

# Load student and job data
student_df = pd.read_csv('job_recommendation_dataset.csv')
job_df = pd.read_csv('cleaned_linkedin_jobs.csv')  # <-- Use cleaned file here!

# Compute cosine similarity matrix (students x jobs)
similarity_matrix = cosine_similarity(student_embeddings, job_embeddings)

# Boost similarity for jobs in the same state
boost_value = 0.2
for student_idx, student_row in student_df.iterrows():
    student_state = extract_state(student_row['location'])
    for job_idx, job_row in job_df.iterrows():
        job_state = extract_state(job_row['location'])
        if student_state and job_state and student_state.lower() == job_state.lower():
            similarity_matrix[student_idx, job_idx] += boost_value

# Recommend top N jobs for each student
top_n = 3
top_jobs_indices = np.argsort(similarity_matrix, axis=1)[:, -top_n:][:, ::-1]

for student_idx, job_indices in enumerate(top_jobs_indices):
    student_row = student_df.iloc[student_idx]
    student_id = student_row['user_id']
    student_info = f"Student {student_id} (Age: {student_row['age']}, Location: {student_row['location']})"
    print(f"\n{student_info} top {top_n} jobs:")
    for rank, job_idx in enumerate(job_indices, 1):
        job_row = job_df.iloc[job_idx]
        desc = job_row['job_details'] if pd.notnull(job_row['job_details']) else "No description provided"
        print(f"  {rank}. Title: {job_row['job']}")
        print(f"     Company: {job_row['company_name']}")
        print(f"     Location: {job_row['location']}")
        print(f"     Work Type: {job_row['work_type']}")
        print(f"     Description: {desc}\n")