import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, log_loss, roc_auc_score, precision_score,
                             recall_score, f1_score, confusion_matrix, roc_curve)

crime = pd.read_csv("data/cleaned_crime_data.csv")

#label: 1 = murder cases above the median district, 0 = otherwise
#(only a demonstration label, it is not an official NCRB category)
crime["high_murder"] = (crime["murder"] > crime["murder"].median()).astype(int)
print(crime["high_murder"].value_counts())

features = ["attempt_to_murder", "culpable_homicide_not_amounting_to_murder", "rape", "kidnapping_and_abduction",
            "dacoity", "robbery", "burglary", "theft", "riots", "criminal_breach_of_trust", "cheating",
            "arson", "hurt_grevious_hurt", "dowry_deaths", "causing_death_by_negligence"]
x = crime[features]
y = crime["high_murder"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

#baseline = always guess the most common class
models = {
    "Baseline": DummyClassifier(strategy="prior"),
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "KNN (k=5)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    "Naive Bayes": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=42),
    "SVM (rbf)": make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True, random_state=42)),
}

rows = []
plt.figure(figsize=(7, 6))
for name, model in models.items():
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    cv = cross_val_score(model, x, y, cv=5).mean()
    rows.append([name,
                 round(accuracy_score(y_test, y_pred), 4),
                 round(log_loss(y_test, model.predict_proba(x_test)), 4),
                 round(roc_auc_score(y_test, y_prob), 4),
                 round(precision_score(y_test, y_pred, zero_division=0), 4),
                 round(recall_score(y_test, y_pred), 4),
                 round(f1_score(y_test, y_pred), 4),
                 round(cv, 4)])
    print(name, "confusion matrix:", cm.tolist())

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr, label=name)

result = pd.DataFrame(rows, columns=["Model", "Accuracy", "Log loss", "AUC", "Precision", "Recall", "F1", "5-fold CV accuracy"])
print()
print(result.to_string(index=False))
result.to_csv("outputs/model_comparison.csv", index=False)

#ROC curve
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False positive rate")
plt.ylabel("True positive rate")
plt.title("ROC curves (high murder district)")
plt.legend()
plt.savefig("outputs/figures/10_roc_curves.png")
plt.close()
