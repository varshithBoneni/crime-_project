import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

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

#SVM also needs scaled data
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#compare different kernels
for kernel in ["linear", "poly", "rbf"]:
    svm = SVC(kernel=kernel, random_state=42)
    svm.fit(x_train, y_train)
    print(kernel, "kernel accuracy:", round(accuracy_score(y_test, svm.predict(x_test)), 4))

svm = SVC(kernel="rbf", random_state=42)
svm.fit(x_train, y_train)
y_pred = svm.predict(x_test)

print()
print("Confusion matrix (rbf):")
print(confusion_matrix(y_test, y_pred))
