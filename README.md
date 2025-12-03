# Machine Learning-Based GitHub Commit Quality Classification System

A machine learning system designed to automatically evaluate and classify the quality of GitHub commits based on commit-level metadata and code-quality metrics extracted at scale. The goal is to help developers and teams prioritize meaningful commits and improve code review efficiency using automated quality insights.


## 🔑 Key Contributions
1. Collected and processed a large dataset of **300,000+ GitHub commits** using GitHub API, extracting metadata & code-quality indicators including **entropy, readability, files changed, and lines of code (LOC)**.
2. Implemented an **unsupervised clustering pipeline using K-Medoids** to group commits into **quality-based categories: Low, Medium, High**.
3. Used **Random Forest regression** to validate and benchmark clustering performance using **RMSE, Explained Variance Score, and MAE**.
4. Conducted **feature-importance analysis**, identifying that **readability and entropy strongly correlate with high-quality commits**, while **file count shows weak relevance**.
5. Visualized **cluster patterns, correlations, and model statistics** to generate insight-driven recommendations for commit quality improvement.

---

## 📊 Outcome / Impact
1. Successfully classified commit quality into 3 categories, reducing noise and helping prioritize high-value code changes.
2. Demonstrated that **unsupervised machine learning can meaningfully evaluate commit quality**, with improved error metrics for higher-quality clusters.
3. Potential applications include:
   - Automated code review prioritization
   - Stand-up productivity analytics
   - Developer performance dashboards
   - CI/CD commit-scoring integration

---

## 🛠 Tech Stack
**Python**, Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn
