
from flask import Flask, request, jsonify
import openai
import base64
from PIL import Image
from io import BytesIO
import fitz  # PyMuPDF
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
from flasgger import Swagger, swag_from

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

Swagger(app, config=swagger_config)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_images_from_pdf(pdf_file):
    images = []
    pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in pdf_doc:
        pix = page.get_pixmap()
        img_data = BytesIO(pix.tobytes("png"))
        images.append(Image.open(img_data))
    return images

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route("/analyze", methods=["POST"])
@swag_from({
    'summary': 'Analyze Medical Report (PDF/Image)',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'PDF or image file of the medical report'
        }
    ],
    'responses': {
        200: {
            'description': 'Summary of medical report in plain language',
            'examples': {
                'application/json': {
                    'summary': 'This report shows mild anemia with low hemoglobin...'
                }
            }
        },
        400: {
            'description': 'No file uploaded or invalid request'
        },
        500: {
            'description': 'Server error or OpenAI issue'
        }
    }
})
def analyze_medical_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    images = []

    if file.filename.lower().endswith(".pdf"):
        images = extract_images_from_pdf(file)
    else:
        image = Image.open(file.stream).convert("RGB")
        images = [image]

    try:
        all_summaries = []
        for img in images:
            b64_img = image_to_base64(img)
            vision_response = openai.ChatCompletion.create(
                model="gpt-4-turbo-2024-04-09",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Explain this medical report in simple language for a patient."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            summary = vision_response["choices"][0]["message"]["content"]
            all_summaries.append(summary)

        return jsonify({"summary": "\n\n".join(all_summaries)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
