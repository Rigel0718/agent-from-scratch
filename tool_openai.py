from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "read_file",
        "description": (
            "Reads the content of a file and returns it as a string. "
            "Read only text files. Do not read binary files."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to be read."
                },
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

history = [
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Please summarize the content of 'example.txt'."}
]

step = 0

while True:
    response = client.responses.create(
        model="gpt-5-mini",
        input=history,
        tools=TOOL_SCHEMAS,
        reasoning={"effort": "none"},
    )

    history.extend(response.output)

    # check for function calls in the response
    with open(f"test/response_{step}.json", "w", encoding="utf-8") as f:
        json.dump(
            response.model_dump(),
            f,
            indent=2,
            ensure_ascii=False,
        )

    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    if not tool_calls:
        print(response.output_text)
        break


    for tool_call in tool_calls:
        args = json.loads(tool_call.arguments)

        print(
            f"Tool called: {tool_call.name} "
            f"with arguments: {args}"
        )

        result = read_file(**args)

        history.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": result,
        })

    step += 1

print("MEMORIES", history)

    