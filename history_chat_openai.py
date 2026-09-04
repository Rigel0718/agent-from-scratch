from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

MODEL = "gpt-5-mini"

message_history = [
    {"role": "developer", "content": "you are a helpful assistant."},
]

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break
    message_history.append({"role": "user", "content": user_input})

    response = client.responses.create(
        model=MODEL,
        input=message_history,
    )

    assistant_reply = response.output_text
    print(f"Assistant: {assistant_reply}")

    message_history.append({"role": "assistant", "content": assistant_reply})