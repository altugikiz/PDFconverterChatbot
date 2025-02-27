
from google import genai  # Yanlış!
from api_read import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

while True:
    soru = input("Soru: ")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=soru,
    )

    print(response.text)