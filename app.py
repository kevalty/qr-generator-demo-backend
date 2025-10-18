# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import qrcode
from io import BytesIO # To handle image data in memory

# Initialize Flask App
app = Flask(__name__)
CORS(app) # Allow frontend to connect

@app.route('/generate-qr', methods=['POST'])
def generate_qr_code():
    # Get data from the request body
    data_to_encode = request.json.get('data')
    if not data_to_encode:
        return jsonify({'error': 'Data is required'}), 400

    try:
        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_encode)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save image to a memory buffer
        img_buffer = BytesIO()
        img.save(img_buffer, 'PNG')
        img_buffer.seek(0) # Go to the start of the buffer

        # Return the image data directly in the response
        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=False # Display inline, not as download
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "QR Code Generator API is running!"}

# Run the server
if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on your network if needed
    app.run(host="0.0.0.0", port=5001, debug=True)