from google import genai
from api_read import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print('My files:')
for f in client.files.list():
  print(" ", f'{f.name}: {f.uri}', f'{f.state.name}')