from openai_llm_call import call_openai_model

message_history = [
    {"role": "developer", "content": "you are a helpful assistant."},
]

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break
    message_history.append({"role": "user", "content": user_input})

    assistant_reply = call_openai_model(message_history)
    print(f"Assistant: {assistant_reply}")

    message_history.append({"role": "assistant", "content": assistant_reply})
