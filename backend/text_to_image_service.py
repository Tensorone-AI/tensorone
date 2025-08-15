import requests
import io
import math
import random
from typing import Union


class TextToImageService:
    def __init__(self):
        # Dezgo API configuration
        self.dezgo_base_url = "https://api.dezgo.com"
        # Note: API key should be moved to environment variables for production
        self.api_key = "API_KEY"
        self.headers = {
            "X-Dezgo-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def generate_random_dimension(self) -> int:
        """
        Generate random dimension following the specified formula:
        (Math.floor(Math.random() * (1024 / 8 - 320 / 8 + 1)) + 320 / 8) * 8
        """
        min_val = 320 // 8  # 40
        max_val = 1024 // 8  # 128
        random_val = math.floor(random.random() * (max_val - min_val + 1)) + min_val
        return random_val * 8

    def generate_image(self, prompt: str, width: Union[str, int], height: Union[str, int]) -> dict:
        """
        Generate image using Dezgo API with Flux model.

        Args:
            prompt: Text prompt for image generation
            width: Width in pixels or 'random' for random width
            height: Height in pixels or 'random' for random height

        Returns:
            Dict containing image data or error message
        """
        try:
            # Handle random dimensions
            if width == 'random':
                width = self.generate_random_dimension()
            else:
                width = int(width)

            if height == 'random':
                height = self.generate_random_dimension()
            else:
                height = int(height)

            # Validate dimensions
            if width < 320 or width > 1024 or height < 320 or height > 1024:
                return {"error": "Width and height must be between 320 and 1024 pixels"}

            # Ensure dimensions are multiples of 8
            if width % 8 != 0 or height % 8 != 0:
                return {"error": "Width and height must be multiples of 8"}

            # Prepare API request
            url = f"{self.dezgo_base_url}/text2image_flux"

            payload = {
                "prompt": prompt,
                "model": "flux_1_schnell",
                "width": width,
                "height": height,
                "format": "png"
            }

            # Make API request
            response = requests.post(url, json=payload, headers=self.headers, timeout=60)

            if response.status_code == 200:
                # Return image data as bytes
                image_buffer = io.BytesIO(response.content)
                image_buffer.seek(0)
                return {
                    "success": True,
                    "image": image_buffer,
                    "width": width,
                    "height": height,
                    "prompt": prompt
                }
            else:
                try:
                    error_data = response.json()
                    return {"error": f"Dezgo API error: {error_data.get('message', 'Unknown error')}"}
                except:
                    return {"error": f"Dezgo API error: HTTP {response.status_code}"}

        except requests.exceptions.Timeout:
            return {"error": "Request timeout - image generation took too long"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except ValueError as e:
            return {"error": f"Invalid dimension value: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
