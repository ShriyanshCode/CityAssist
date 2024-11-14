from flask import Flask, request, jsonify
import paddleocr
from paddleocr import PaddleOCR

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.route('/verify_aadhar', methods=['POST'])
def verify_aadhar():
    name_input = request.form.get("name")
    aadhaar_number_input = request.form.get("aadhaar_number")
    
    # Check if both name and Aadhaar number are provided
    if not name_input or not aadhaar_number_input:
        return jsonify({"error": "Name or Aadhaar number not provided"}), 400
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    image_file = request.files['image']
    
    image = image_file.read()

    #OCR
    results = ocr.ocr(image, cls=True)
    extracted_text = " ".join([line[1][0] for line in results[0]])
    
    # Basic checks for name and Aadhaar number 
    name_verified = name_input.lower() in extracted_text.lower()
    aadhaar_verified = aadhaar_number_input in extracted_text
    
    if name_verified and aadhaar_verified:
        return jsonify({"verification": "Verified"})
    else:
        return jsonify({"verification": "Failed"}), 400

if __name__ == '__main__':
    app.run(port=5001)
