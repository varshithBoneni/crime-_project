# Indian Crime Trend Analysis and Prediction Using Machine Learning

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)
![Statistical Analysis](https://img.shields.io/badge/Statistics-SciPy-green)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

## Project Overview
This repository contains an end-to-end data science and machine learning research project analyzing district-level crime patterns across India using official records from the **National Crime Records Bureau (NCRB)**, Ministry of Home Affairs, Government of India (published via [data.gov.in](https://data.gov.in/)).

The project formulates and evaluates:
1. **Continuous Crime Volume Prediction (Regression)**: Modeling property crimes (predicting district theft volume from burglary counts using Simple Linear Regression and Polynomial Regression) and severe violent crimes (estimating murder occurrences from co-occurring violent IPC offenses using Multiple Linear Regression with analytical Ordinary Least Squares).
2. **High-Risk Crime Classification**: Classifying whether an administrative district falls into the high-violence / high-murder risk category (`high_murder = 1` for districts exceeding the national median of 34 cases) using five machine learning classifiers (**Logistic Regression**, **K-Nearest Neighbours**, **Gaussian Naive Bayes**, **Decision Trees**, and **Support Vector Machines**).
3. **Inferential Hypothesis Testing**: Evaluating regional disparities and spatial dependencies through **Pearson correlation**, **One-way ANOVA** across geographic zones, **Welch's two-sample $t$-test**, and **Chi-Square tests of independence**.

---

## Academic Information
- **Course**: INT234 (Data Science / Predictive Analysis)
- **Institution**: Lovely School of Computer Science and Engineering, Lovely Professional University, Phagwara, Punjab
- **Student**: Boneni Varshith (Registration No. 12407267, Roll No. 11, Section RK3P24PSA11)
- **Project Guide**: Tanima Thakur

---

## Dataset Description
- **File**: `data/raw/dstrIPC_2013.csv`
- **Source**: National Crime Records Bureau (NCRB), "Crime in India 2013" district-wise IPC table.
- **Raw Dimensions**: 823 rows × 33 columns across 35 States and Union Territories.
- **Data Preprocessing & Auditing**:
  - Removed **35 statewide aggregate summary rows** (`ZZ TOTAL`) to prevent 100% double-counting.
  - Filtered **34 non-district specialized policing units** (e.g., Railway Police / GRP, CID, Crime Branch units) that operate across multiple civil districts.
  - Resulting clean empirical dataset: **754 verified geographic districts** with **0 missing values** and **0 duplicate records**.

---

## Key Experimental Results

### 1. Regression Benchmarks (Predicting Continuous Crime Counts)
| Model | Target Offense | Predictors Used | Test MAE | Test RMSE | Test $R^2$ | Key Finding |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline (Mean)** | Theft | None (Predicts training mean) | 436.24 | 716.87 | -0.0001 | Naive central tendency reference |
| **Simple Linear Regression** | Theft | Burglary | 290.90 | 591.49 | 0.3191 | $17.5\%$ reduction in test RMSE over baseline |
| **Polynomial Regression (Degree 2)** | Theft | Burglary + $\text{Burglary}^2$ | **282.74** | **585.90** | **0.3319** | **Best property model**; captures urban escalation |
| **Polynomial (Degrees 4 & 5)** | Theft | Higher-order powers | 308.06 | 614.55 | 0.2650 | Degrades sharply due to overfitting |
| **Multiple Linear Regression (OLS)** | Murder | 7 Violent Crime Categories | **17.70** | **25.22** | **0.6075** | Explains $60.8\%$ of homicide variance; Dacoity and Attempt to Murder are primary drivers |

*Analytical OLS closed-form solution $\beta = (X^T X)^{-1} X^T y$ was verified from first principles and matched scikit-learn coefficients exactly (`np.allclose = True`).*

### 2. Classification Benchmarks (Predicting High Murder Risk Districts)
*Evaluated on independent unseen test partition of 151 districts (balanced 49.7% high risk / 50.3% low risk):*

| Model Architecture | Accuracy | Log Loss | ROC-AUC | Precision | Recall | F1-Score | 5-Fold CV Accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Majority Baseline** | 50.33% | 0.6931 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | 50.13% |
| **Logistic Regression** | **86.75%** | **0.2863** | **0.9528** | 0.8667 | **0.8667** | **0.8667** | **81.44%** |
| **KNN ($k=5$)** | **86.75%** | 0.7458 | 0.9306 | **0.8767** | 0.8533 | 0.8649 | 78.92% |
| **SVM (RBF Kernel)** | 86.09% | 0.3059 | 0.9423 | 0.8649 | 0.8533 | 0.8591 | **81.44%** |
| **Decision Tree ($\text{depth}=3$)** | 84.11% | 0.4090 | 0.8994 | 0.8592 | 0.8133 | 0.8356 | 74.67% |
| **Gaussian Naive Bayes** | 79.47% | 2.2622 | 0.9011 | 0.8667 | 0.6933 | 0.7704 | 78.66% |

- **Top Classifier**: Logistic Regression achieved the highest calibration ($\text{Log Loss} = 0.2863$, $\text{AUC} = 0.9528$, $F_1 = 0.8667$).
- **Interpretability**: Pruned Decision Tree reveals that `attempt_to_murder` ($> 74\%$ feature importance) is the primary dividing threshold for lethal crime risk.
- **Multicollinearity Impact**: Gaussian Naive Bayes underperformed due to violated conditional independence assumptions across co-occurring violent offenses.

---

## Statistical Hypothesis Tests Summary
- **Pearson Correlation**: Burglary vs Theft ($r = 0.884, p < 0.0001$), Attempt to Murder vs Murder ($r = 0.778, p < 0.0001$).
- **One-Way ANOVA Across 6 Geographic Zones**:
  - Total IPC Crimes: $F = 29.38, p = 2.77 \times 10^{-27}$ (South highest at 5,833.3 mean; North-East lowest at 1,022.8).
  - Murder Volume: $F = 22.61, p = 3.65 \times 10^{-21}$ (East highest at 67.6 mean).
- **Two-Sample Welch's $t$-Test (North vs South)**: $t = -7.85, p = 4.40 \times 10^{-13}$.
- **Chi-Square Test of Independence (Zone vs High Murder Risk)**: $\chi^2 = 70.63, df = 5, p = 7.59 \times 10^{-14}$ (East has $72.9\%$ high-risk districts; North-East has $20.2\%$).

---

## Repository Structure
```
crime_project/
├── data/
│   ├── raw/
│   │   └── dstrIPC_2013.csv               # Raw official NCRB dataset (823 rows)
│   └── cleaned_crime_data.csv            # Cleaned dataset (754 genuine districts)
├── outputs/
│   ├── cleaning_report.txt               # Verification audit of row filtering
│   ├── model_comparison.csv             # Quantitative metrics across all models
│   └── figures/
│       ├── 1_crime_by_category.png       # Total IPC crimes by category
│       ├── 2_top_states.png              # Top 10 states by crime count
│       ├── 3_top_districts.png           # Top 10 districts by crime count
│       ├── 4_distribution_total.png      # Skewed district crime distribution
│       ├── 5_correlation_heatmap.png     # Full IPC correlation matrix
│       ├── 6_simple_linear_regression.png# Burglary vs Theft fit
│       ├── 7_multiple_regression_actual_vs_predicted.png # OLS murder prediction
│       ├── 8_polynomial_regression.png   # Degree 2 quadratic curve
│       ├── 9_decision_tree.png           # Full visual decision tree
│       ├── 10_roc_curves.png             # Multi-model ROC comparison
│       ├── fig_box_zones.png             # Crime distribution across zones
│       ├── fig_reg_rmse.png              # Regression error comparison
│       ├── fig_knn_k.png                 # Hyperparameter tuning curve for kNN
│       ├── fig_dt_importance.png         # Decision tree feature importances
│       ├── fig_confusion_matrices.png    # 5-model confusion matrices
│       └── fig_f1_scores.png             # F1-score comparison
├── reports/
│   ├── Indian_Crime_Prediction_Report.pdf # Official 41-page academic project report
│   ├── Indian_Crime_Prediction_Report.docx# Editable Word report
│   └── build_and_sync_report.py          # Python report generation engine
├── 01_load_and_inspect.py                # Schema inspection & validation
├── 02_clean_data.py                      # Data preprocessing & anomaly removal
├── 03_eda_charts.py                      # Visual exploratory analysis
├── 04_simple_linear_regression.py        # Simple linear modeling (Theft)
├── 05_multiple_regression_ols.py         # Multiple OLS regression (Murder)
├── 06_polynomial_regression.py           # Polynomial curve fitting (Degrees 1-5)
├── 07_logistic_regression.py             # Logistic regression classifier
├── 08_knn_classification.py              # K-Nearest Neighbours tuning & evaluation
├── 09_naive_bayes.py                     # Gaussian Naive Bayes model
├── 10_decision_tree.py                   # Pruned Decision Tree & rule extraction
├── 11_support_vector_machine.py          # SVM with linear, poly, and RBF kernels
├── 12_evaluation_and_comparison.py       # Master model evaluation & ROC curves
├── requirements.txt                      # Project dependencies
└── README.md                             # Comprehensive project documentation
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/varshithBoneni/crime_project.git
cd crime_project
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute the Pipeline
Run scripts in sequential order:
```bash
python 01_load_and_inspect.py
python 02_clean_data.py
python 03_eda_charts.py
python 04_simple_linear_regression.py
python 05_multiple_regression_ols.py
python 06_polynomial_regression.py
python 07_logistic_regression.py
python 08_knn_classification.py
python 09_naive_bayes.py
python 10_decision_tree.py
python 11_support_vector_machine.py
python 12_evaluation_and_comparison.py
```

---

## Academic Project Reports
The complete, professionally formatted university report is located in the `reports/` directory:
- 📕 **[Indian_Crime_Prediction_Report.pdf](reports/Indian_Crime_Prediction_Report.pdf)**
- 📘 **[Indian_Crime_Prediction_Report.docx](reports/Indian_Crime_Prediction_Report.docx)**

---

## Author & Acknowledgements
- **Author**: Boneni Varshith (Registration No. 12407267)
- **Institution**: Lovely Professional University, Punjab, India
- **Data Source**: National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of India
