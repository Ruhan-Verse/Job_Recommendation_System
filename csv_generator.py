import pandas as pd
import random

# Load data
personal_data = pd.read_csv("personal_data.csv")
game_mode = pd.read_csv("game_mode.csv")
result = pd.read_csv("result (1).csv")
result_per_q = pd.read_csv("result_per_question (2).csv")
category = pd.read_csv("category.csv")
championship = pd.read_csv("championship.csv")

# Step 1: Merge basic data from personal_data and result
df = personal_data[["user_id", "age", "location", "interests"]].copy()

# Step 2: Qualification from game_mode
df = df.merge(game_mode[["user_id", "user_qualification"]], on="user_id", how="left")
df.rename(columns={"user_qualification": "qualification"}, inplace=True)

# Step 3: avg_score and avg_accuracy from result
result["avg_accuracy"] = result["correct_questions"] / result["total_questions"]
df = df.merge(result[["user_id", "total_score", "avg_accuracy"]], on="user_id", how="left")
df.rename(columns={"total_score": "avg_score"}, inplace=True)

# Step 4: Derive top_category
# First map champ_id → category_id using championship
championship_map = championship[["champ_id", "category_id"]]

# Now join with result_per_q to get user_id and champ_id
user_category = result_per_q.merge(championship_map, on="champ_id", how="left")

# Count most frequent category_id per user
top_cat = user_category.groupby(["user_id", "category_id"]).size().reset_index(name="count")
top_cat = top_cat.sort_values(["user_id", "count"], ascending=[True, False]).drop_duplicates("user_id")

# Map category_id → category_name
top_cat = top_cat.merge(category[["category_id", "category_name"]], on="category_id", how="left")
top_cat = top_cat[["user_id", "category_name"]].rename(columns={"category_name": "top_category"})

# Merge into df
df = df.merge(top_cat, on="user_id", how="left")

# Step 5: Add job_title (empty) and course_id (dummy)
df["job_title"] = ""  # Target column for prediction

# Dummy course_id — assign a random course ID like "C101", "C102", etc.
dummy_course_ids = [f"C{100+i}" for i in range(len(df))]
random.shuffle(dummy_course_ids)
df["course_id"] = dummy_course_ids

# Final column order without skill_domain
final_columns = ["user_id", "age", "location", "interests", "qualification",
                 "avg_score", "avg_accuracy", "top_category", "job_title", "course_id"]
df = df[final_columns]

# Save to CSV
df.to_csv("job_recommendation_dataset.csv", index=False)
print("✅ job_recommendation_dataset.csv created successfully without 'skill_domain' column!")
