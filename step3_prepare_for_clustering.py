import pandas as pd
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "data/cleaned_commits.xlsx"
OUTPUT_FILE = "data/normalized_for_clustering.xlsx"

print("Loading cleaned commit dataset...")
df = pd.read_excel(INPUT_FILE)

# Select the numeric features for clustering
FEATURES = ["READABILITY", "Entropy", "LOC", "FILES CHANGED"]

print("Selecting clustering features:", FEATURES)
X = df[FEATURES].copy()

# Normalize features using StandardScaler
print("Normalizing features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaled features and original dataframe merged
for i, col in enumerate(FEATURES):
    df[f"{col}_SCALED"] = X_scaled[:, i]

# Save output file for clustering use
df.to_excel(OUTPUT_FILE, index=False)

print("\n----- SUMMARY -----")
print(f"Rows processed: {len(df)}")
print("Feature value ranges after scaling:")
for col in FEATURES:
    print(f"  {col}_SCALED → min: {df[col + '_SCALED'].min():.3f}, max: {df[col + '_SCALED'].max():.3f}")

print(f"\nNormalized file successfully saved as: {OUTPUT_FILE}")
print("Ready for Step 4: Custom K-Medoids clustering.\n")
