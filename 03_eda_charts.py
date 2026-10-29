import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

crime = pd.read_csv("data/cleaned_crime_data.csv")

#main crime categories (sub-categories left out so nothing is counted twice)
main = ["murder", "attempt_to_murder", "culpable_homicide_not_amounting_to_murder", "rape",
        "kidnapping_and_abduction", "dacoity", "robbery", "burglary", "theft", "riots",
        "criminal_breach_of_trust", "cheating", "counterfieting", "arson", "hurt_grevious_hurt",
        "dowry_deaths", "cruelty_by_husband_or_his_relatives", "causing_death_by_negligence"]

#1. crime count by category
cat_total = crime[main].sum().sort_values()
plt.figure(figsize=(9, 6))
cat_total.plot(kind="barh", color="steelblue")
plt.title("Total registered IPC crimes by category, India 2013")
plt.xlabel("Number of cases")
plt.tight_layout()
plt.savefig("outputs/figures/1_crime_by_category.png")
plt.close()

#2. top 10 states
state_total = crime.groupby("state_ut")["total_ipc_crimes"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
state_total.sort_values().plot(kind="barh", color="darkorange")
plt.title("Top 10 states/UTs by total registered IPC crimes, 2013")
plt.xlabel("Number of cases (not adjusted for population)")
plt.tight_layout()
plt.savefig("outputs/figures/2_top_states.png")
plt.close()

#3. top 10 districts
top = crime.sort_values("total_ipc_crimes", ascending=False).head(10)
labels = top["district"] + " (" + top["state_ut"] + ")"
plt.figure(figsize=(10, 5))
plt.barh(labels[::-1], top["total_ipc_crimes"][::-1], color="seagreen")
plt.title("Top 10 districts by total registered IPC crimes, 2013")
plt.xlabel("Number of cases (not adjusted for population)")
plt.tight_layout()
plt.savefig("outputs/figures/3_top_districts.png")
plt.close()

#4. distribution of the total crimes per district
plt.figure(figsize=(8, 5))
sns.histplot(crime["total_ipc_crimes"], bins=40, color="purple")
plt.title("Distribution of total IPC crimes per district (right skewed)")
plt.xlabel("Total IPC crimes in a district")
plt.tight_layout()
plt.savefig("outputs/figures/4_distribution_total.png")
plt.close()

#5. correlation heatmap
plt.figure(figsize=(11, 9))
sns.heatmap(crime[main].corr(), cmap="coolwarm", center=0)
plt.title("Correlation between crime categories (district level, 2013)")
plt.tight_layout()
plt.savefig("outputs/figures/5_correlation_heatmap.png")
plt.close()

print("Charts saved in outputs/figures/")
print()
print("Top 5 categories:")
print(cat_total.tail(5)[::-1])
print()
print("Top 5 states:")
print(state_total.head(5))

#correlation values (Pearson) of murder with other crimes
print()
print("Correlation of murder with other crimes:")
print(crime[main].corr()["murder"].drop("murder").sort_values(ascending=False).round(3).head(6))
