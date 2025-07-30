from flask import Flask, request, render_template_string
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Image Background Remover</title></head>
<body>
    <h2>Upload Image</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <input type="submit" value="Remove Background">
    </form>
    {% if result_image %}
        <h3>Result:</h3>
        <img src="{{ result_image }}" alt="Output" style="max-width:400px;">
        <br><a href="{{ result_image }}" download="output.png">Download</a>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image = None
    if request.method == 'POST':
        image = request.files['image']
        input_image = Image.open(image.stream).convert("RGBA")
        output = remove(input_image)

        buffer = io.BytesIO()
        output.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        result_image = f"data:image/png;base64,{base64_img}"

    return render_template_string(HTML, result_image=result_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
