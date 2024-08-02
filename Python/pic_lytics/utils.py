import tensorflow as tf

def carregar_imagem(caminho_imagem, largura=224, altura=224):
    imagem = tf.keras.preprocessing.image.load_img(caminho_imagem, target_size=(largura, altura))
    imagem = tf.keras.preprocessing.image.img_to_array(imagem)
    imagem = np.expand_dims(imagem, axis=0)
    imagem = imagem / 255.0
    return imagem