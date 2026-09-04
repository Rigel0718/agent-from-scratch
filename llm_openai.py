from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


MODEL = "gpt-5-mini"

response = client.responses.create(
    model=MODEL,
    instructions="You are a helpful assistant.",
    input="Hello",
)
# print(response.output_text)