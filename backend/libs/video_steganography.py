import os
import shutil
import math
from subprocess import call, STDOUT
import cv2
from PIL import Image
from stegano import lsb


def split_string(message, parts=10):
    per_part = math.ceil(len(message) / parts)
    return [message[i:i + per_part] for i in range(0, len(message), per_part)]


def frame_extraction(video_path):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    print("[INFO] Extracting frames into temp directory...")
    vidcap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(f"temp/{count}.png", image)
        count += 1

    print(f"[INFO] Extracted {count} frames.")
    return count


def encode_message(message):
    parts = split_string(message)
    for i, part in enumerate(parts):
        frame_path = f"temp/{i}.png"
        if not os.path.exists(frame_path):
            print(f"[ERROR] Frame {frame_path} not found.")
            break
        try:
            img = Image.open(frame_path).convert("RGB")
            encoded_img = lsb.hide(img, part)
            encoded_img.save(frame_path)
            print(f"[INFO] Frame {i} encoded with part: {part}")
        except Exception as e:
            print(f"[ERROR] Failed to encode frame {frame_path}: {e}")


def merge_audio_video(output_file):
    if os.path.exists("temp/audio.mp3"):
        print("[INFO] Merging audio and video...")
        call(["ffmpeg", "-i", "temp/Embedded_Video.mp4", "-i", "temp/audio.mp3",
              "-codec", "copy", output_file, "-y"],
             stdout=open(os.devnull, "w"), stderr=STDOUT)
    else:
        print("[WARNING] No audio found. Saving silent stego video.")
        shutil.copy("temp/Embedded_Video.mp4", output_file)


def clean_temp():
    if os.path.exists("temp"):
        shutil.rmtree("temp")
        print("[INFO] Temp directory cleaned up.")


def encode_video(file_path, message):
    print("[INFO] Video Steganography ENCODING")

    if not message.strip():
        raise ValueError("[ERROR] Empty message passed.")

    total = frame_extraction(file_path)

    print("[INFO] Extracting audio from original video...")
    call(["ffmpeg", "-i", file_path, "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"],
         stdout=open(os.devnull, "w"), stderr=STDOUT)

    encode_message(message)

    print("[INFO] Generating video from stego frames...")
    call(["ffmpeg", "-framerate", "24", "-i", "temp/%d.png", "-vcodec", "libx264",
          "-pix_fmt", "yuv420p", "temp/Embedded_Video.mp4", "-y"],
         stdout=open(os.devnull, "w"), stderr=STDOUT)

    output_video = "Encoded_video.mp4"
    merge_audio_video(output_video)
    clean_temp()

    print(f"[✅] Stego video saved as: {output_video}")
    print("=" * 100)


def decode_video(file_path):
    print("[INFO] Video Steganography DECODING")

    total_frames = frame_extraction(file_path)
    if total_frames == 0:
        raise ValueError("[❌] No frames found to decode.")

    decoded_message = []
    for index in range(total_frames):
        frame_path = f"temp/{index}.png"
        if not os.path.exists(frame_path):
            break
        try:
            data = lsb.reveal(frame_path)
            if data:
                decoded_message.append(data)
        except Exception as e:
            print(f"[ERROR] Frame {index}: {e}")
            break

    clean_temp()

    if decoded_message:
        full_msg = ''.join(decoded_message)
        print("[*] The Encoded data was:\n")
        print(full_msg)
        print("=" * 100)
        return full_msg
    else:
        print("[❌] No hidden message found.")
        return ""
