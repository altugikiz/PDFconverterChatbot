from google import genai  # Doğru!
from api_read import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Merhaba!",
)

print(response.text)