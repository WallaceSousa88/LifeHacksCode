import tensorflow as tf

def criar_modelo(num_classes):
    # Defina a arquitetura da sua CNN aqui
    modelo = tf.keras.models.Sequential([
        # ... (Camadas da sua CNN)
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return modelo