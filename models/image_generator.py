import requests
from config import settings


class ImageGenerator:
    def __init__(self):
        self.api_key = settings.stability_api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generate_image(self, prompt: str) -> bytes:
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*",
        }

        files = {"none": ''}
        data = {
            "prompt": prompt,
            "output_format": "png",
        }

        response = requests.post(self.base_url, headers=headers, files=files, data=data, timeout=60)

        if response.status_code != 200:
            raise RuntimeError(f"Image generation failed: {response.status_code} - {response.text}")

        return response.content