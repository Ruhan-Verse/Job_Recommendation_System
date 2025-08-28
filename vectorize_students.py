from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# Load student and cleaned job data
student_df = pd.read_csv('job_recommendation_dataset.csv')
job_df = pd.read_csv('cleaned_linkedin_jobs.csv')

model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_student(row):
    return (
        f"Age: {row['age']}, Location: {row['location']}, Interests: {row['interests']}, "
        f"Qualification: {row['qualification']}, Score: {row['avg_score']}, "
        f"Accuracy: {row['avg_accuracy']}, Top Category: {row['top_category']}, "
        f"Job Title: {row['job_title']}"
    )

def encode_job(row):
    return (
        f"Job: {row['job']}, Location: {row['location']}, Company: {row['company_name']}, "
        f"Work Type: {row['work_type']}, Details: {row['job_details']}"
    )

student_corpus = student_df.apply(encode_student, axis=1).tolist()
job_corpus = job_df.apply(encode_job, axis=1).tolist()

student_embeddings = model.encode(student_corpus, show_progress_bar=True)
job_embeddings = model.encode(job_corpus, show_progress_bar=True)

np.save('student_embeddings.npy', student_embeddings)
np.save('job_embeddings.npy', job_embeddings)
print("✅ Embeddings saved as student_embeddings.npy and job_embeddings.npy")