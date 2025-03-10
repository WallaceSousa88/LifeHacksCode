# pip install pandas scikit-learn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv('car_price_dataset.csv')
X = df[['Brand', 'Model', 'Year', 'Engine_Size', 'Fuel_Type', 'Transmission', 'Mileage', 'Doors', 'Owner_Count']]
y = df['Price']
X = pd.get_dummies(X, drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Erro Absoluto Médio: {mae}')
print(f'Erro Quadrático Médio: {mse}')
print(f'R-quadrado: {r2}')

residuos = y_test - y_pred

plt.figure(figsize=(10, 6))
sns.boxplot(x=residuos)
plt.title("Boxplot dos Resíduos")
plt.xlabel("Resíduos")
plt.show()

z_scores = np.abs(stats.zscore(residuos))
limiar = 3
outlier_indices = np.where(z_scores > limiar)[0]
print("Índices dos possíveis outliers (z-score > 3):", outlier_indices)
print("Valores dos resíduos outliers:", residuos.iloc[outlier_indices])

plt.figure(figsize=(10, 6))
plt.hist(residuos, bins=30, edgecolor='k')
plt.title("Histograma dos Resíduos")
plt.xlabel("Resíduo")
plt.ylabel("Frequência")
plt.show()