import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from modelo import criar_modelo

def treinar_modelo(caminho_dados):
    # Parâmetros do treinamento
    largura, altura = 224, 224  # Ajuste conforme necessário
    tamanho_lote = 32
    epocas = 10

    # Carregar dados de treinamento com aumento de dados
    gerador_treino = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    dados_treino = gerador_treino.flow_from_directory(
        caminho_dados,
        target_size=(largura, altura),
        batch_size=tamanho_lote,
        class_mode='categorical'
    )

    # Criar o modelo
    modelo = criar_modelo(num_classes=len(dados_treino.class_indices))

    # Compilar e treinar o modelo
    modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    modelo.fit(
        dados_treino,
        steps_per_epoch=dados_treino.samples // tamanho_lote,
        epochs=epocas
    )

    # Salvar o modelo treinado
    modelo.save('modelo_treinado.h5')
    print("Modelo treinado salvo com sucesso!")