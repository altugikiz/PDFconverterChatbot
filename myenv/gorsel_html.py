from google import genai
from google.genai import types
from api_read import GEMINI_API_KEY
import requests

client = genai.Client(api_key=GEMINI_API_KEY)
image_path = "https://image.hurimg.com/i/hurriyet/75/750x422/67b87da0081656cd37438b3e.jpg"
image = requests.get(image_path)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=["Görüntğdeki futbolcu kimdir?",
              types.Part.from_bytes(data=image.content, mime_type="image/jpg")])

print(response.text)