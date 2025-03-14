# Random Forest

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('car_price_dataset.csv')

X = df[['Brand', 'Model', 'Year', 'Engine_Size', 'Fuel_Type', 'Transmission', 'Mileage', 'Doors', 'Owner_Count']]
y = df['Price']

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

def prever_preco():
    brand = input("Marca: ")
    model_car = input("Modelo: ")
    try:
        year = int(input("Ano (ex: 2015): "))
    except ValueError:
        print("Valor inválido para o ano. Tente novamente.")
        return

    try:
        engine_size = float(input("Tamanho do Motor (ex: 2.0): "))
    except ValueError:
        print("Valor inválido para o tamanho do motor. Tente novamente.")
        return

    fuel_type = input("Tipo de Combustível (ex: Gasolina, Diesel, etc.): ")
    transmission = input("Transmissão (ex: Manual ou Automática): ")

    try:
        mileage = int(input("Quilometragem: "))
    except ValueError:
        print("Valor inválido para a quilometragem. Tente novamente.")
        return

    try:
        doors = int(input("Número de Portas: "))
    except ValueError:
        print("Valor inválido para o número de portas. Tente novamente.")
        return

    try:
        owner_count = int(input("Número de Proprietários Anteriores: "))
    except ValueError:
        print("Valor inválido para o número de proprietários. Tente novamente.")
        return

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
    print(f"\nO preço estimado do carro é: {predicted_price[0]:.2f}")

if __name__ == "__main__":
    prever_preco()
