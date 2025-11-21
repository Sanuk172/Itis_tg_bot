from google import genai
from Api_key import *

client = genai.Client(api_key=GOOGLE_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Напиши задачу по математике для тренировки 19 номера егэ по математике с ответом, без форматирования"
)

print(response.text)
print(123)