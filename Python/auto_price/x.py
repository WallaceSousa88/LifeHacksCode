# Regressão Linear

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('car_price_dataset.csv')

X = df[['Brand', 'Model', 'Year', 'Engine_Size', 'Fuel_Type', 'Transmission', 'Mileage', 'Doors', 'Owner_Count']]
y = df['Price']

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

def prever_preco():
    brand = input("Marca: ")
    model_car = input("Modelo: ")
    year = int(input("Ano: "))
    engine_size = float(input("Tamanho do Motor: "))
    fuel_type = input("Tipo de Combustível: ")
    transmission = input("Transmissão: ")
    mileage = int(input("Quilometragem: "))
    doors = int(input("Número de Portas: "))
    owner_count = int(input("Número de Proprietários Anteriores: "))

    user_data = pd.DataFrame({
        'Brand': [brand],
        'Model': [model_car],
        'Year': [year],
        'Engine_Size': [engine_size],
        'Fuel_Type': [fuel_type],
        'Transmission': [transmission],
        'Mileage': [mileage],
        'Doors': [doors],
        'Owner_Count': [owner_count]
    })

    user_data = pd.get_dummies(user_data, drop_first=True)
    user_data = user_data.reindex(columns=X.columns, fill_value=0)

    predicted_price = model.predict(user_data)
    print(f"O preço estimado do carro é: {predicted_price[0]}")

prever_preco()