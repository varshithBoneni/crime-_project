import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

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

model = GaussianNB()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print(classification_report(y_test, y_pred, target_names=["low", "high"]))
