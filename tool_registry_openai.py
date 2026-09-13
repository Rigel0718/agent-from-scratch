import json

from openai_llm_call import call_openai_model
from tool_openai import read_file, TOOL_SCHEMAS


TOOL_REGISTRY = {
    "read_file": read_file,
}

MAX_STEPS = 5

response_history = [
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Please summarize the content of 'example.txt'."}
]

steps = 0

while steps < MAX_STEPS:
    response = call_openai_model(
        response_history,
        raw_response=True,
        tools=TOOL_SCHEMAS,
    )

    response_history.extend(response.output)

    # check for function calls in the response
    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    if not tool_calls:
        print(response.output_text)
        break

    for tool_call in tool_calls:

        print(
            f"Tool called: {tool_call.name} "
            f"with arguments: {tool_call.arguments}"
        )
        try:
            args = json.loads(tool_call.arguments)
        except json.JSONDecodeError as e:
            result = (
                f"Invalid tool arguments:"
                f"{type(e).__name__} : {e}, "
            )
        else:
            tool_function = TOOL_REGISTRY.get(tool_call.name)

            if tool_function is None:
                raise ValueError(
                    f"Tool '{tool_call.name}' is not registered."
                )

            try:
                result = tool_function(**args)

            except TypeError as e:
                result = (
                    f"Invalid tool arguments: "
                    f"{type(e).__name__}: {e}"
                )

            except Exception as e:
                result = (
                    f"Tool execution failed: "
                    f"{type(e).__name__}: {e}"
                )

        response_history.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": result,
        })

    steps += 1
else:
    raise RuntimeError(
        f"Exceeded maximum number of steps ({MAX_STEPS}) without reaching a final response."
    )