from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


MODEL = "gpt-5-mini"

user_input = [
    {"role": "developer", "content": "you are a helpful assistant."},
    {"role": "user", "content": "What is the capital of Korea?"}
]

response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    input=user_input,
)

print(response.output_text)