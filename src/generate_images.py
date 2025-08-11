import requests
import base64
from src.config import GEMINI_API_KEY, IMAGE_MODEL, IMAGE_SIZE
import time

def create_image(prompt: str, save_path: str, max_retries: int = 3, timeout: int = 10):
    """
    Generates an image from a prompt using Gemini REST API and saves it locally.
    Retries on failure up to max_retries times with timeout.

    Args:
        prompt (str): Text prompt for image generation.
        save_path (str): File path to save the generated image.
        max_retries (int): Maximum number of retries if request fails.
        timeout (int): Request timeout in seconds.
    """
    url = f"https://api.generative.googleapis.com/v1beta2/models/{IMAGE_MODEL}:generateImage"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    width, height = map(int, IMAGE_SIZE.lower().split('x'))

    json_data = {
        "prompt": prompt,
        "imageConfig": {
            "height": height,
            "width": width
        },
        "candidateCount": 1
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=json_data, timeout=timeout)
            response.raise_for_status()

            data = response.json()

            # Safety check: ensure keys exist
            if "results" not in data or not data["results"]:
                raise ValueError("No results in response JSON.")

            image_info = data["results"][0].get("image")
            if not image_info or "imageBytes" not in image_info:
                raise ValueError("Image bytes not found in response.")

            b64_image = image_info["imageBytes"]
            image_bytes = base64.b64decode(b64_image)

            with open(save_path, "wb") as f:
                f.write(image_bytes)

            print(f"✅ Image saved: {save_path}")
            break  # Success, exit retry loop

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"❌ Attempt {attempt} - Image generation failed for {save_path}: {e}")
            if attempt < max_retries:
                print(f"⏳ Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"⚠️ All {max_retries} attempts failed. Skipping image: {save_path}")
