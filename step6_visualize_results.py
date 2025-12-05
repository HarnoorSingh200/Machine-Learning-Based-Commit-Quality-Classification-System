import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Files
CLUSTERED_FILE = "data/clustered_commits.xlsx"
EVAL_FILE = "data/cluster_evaluation_metrics.xlsx"

print("Loading datasets for visualization...")
df = pd.read_excel(CLUSTERED_FILE)
importance_df = pd.read_excel(EVAL_FILE, sheet_name="Feature Importance")

# -------------------- PIE CHART --------------------

print("Plotting cluster distribution pie chart...")
cluster_counts = df["QUALITY_LABEL"].value_counts()

plt.figure(figsize=(6,6))
plt.pie(
    cluster_counts.values,
    labels=cluster_counts.index,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90
)
plt.title("Cluster Distribution (Commit Quality)")
plt.tight_layout()
plt.savefig("plot_cluster_distribution.png")
plt.close()

# -------------------- CORRELATION HEATMAP --------------------

print("Generating correlation heatmap...")
feature_cols = ["FILES CHANGED", "READABILITY", "Entropy", "LOC"]
corr = df[feature_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Commit Metrics")
plt.tight_layout()
plt.savefig("plot_correlation_heatmap.png")
plt.close()

# -------------------- PCA 2D CLUSTER VISUALIZATION --------------------

print("Creating PCA 2D visualization...")
pca = PCA(n_components=2)
pca_data = pca.fit_transform(df[[col+"_SCALED" for col in feature_cols]])

df["PCA1"] = pca_data[:,0]
df["PCA2"] = pca_data[:,1]

plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df,
    x="PCA1",
    y="PCA2",
    hue="QUALITY_LABEL",
    palette="viridis",
    alpha=0.6
)
plt.title("Commit Clusters (PCA 2D Projection)")
plt.tight_layout()
plt.savefig("plot_cluster_pca.png")
plt.close()

# -------------------- FEATURE IMPORTANCE BAR CHART --------------------

print("Plotting feature importance chart...")
plt.figure(figsize=(7,5))
sns.barplot(x="Importance", y="Feature", data=importance_df, palette="crest")
plt.title("Feature Importance from Random Forest")
plt.tight_layout()
plt.savefig("plot_feature_importance.png")
plt.close()

print("\n----- VISUALIZATION COMPLETE -----")
print("Generated files:")
print("  plot_cluster_distribution.png")
print("  plot_correlation_heatmap.png")
print("  plot_cluster_pca.png")
print("  plot_feature_importance.png\n")

print("Proceed to Step 7: Insights & Final README creation.")
