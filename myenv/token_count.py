from google import genai
from api_read import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)
myfile = client.files.get(name="wlvvj4iuu4gs")
response = client.models.count_tokens(
    model="gemini-2.0-flash",
    contents=[myfile]
)

print(response)