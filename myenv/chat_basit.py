# Sohbeti hatırlasın
from google import genai
from api_read import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

chat = client.chats.create(model="gemini-2.0-flash")
response = chat.send_message("Evimde 2 adet köpek ve 1 tane de kedi var?")
print(response.text)
response = chat.send_message("Benim kaç tane kedim var?")
print(response.text)
for message in chat._curated_history:
    print(f'role - ', message.role, end=": ")
    print(message.parts[0].text)