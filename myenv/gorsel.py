from google import genai
from google.genai import types
from api_read import GEMINI_API_KEY
import PIL.Image
client = genai.Client(api_key=GEMINI_API_KEY)
image = PIL.Image.open('myenv/nba.jpg')

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Bu resimde ne var?", image])

print(response.text)