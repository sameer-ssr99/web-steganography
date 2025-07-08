import os
import wave

def encode_audio(input_path, message, output_path):
    print("[INFO] Audio Steganography ENCODING\n")

    # Read audio
    song = wave.open(input_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    params = song.getparams()
    song.close()

    # Add end marker and convert message to binary
    message += '*^*^*'
    binary_data = ''.join(format(ord(char), '08b') for char in message)

    if len(binary_data) > len(frame_bytes):
        raise ValueError("[ERROR] Message too large to encode in this audio.")

    # Modify LSB of each byte
    for i in range(len(binary_data)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_data[i])

    # Save encoded audio
    with wave.open(output_path, 'wb') as stego:
        stego.setparams(params)
        stego.writeframes(frame_bytes)

    print("[INFO] Encoding complete.")
    print(f"[INFO] Location: {output_path}")
    print("=" * 100)

def decode_audio(file_path):
    print("[INFO] Audio Steganography DECODING\n")

    song = wave.open(file_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    song.close()

    # Extract LSBs
    extracted_bits = [str(byte & 1) for byte in frame_bytes]
    binary_data = ''.join(extracted_bits)
    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    decoded_message = ""
    for byte in all_bytes:
        char = chr(int(byte, 2))
        decoded_message += char
        if decoded_message.endswith("*^*^*"):
            break

    cleaned = decoded_message[:-5]  # remove marker
    print("[*] The Encoded data was:", cleaned)
    print("=" * 100)
    return cleaned
