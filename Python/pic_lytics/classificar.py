import os
import numpy as np
import tensorflow as tf
from utils import carregar_imagem

def classificar_imagens(caminho_modelo, caminho_imagens):
    # Carregar o modelo treinado
    modelo = tf.keras.models.load_model(caminho_modelo)

    # Obter a lista de classes do modelo
    classes = ['Classe1', 'Classe2', ...]  # Substitua pelas classes reais

    # Classificar cada imagem na pasta
    for nome_arquivo in os.listdir(caminho_imagens):
        caminho_imagem = os.path.join(caminho_imagens, nome_arquivo)
        imagem = carregar_imagem(caminho_imagem)
        previsao = modelo.predict(imagem)
        classe_prevista = np.argmax(previsao)

        print(f"Imagem: {nome_arquivo}, Classe prevista: {classes[classe_prevista]}")