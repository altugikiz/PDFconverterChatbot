from google import genai
from google.genai import types
from api_read import GEMINI_API_KEY
import pathlib
import PIL.Image

image_path_1 = "myenv/ufc5.jpg"  # Replace with the actual path to your first image
image_path_2 = "myenv/fifa25.jpg" # Replace with the actual path to your second image
image_path_3='myenv/nba.jpg'
#image_url_1 = "https://goo.gle/instrument-img" # Replace with the actual URL to your third image

pil_image = PIL.Image.open(image_path_1)

b64_image = types.Part.from_bytes(
    data=pathlib.Path(image_path_2).read_bytes(),
    mime_type="image/jpg"
)
pil_image3 = PIL.Image.open(image_path_3)

#downloaded_image = requests.get(image_url_1)

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Resimlerdeki ortak noktaları ve farklılıkları söyle",
              pil_image, b64_image, pil_image3])

print(response.text)