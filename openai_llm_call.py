from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

MODEL = "gpt-5-mini"

def call_openai_model(user_input, raw_response=False, tools=None):
    request = {
        "model": MODEL,
        "reasoning": {"effort": "none"},
        "input": user_input,
    }
    if tools is not None:
        request["tools"] = tools

    response = client.responses.create(
        **request,
    )
    if raw_response:
        return response
    
    return response.output_text
