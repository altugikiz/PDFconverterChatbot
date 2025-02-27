from google.genai import types,Client
from api_read import GEMINI_API_KEY
client = Client(api_key=GEMINI_API_KEY)

with open(r'myenv\bdm_aciklama.m4a', 'rb') as f:
    auido_bytes = f.read()

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents=[
    'Bu ses dosyanın içeriğini açıkla',
    types.Part.from_bytes(
      data=auido_bytes,
      mime_type='audio/aac',
    )
  ]
)

print(response.text)



