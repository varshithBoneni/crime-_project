import pandas as pd

#load dataset
crime = pd.read_csv("data/raw/dstrIPC_2013.csv")

#basic information
print("Shape:", crime.shape)
print()
print("Columns:")
print(list(crime.columns))
print()
print(crime.dtypes.value_counts())
print()
print(crime.head())

#check missing values and duplicates
print()
print("Total missing values:", crime.isnull().sum().sum())
print("Duplicate rows:", crime.duplicated().sum())

#check year and state
print()
print("Years in the file:", crime["YEAR"].unique())
print("Number of states/UTs:", crime["STATE/UT"].nunique())
print("Number of districts:", crime["DISTRICT"].nunique())

#check negative values
numbers = crime.iloc[:, 3:]
print("Negative values:", (numbers < 0).sum().sum())

#important note
print()
print("NOTE: only one year (2013) is present, so forecasting future years is NOT possible with this file.")
