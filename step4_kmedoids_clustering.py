import pandas as pd
from KMedoids import KMedoids   # using custom implementation
import numpy as np

INPUT_FILE = "data/normalized_for_clustering.xlsx"
OUTPUT_FILE = "data/clustered_commits.xlsx"

print("Loading normalized dataset...")
df = pd.read_excel(INPUT_FILE)

# ------------------ SAMPLE DATASET HERE ------------------
# Reduce dataset size for faster clustering (choose your number)
SAMPLE_SIZE = 10000        # limited due to laptop processing capacity

if len(df) > SAMPLE_SIZE:
    print(f"Sampling dataset from {len(df)} rows down to {SAMPLE_SIZE} rows...")
    df = df.sample(SAMPLE_SIZE, random_state=42).reset_index(drop=True)

# ---------------------------------------------------------

# Select SCALED features for clustering
FEATURES_SCALED = [
    "READABILITY_SCALED",
    "Entropy_SCALED",
    "LOC_SCALED",
    "FILES CHANGED_SCALED",
]

print("Preparing clustering input...")
data = df[FEATURES_SCALED].values

# Convert numpy rows to list of tuples (format expected by custom KMedoids)
data_list = [tuple(row) for row in data]

# Run K-Medoids
print("Running K-Medoids clustering with k = 3")
kmedoids = KMedoids(n_cluster=3, max_iter=100, tol=0.001)
kmedoids.fit(data_list)

clusters = kmedoids.clusters
medoids = list(kmedoids.medoids)

print("\nCluster Medoids (row indices):", medoids)
print("Cluster sizes:")
for idx, medoid in enumerate(medoids):
    print(f"  Cluster {idx+1}: {len(clusters[medoid])} commits")

# Assign cluster labels to dataframe
cluster_labels = [-1] * len(df)
for cluster_index, medoid in enumerate(medoids):
    for row_index in clusters[medoid]:
        cluster_labels[row_index] = cluster_index

df["CLUSTER"] = cluster_labels

CLUSTER_MAP = {
    0: "LOW_QUALITY",
    1: "MEDIUM_QUALITY",
    2: "HIGH_QUALITY"
}
df["QUALITY_LABEL"] = df["CLUSTER"].map(CLUSTER_MAP)

df.to_excel(OUTPUT_FILE, index=False)

print("\nCluster labeling complete!")
print(df['QUALITY_LABEL'].value_counts())
print(f"Saved clustered dataset to: {OUTPUT_FILE}")
print("Proceed to Step 5: Random Forest validation.\n")
