from google import genai
from api_read import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# Upload a file
poem_file = client.files.upload(file="myenv\siir.txt")

# Files will auto-delete after a period.
print('Son kullanim',poem_file.expiration_time)

prompt="Bu şiir kime ait?"
response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents=[
    prompt,
    poem_file
  ]
)

print(response.text)

# Or they can be deleted explicitly.
dr = client.files.delete(name=poem_file.name)

try:
  client.models.generate_content(
      model="gemini-2.0-flash-exp",
      contents=['Finish this poem:', poem_file])
except genai.errors.ClientError as e:
  print(e.code)  # 403
  print(e.status)  # PERMISSION_DENIED
  print(e.message)  # You do not have permission to access the File .. or it may not exist.