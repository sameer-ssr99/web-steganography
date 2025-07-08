from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os

from libs.image_steganography import encode_image, decode_image
from libs.audio_steganography import encode_audio, decode_audio
from libs.text_steganography import encode_text, decode_text
from libs.video_steganography import encode_video, decode_video

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process():
    mode = request.form.get('mode')
    media = request.form.get('media')
    file = request.files.get('file')
    message = request.form.get('message', '')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    try:
        if mode == 'encode':
            if media == 'image':
                output_path = os.path.join(PROCESSED_FOLDER, f'stego_{filename}')
                encode_image(input_path, message + '|||END|||', output_path)
                return send_file(output_path, as_attachment=True)

            elif media == 'audio':
                output_path = os.path.join(PROCESSED_FOLDER, f'stego_{filename}')
                encode_audio(input_path, message + '|||END|||', output_path)
                return send_file(output_path, as_attachment=True)

            elif media == 'text':
                output_path = encode_text(input_path, message + '|||END|||')
                return send_file(output_path, as_attachment=True)

            elif media == 'video':
                encode_video(input_path, message + '|||END|||')
                return send_file("Encoded_video.mp4", as_attachment=True)

        elif mode == 'decode':
            if media == 'image':
                print("[DEBUG] Image decode requested for:", input_path)
                secret = decode_image(input_path)
                print("[DEBUG] Decoded message:", secret)
                return jsonify({'message': secret})

            elif media == 'audio':
                secret = decode_audio(input_path)
                return jsonify({'message': secret.split('|||END|||')[0] if '|||END|||' in secret else secret})

            elif media == 'text':
                secret = decode_text(input_path)
                return jsonify({'message': secret.split('|||END|||')[0] if '|||END|||' in secret else secret})

            elif media == 'video':
                secret = decode_video(input_path)
                return jsonify({'message': secret.split('|||END|||')[0] if '|||END|||' in secret else secret})

        return jsonify({'error': 'Invalid mode or media'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

