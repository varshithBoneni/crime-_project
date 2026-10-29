import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

crime = pd.read_csv("data/cleaned_crime_data.csv")

#x = burglary cases, y = theft cases (same district, same year)
x = crime[["burglary"]]
y = crime["theft"]

#correlation between x and y
print("Correlation:", round(x["burglary"].corr(y), 4))

#split the data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)

#evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
print("MAE :", round(mae, 2))
print("MSE :", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 4))

#predict for a new district
burglary = pd.DataFrame({"burglary": [500]})
theft = model.predict(burglary)
print(f"A district with {burglary['burglary'][0]} burglary cases is estimated to have {theft[0]:.2f} theft cases")

#plot
plt.scatter(x_test, y_test, color="blue", label="Actual")
xs = x_test.sort_values("burglary")
plt.plot(xs, model.predict(xs), color="red", label="Regression line")
plt.xlabel("Burglary cases")
plt.ylabel("Theft cases")
plt.title("Simple Linear Regression: Burglary vs Theft (2013)")
plt.legend()
plt.savefig("outputs/figures/6_simple_linear_regression.png")
plt.close()
