import os
from flask import Flask, render_template, request, send_from_directory
from rembg import remove
from PIL import Image
import openai
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'



os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    style = request.form['style']
    filename = f"{uuid.uuid4().hex}.png"

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    # Background removal
    with open(input_path, 'rb') as inp:
        output = remove(inp.read())
    bg_removed_path = os.path.join(app.config['UPLOAD_FOLDER'], f"nobg_{filename}")
    with open(bg_removed_path, 'wb') as out:
        out.write(output)

    # OpenAI image edit
    with open(bg_removed_path, "rb") as img:
        result = openai.images.edit(
            image=img,
            prompt=f"Change the outfit of the person in this image to a {style}. Keep the body realistic and maintain facial features.",
            n=1,
            size="512x512"
        )

    image_url = result['data'][0]['url']
    return render_template('index.html', output_image=image_url, file_name=filename)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
