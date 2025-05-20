import pandas as pd

# File paths
file1 = "ZA_Pipeline 22_04_2025.xlsx"
file2 = "Pipeline View dateverse.xlsx"


df1 = pd.read_excel(file1, engine="openpyxl")
df2 = pd.read_excel(file2, engine="openpyxl")


ids_file1 = df1["OpportunityID"].dropna().astype(str)
ids_file2 = df2["OpportunityID"].dropna().astype(str)


missing_ids = ids_file1[~ids_file1.isin(ids_file2)]


print("Missing IDs from file2:")
print(missing_ids)

missing_ids.to_excel("missing_ids.xlsx", index=False)
