import os
import cv2
from PIL import Image
import numpy as np

# Convert string data to binary format
def data2binary(data):
    return ''.join([format(ord(i), '08b') for i in data])

# Add data to the image pixels
def hide_data(img, data):
    data += "|||END|||"
    b_data = data2binary(data)
    data_len = len(b_data)
    data_index = 0

    for row in img:
        for pix in row:
            for i in range(3):  # for R, G, B
                if data_index < data_len:
                    pix[i] = (pix[i] & 0b11111110) | int(b_data[data_index])
                    data_index += 1
    return img

# Extract the hidden binary data from the image
def find_data(img):
    bin_data = ""
    for row in img:
        for pix in row:
            for i in range(3):
                bin_data += str(pix[i] & 1)

    all_bytes = [bin_data[i:i + 8] for i in range(0, len(bin_data), 8)]
    readable_data = ""
    for byte in all_bytes:
        readable_data += chr(int(byte, 2))
        if "|||END|||" in readable_data:
            break
    return readable_data.split("|||END|||")[0]  # return only message

# Encode message into image and save
def encode_image(input_path, message, output_path):
    image = cv2.imread(input_path)
    if image is None:
        raise FileNotFoundError(f"[ERROR] File '{input_path}' not found.")

    img_pil = Image.open(input_path)
    w, h = img_pil.size

    encoded_image = hide_data(image, message)
    temp_path = "temp.png"
    cv2.imwrite(temp_path, encoded_image)

    resized = Image.open(temp_path)
    resized = resized.resize((w, h), Image.Resampling.LANCZOS)
    resized.save(output_path)

    img_pil.close()
    resized.close()
    os.remove(temp_path)

# Decode hidden message from image
def decode_image(file_path):
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError(f"[ERROR] File '{file_path}' not found.")
    return find_data(image)
