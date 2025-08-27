# pip install pytesseract opencv-python pillow numpy
# https://sourceforge.net/projects/tesseract-ocr.mirror/

import cv2
import pytesseract
import re
import numpy as np

from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = 'x.png'
image = Image.open(image_path)

texto_original = pytesseract.image_to_string(image, lang='eng')
print("Texto encontrado na imagem original:")
print(texto_original)

image = ImageEnhance.Brightness(image).enhance(1.0)
image = ImageEnhance.Contrast(image).enhance(2.0)
image = ImageEnhance.Color(image).enhance(0.0)
image = ImageEnhance.Sharpness(image).enhance(2.0)

image_np = np.array(image)
image_hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
h, s, v = cv2.split(image_hsv)
h = cv2.add(h, 100)
v = cv2.add(v, 100)
image_hsv = cv2.merge([h, s, v])
image_np = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

cv2.imwrite('imagem_tratada.png', image_np)

gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
pil_img = Image.fromarray(gray)

texto_tratado = pytesseract.image_to_string(pil_img, lang='eng')
print("\nTexto encontrado na imagem tratada:")
print(texto_tratado)

psm_modes = ['7', '8', '13']
numeros_encontrados = set()

for psm in psm_modes:
    config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist=0123456789'
    texto = pytesseract.image_to_string(pil_img, lang='eng', config=config)
    numeros = re.findall(r'\b\d{5}\b', texto)
    numeros_encontrados.update(numeros)

contornos_img = gray.copy()
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 30 and h > 30:
        roi = gray[y:y+h, x:x+w]
        roi_pil = Image.fromarray(roi)
        config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        texto_roi = pytesseract.image_to_string(roi_pil, lang='eng', config=config)
        numeros_roi = re.findall(r'\b\d{5}\b', texto_roi)
        numeros_encontrados.update(numeros_roi)

print("\nNúmeros de 5 dígitos encontrados:", list(numeros_encontrados))