import pandas as pd
import math
import string
from readability import Readability

INPUT_FILE = 'data/dataset.xlsx'
OUTPUT_FILE = 'data/cleaned_commits.xlsx'

print("Loading dataset...")
df = pd.read_excel(INPUT_FILE)

# DATA CLEANING

# Remove rows with missing commit messages
df.dropna(subset=["COMMIT MESSAGE"], inplace=True)

# Remove commit messages that are too short (noise)
df = df[df["COMMIT MESSAGE"].astype(str).str.len() > 3]

# Normalize whitespace & remove non-printable characters
df["COMMIT MESSAGE"] = df["COMMIT MESSAGE"].astype(str).apply(
    lambda x: ''.join(c for c in x if c in string.printable).strip()
)

# Convert numeric columns to integers
for col in ["INSERTIONS", "DELETIONS", "FILES CHANGED"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Remove extreme outliers (optional but recommended)
df = df[(df["INSERTIONS"] < 50000) & (df["DELETIONS"] < 50000)]

print(f"Remaining rows after cleaning: {len(df)}")


# FEATURE ENGINEERING

# Shannon Entropy
def shannon_entropy(text):
    if not text or not isinstance(text, str):
        return 0.0

    text = ''.join(c for c in text if c in string.printable)
    if len(text) == 0:
        return 0.0

    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    entropy = 0.0
    length = len(text)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)

    return round(entropy, 5)


# Readability Score (Flesch–Kincaid)
def get_readability_score(text):
    if not isinstance(text, str) or len(text.split()) < 3:
        return 0.0
    try:
        r = Readability(text)
        fk = r.flesch_kincaid()
        return round(fk.score, 3) if hasattr(fk, "score") else 0.0
    except:
        return 0.0


print("Calculating entropy...")
df["Entropy"] = df["COMMIT MESSAGE"].apply(shannon_entropy)

print("Calculating readability...")
df["READABILITY"] = df["COMMIT MESSAGE"].apply(get_readability_score)

# Add LOC (Lines of Code Changed)
df["LOC"] = df["INSERTIONS"] + df["DELETIONS"]

# KEEP ONLY THE DESIRED COLUMNS (in your preferred order)
final_columns = [
    "READABILITY",
    "FILES CHANGED",
    "LOC",
    "Entropy"
]

df = df[final_columns]

print(f"Saving final cleaned file → {OUTPUT_FILE}")
df.to_excel(OUTPUT_FILE, index=False)

print("----- SUMMARY -----")
print(f"Entropy range: {df['Entropy'].min()} – {df['Entropy'].max()}")
print(f"Readability range: {df['READABILITY'].min()} – {df['READABILITY'].max()}")
print(f"LOC avg: {df['LOC'].mean():.2f}")

print("Step completed successfully.")
