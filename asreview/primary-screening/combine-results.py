import os
import pandas as pd

base_dir = os.getcwd() + "/results"

# Paths
eoan_path = "eoan_round_1.csv"
openai2_path = "openai_round_2.csv"
openai3_path = "openai_round_3.csv"

# Read CSVs
eoan = pd.read_csv(base_dir + "/" + eoan_path)
openai2 = pd.read_csv(base_dir + "/" + openai2_path)
openai3 = pd.read_csv(base_dir + "/" + openai3_path)

openai2 = openai2[['DOI', 'openai_suggestion']].rename(columns={'openai_suggestion': 'openai_suggestion_2'})
openai3 = openai3[['DOI', 'openai_suggestion']].rename(columns={'openai_suggestion': 'openai_suggestion_3'})

# Merge openai suggestions into eoan dataframe
df = eoan.merge(openai2, on='DOI', how='left')
df = df.merge(openai3, on='DOI', how='left')

# Export to new CSV
df.to_csv("combined_screening_results.csv", index=False)
print("Combined results saved to combined_screening_results.csv")