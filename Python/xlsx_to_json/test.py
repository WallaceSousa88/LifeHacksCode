# pip install pymupdf

import fitz
import os

def pdf_to_text(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if not text.strip():
                text = "[Imagem encontrada na página]\n"
            txt_file.write(text)
            txt_file.write("\n\n")

def main():
    input_dir = 'entrada'
    output_dir = 'saida'
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_dir, txt_filename)
            pdf_to_text(pdf_path, txt_path)

if __name__ == "__main__":
    main()
