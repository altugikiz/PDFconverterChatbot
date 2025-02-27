from google import genai
from api_read import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

myfile = client.files.upload(file=r'myenv\bdm_aciklama.m4a')

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents=[
    'bu ses klibini tanımla.',
    myfile,
  ]
)

print(response.text)