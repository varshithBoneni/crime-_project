import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

crime = pd.read_csv("data/cleaned_crime_data.csv")

x = crime[["burglary"]]
y = crime["theft"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#try different degrees
print("Degree  Train R2  Test R2   Test MAE   Test RMSE")
for degree in [1, 2, 3, 4, 5]:
    poly = PolynomialFeatures(degree=degree)
    x_train_p = poly.fit_transform(x_train)
    x_test_p = poly.transform(x_test)

    model = LinearRegression()
    model.fit(x_train_p, y_train)

    pred_train = model.predict(x_train_p)
    pred_test = model.predict(x_test_p)
    print(degree, "     ", round(r2_score(y_train, pred_train), 4), "   ", round(r2_score(y_test, pred_test), 4),
          "   ", round(mean_absolute_error(y_test, pred_test), 1), "   ", round(np.sqrt(mean_squared_error(y_test, pred_test)), 1))

#plot degree 2 curve
poly = PolynomialFeatures(degree=2)
model = LinearRegression()
model.fit(poly.fit_transform(x_train), y_train)

line = pd.DataFrame({"burglary": np.linspace(0, x["burglary"].max(), 200)})
plt.scatter(x_test, y_test, color="blue", s=12, label="Actual")
plt.plot(line, model.predict(poly.transform(line)), color="red", label="Degree 2 curve")
plt.xlabel("Burglary cases")
plt.ylabel("Theft cases")
plt.title("Polynomial Regression (degree 2)")
plt.legend()
plt.savefig("outputs/figures/8_polynomial_regression.png")
plt.close()
print()
print("Higher degree gives a better train score but may be worse on test data (overfitting).")
