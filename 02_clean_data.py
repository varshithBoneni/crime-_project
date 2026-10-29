import pandas as pd

#load dataset
crime = pd.read_csv("data/raw/dstrIPC_2013.csv")
rows_start = len(crime)

#clean the text columns
crime["STATE/UT"] = crime["STATE/UT"].str.strip()
crime["DISTRICT"] = crime["DISTRICT"].str.strip().str.upper()

report = []
report.append("Rows in raw file: " + str(rows_start))

#check state total rows against sum of districts before removing them
totals = crime[crime["DISTRICT"] == "ZZ TOTAL"]
others = crime[crime["DISTRICT"] != "ZZ TOTAL"]
check = others.groupby("STATE/UT")["TOTAL IPC CRIMES"].sum()
matched = 0
for i, row in totals.iterrows():
    if check[row["STATE/UT"]] == row["TOTAL IPC CRIMES"]:
        matched = matched + 1
report.append("ZZ TOTAL rows: " + str(len(totals)) + " (state total equals sum of its other rows in " + str(matched) + " states)")

#remove state total rows (they would double count)
crime = crime[crime["DISTRICT"] != "ZZ TOTAL"]
report.append("Removed ZZ TOTAL rows (double counting): " + str(len(totals)))

#remove railway police and other special units, they are not districts
special = crime["DISTRICT"].str.contains(r"RLY|RAILWAY|GRP|CID|CRIME", regex=True)
removed = crime[special]
report.append("Removed railway/GRP/CID/crime-branch units: " + str(len(removed)))
report.append("Examples: " + ", ".join(removed["DISTRICT"].head(8)))
crime = crime[~special]

#make column names easy to use
crime.columns = [c.strip().lower().replace("/", "_").replace(" ", "_").replace("&", "and") for c in crime.columns]

#final checks
report.append("Rows in cleaned file: " + str(len(crime)))
report.append("Missing values after cleaning: " + str(crime.isnull().sum().sum()))
report.append("Duplicate (state, district) rows: " + str(crime.duplicated(["state_ut", "district"]).sum()))
report.append("Negative counts: " + str((crime.iloc[:, 3:] < 0).sum().sum()))
report.append("Zero counts were kept as zero (NCRB table reports 0 for no registered cases).")

crime.to_csv("data/cleaned_crime_data.csv", index=False)

#save report
text = "\n".join(report)
open("outputs/cleaning_report.txt", "w").write(text)
print(text)
