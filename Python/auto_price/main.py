# pip install pandas numpy matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

dataset = pd.read_csv("car_price_dataset.csv")

output_dir = "analise_dados"
os.makedirs(output_dir, exist_ok=True)

numerical_columns = dataset.select_dtypes(include=["int64", "float64"]).columns

medias = dataset[numerical_columns].mean()
medianas = dataset[numerical_columns].median()
modas = dataset[numerical_columns].mode().iloc[0]

with open(f"{output_dir}/medidas_tendencia_central.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Variable':<15}{'Média':<15}{'Mediana':<15}{'Moda':<15}\n")
    for var, media, mediana, moda in zip(medias.index, medias, medianas, modas):
        f.write(f"{var:<15}{media:<15.2f}{mediana:<15.2f}{moda:<15.2f}\n")

desvios = dataset[numerical_columns].std()
q1 = dataset[numerical_columns].quantile(0.25)
q3 = dataset[numerical_columns].quantile(0.75)
iqr = q3 - q1

with open(f"{output_dir}/medidas_dispersao.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Variable':<15}{'Desvio Padrão':<15}{'Q1':<15}{'Q3':<15}{'IQR':<15}\n")
    for var, desvio, q1_value, q3_value, iqr_value in zip(desvios.index, desvios, q1, q3, iqr):
        f.write(f"{var:<15}{desvio:<15.2f}{q1_value:<15.2f}{q3_value:<15.2f}{iqr_value:<15.2f}\n")

outliers_count = ((dataset[numerical_columns] < (q1 - 1.5 * iqr)) |
                  (dataset[numerical_columns] > (q3 + 1.5 * iqr))).sum()

with open(f"{output_dir}/outliers_detectados.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Variable':<15}{'Outliers Detected':<15}\n")
    for var, outlier_count in zip(outliers_count.index, outliers_count):
        f.write(f"{var:<15}{outlier_count:<15}\n")

correlation = dataset[numerical_columns].corr()

with open(f"{output_dir}/correlacao.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Variable':<15}" + "".join([f"{col:<15}" for col in correlation.columns]) + "\n")
    for var, values in correlation.iterrows():
        f.write(f"{var:<15}" + "".join([f"{val:<15.2f}" for val in values]) + "\n")

for column in numerical_columns:
    plt.figure()
    plt.hist(dataset[column], bins=20, color="skyblue", edgecolor="black")
    plt.title(f"Histograma de {column}")
    plt.xlabel(column)
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.savefig(f"{output_dir}/histograma_{column}.png")
    plt.close()

    plt.figure()
    sns.boxplot(x=dataset[column], color="lightcoral")
    plt.title(f"Box Plot de {column}")
    plt.savefig(f"{output_dir}/boxplot_{column}.png")
    plt.close()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Mapa de calor da correlação")
plt.savefig(f"{output_dir}/mapa_calor_correlation.png")
plt.close()

for column in numerical_columns:
    if column != "Price":
        plt.figure()
        sns.scatterplot(x=dataset[column], y=dataset["Price"])
        plt.title(f"Dispersão: {column} vs Preço")
        plt.xlabel(column)
        plt.ylabel("Preço")
        plt.savefig(f"{output_dir}/dispersao_{column}_vs_preco.png")
        plt.close()

print(f"Resultados salvos na pasta '{output_dir}'.")