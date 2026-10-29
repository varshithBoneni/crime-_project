import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

crime = pd.read_csv("data/cleaned_crime_data.csv")

#predict murder cases using other crime counts of the same district
features = ["attempt_to_murder", "robbery", "dacoity", "riots", "arson", "hurt_grevious_hurt", "kidnapping_and_abduction"]
x = crime[features]
y = crime["murder"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

print("Coefficients:")
for name, value in zip(features, model.coef_):
    print(" ", name, round(value, 4))
print("Intercept:", round(model.intercept_, 4))

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print()
print("MAE :", round(mae, 2))
print("MSE :", round(mse, 2))
print("RMSE:", round(np.sqrt(mse), 2))
print("R2  :", round(r2_score(y_test, y_pred), 4))

#Ordinary Least Squares by hand: beta = (X'X)^-1 X'y
X = np.column_stack([np.ones(len(x_train)), x_train.values])
beta = np.linalg.inv(X.T @ X) @ X.T @ y_train.values
print()
print("OLS intercept:", round(beta[0], 4))
print("OLS coefficients:", np.round(beta[1:], 4))
print("Same as sklearn?", np.allclose(beta[1:], model.coef_))

#actual vs predicted
plt.scatter(y_test, y_pred, color="green")
plt.plot([0, y_test.max()], [0, y_test.max()], color="red")
plt.xlabel("Actual murder cases")
plt.ylabel("Predicted murder cases")
plt.title("Multiple Linear Regression: actual vs predicted")
plt.savefig("outputs/figures/7_multiple_regression_actual_vs_predicted.png")
plt.close()
