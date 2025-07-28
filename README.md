
# Project Title

A brief description of what this project does and who it's for


## Deployment

To deploy this project run

```bash
  npm run deploy
```
from flask import Flask, request, render_template_string
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Image Background Remover</title>
</head>
<body>
    <h1>Upload Image to Remove Background</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Remove Background</button>
    </form>

    {% if result_image %}
        <h2>Result:</h2>
        <img src="{{ result_image }}" alt="Result Image" style="max-width: 400px;" />
        <br><a href="{{ result_image }}" download="output.png">Download Image</a>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def remove_bg():
    result_image = None
    if request.method == 'POST':
        file = request.files['image']
        input_image = Image.open(file.stream).convert("RGBA")
        output_image = remove(input_image)

        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        result_image = f"data:image/png;base64,{base64_img}"

    return render_template_string(HTML_PAGE, result_image=result_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


