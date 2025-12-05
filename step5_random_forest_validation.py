import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

INPUT_FILE = "data/clustered_commits.xlsx"
OUTPUT_FILE = "data/cluster_evaluation_metrics.xlsx"

print("Loading clustered dataset...")
df = pd.read_excel(INPUT_FILE)

# Features used for validation
FEATURES = ["FILES CHANGED", "READABILITY", "Entropy", "LOC"]

# Target = unsupervised cluster label (0,1,2)
TARGET = "CLUSTER"

X = df[FEATURES]
y = df[TARGET]

print("Splitting train/test set (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training Random Forest model...")
rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)
rf.fit(X_train, y_train)

print("Predicting quality clusters...")
y_pred = rf.predict(X_test)

# --- Metrics ---
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
mae = metrics.mean_absolute_error(y_test, y_pred)
explained_variance = metrics.explained_variance_score(y_test, y_pred)

# --- Feature Importance ---
importance = rf.feature_importances_

results = pd.DataFrame({
    "Metric": ["RMSE", "MAE", "Explained Variance Score"],
    "Value": [rmse, mae, explained_variance]
})

importance_df = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

# Save both tables to Excel
with pd.ExcelWriter(OUTPUT_FILE) as writer:
    results.to_excel(writer, sheet_name="Metrics", index=False)
    importance_df.to_excel(writer, sheet_name="Feature Importance", index=False)

print("\n----- RANDOM FOREST VALIDATION -----")
print(results)
print("\nFeature Importance:")
print(importance_df)

print(f"\nSaved evaluation output → {OUTPUT_FILE}")
print("Proceed to Step 6: Visualization & Insights.\n")
