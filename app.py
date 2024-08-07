from flask import Flask, request, jsonify, send_from_directory, send_file
from pdf2image import convert_from_path
import os
import zipfile

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    pdf_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(pdf_path)

    images = convert_from_path(pdf_path, poppler_path=r'C:\poppler\poppler-24.07.0\Library\bin')

    # Salva as imagens e armazena os caminhos
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join('uploads', f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)

    # Cria o arquivo ZIP
    zip_path = 'uploads/images.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for image_path in image_paths:
            zipf.write(image_path, os.path.basename(image_path))

    return send_file(zip_path, as_attachment=True, download_name='images.zip')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)
