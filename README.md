Modeling Fantasy Football Player Performance With An Emphasis on Rookie Players
=========================================================
by Kush Lalwani and Trevor Bunch

**Requirements**
------------
- Run on a Windows Machine
- Run on Python version 3.13.5, found here: [https://www.python.org/downloads/release/python-3135/] under Files -> Windows -> "Download Python install manager"
- Required Packages: pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn

**Instructions**
------------
1. Install all required packages and correct version of Python, set your environemnt to Python 3.13.5 when running the Jupyter Notebooks.
2. (Optional) Rerun the Jupyter Notebooks to create the datasets
    - Run both `clean_rookies.ipynb` and `cleaning_data_NFL.ipynb`. This will use data from the folders `newdata/` and `college stats/` then cleaned and standardized the data. The output of this code will be stored in the folder called `clean_data/`.
    - Run the Jupyter Notebook called `feature_engineering.ipynb`. This will import data from the following folders `clean_data/`,`other features/` then create new features that will used for feeding into the model. The final output of this will be stored in `training/`
3. Run the Notebook called `ModelCode.ipynb` which will use the data from `training/` to actually train our ML models and produce graphs and rankings.
    - After running the model multiple times we achieved the same results. However runnnig it again after a few weeks, we saw that some of the results changed for veteran QBs and rookie WRs. We were not able to find why this change occurred as all the code stayed the same. We would like to examine this further in our future work.


Why We Chose This Topic
------------

Problem: Fantasy football is continuously increasing in popularity and newer/casual users need more insight into their roster formation

Solution: Using data and machine learning can help improve decisions and we learned which models and features can give the best projections and insight

Problem: Issue of poor performance projecting rookies in our research and rookies are a valuable part of fantasy – can be top performers but initially undervalued

Solution: We want to improve upon past research and be able to predict rookies more accurately

## Overview  
This project develops machine learning models to predict **season-long fantasy football performance** for NFL veterans and rookies. While most existing work focuses on weekly projections or purely NFL-level data, our work introduces a **rookie-specific modeling framework** that integrates college statistics, contextual team features, and schedule strength to improve preseason forecasting.

Our pipeline covers:
- Multi-source data cleaning (NFL stats, college stats, draft results)
- Feature engineering for positional strength of schedule, team context, and rookie college-to-NFL transitions
- A unified ML modeling framework with hyperparameter tuning and feature selection
- A novel approach for rookie prediction, addressing the lack of historical NFL data
- A 2024 season holdout validation set used for final unbiased performance evaluation

---

## Key Contributions  

### **1. Rookie Performance Simulation (Novel Contribution)**  
Rookie forecasting is typically unreliable due to missing NFL history.  
Our approach models rookies by:
- Mapping college production metrics → NFL-adjusted context  
- Incorporating schedule strength, team offensive efficiency, and positional opportunity  
- Generating "pseudo-historical" features for rookies so standard ML models can evaluate them  

This closes one of the largest gaps in available fantasy-prediction research.

### **2. Context-Aware Feature Engineering**  
We build features using:
- Position-specific defensive strength of schedule  
- Team-level offensive strength and pace  
- College efficiency and per-game metrics (for rookies)  
- Preseason rankings and opportunity share indicators  
- Age, draft capital, and career trajectory variables  

### **3. Multi-Model Framework**  
We evaluate several models under a unified pipeline:
- **XGBoost**
- **Random Forest**
- **Lasso Regression**
- **Support Vector Regression**
- **Neural Network**

Each model uses consistent preprocessing, tuning, and evaluation.

### **4. Feature Selection via Backward Elimination**  
We implement custom backward feature elimination:
1. Fit the model  
2. Rank features by importance  
3. Drop the least important  
4. Refit and check RMSE  
5. Stop when performance worsens  

This identifies the most predictive subset of features for each model.

### **5. Modeling Goals / Hypotheses**  
- Predict veteran fantasy scores within **RMSE ≤ 50**  
- Predict rookie fantasy scores within **RMSE ≤ 60**  
- Validate all final models on a 2024 holdout test set  

---

## Data Sources  
- **NFL Player Statistics** — season-level and advanced stats  
- **College Statistics** — Football-Reference and scraped datasets  
- **Draft Data** — draft year, pick, team, college  
- **Schedule Strength** — positional defensive ratings and opponent lists  
- **Team Strength Metrics** — adjusted offensive efficiency  

---

## Data Processing & Feature Engineering  

### **1. Data Cleaning**
Handled through the following notebooks and scripts:
- `cleaning_data_NFL.ipynb` — cleans and standardizes NFL player data  
- `clean_rookies.ipynb` — processes rookie and college player data  
- `stat_scraper.py` — scrapes missing data (college tables, stats)  
- Name normalization (lowercasing, removing suffixes, punctuation handling)  
- Team/year consistency checks  
- Imputation for gaps (e.g., years missing schedule data)

### **2. Feature Engineering**
Implemented in:
- `feature_engineering.ipynb`  
- `other features/`  

Key features include:
- Average positional strength of schedule  
- College per-game metrics (yardage, usage, efficiency)  
- Team-level offensive metrics  
- Draft capital, age, career stage  
- Preseason rankings and opportunity indicators

### **3. Rookie-Specific Feature Mapping**
- College stats mapped to NFL equivalents  
- Opponent strength adjusted for positional tendencies  
- Team context applied to rookies to mimic NFL history  

---

## Modeling Framework  

Implemented in `ModelCode.ipynb`.

### **Unified Preprocessing Pipeline**
All models use:
- `SimpleImputer` → mean imputation  
- `StandardScaler` → standardization  
- An estimator (RF, XGB, SVR, etc.)  

Ensures uniformity across model comparisons.

### **Custom RMSE Scorer**
A custom RMSE metric is used for all evaluations.

### **Hyperparameter Tuning**
GridSearchCV + K-Fold cross-validation determines optimal model parameters.

### **Backward Feature Elimination**
A custom elimination loop identifies the best subset of features by iteratively removing the least important ones until RMSE stops improving.

### **Holdout Validation (2024 Season)**
After selecting the best model and feature set for each position, the **2024 season was held out entirely** and used as the final validation dataset.  
This provides:
- An unbiased measure of real-world predictive performance  
- A strict test of generalization beyond historical seasons  

### **Final Inference**
A helper function fits the final model on selected features and generates predictions for a new season dataset.

---
## Project Structure
```
root/
│
├── Parent_code/
├── clean_data/
├── college stats/
├── newdata/
├── other features/
├── training/
│
├── ModelCode.ipynb
├── README.md
├── clean_rookies.ipynb
├── cleaning_data_NFL.ipynb
├── feature_engineering.ipynb
└── stat_scraper.py
```
---

## Team  

Kush Lalwani - Data collection 
Kush Lalwani - Cleaning and normalization  
Kush Lalwani - Feature engineering  
Trevor Bunch - Modeling and evaluation  
Trevor Bunch - Report writing and analysis  


