"""Lesson 2.2: Personal Tutor with Memory.

A chat tutor that remembers the conversation by keeping every message in a list.
Commands: /reset clears the memory, /count shows its size, bye exits.
"""

from langchain.chat_models import init_chat_model

MAX_MESSAGES = 8  # keep memory short so the chat stays fast and cheap

# Create the model once, before the loop, so every question reuses it
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.3)

# The system message is messages[0]: it sets the tutor's role and answer length for the whole chat
messages = [
    {"role": "system", "content": "You are a friendly tutor. Answer in 2 short lines."},
]
questions = []  # only the user's questions, for the summary when the chat ends

print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    text = input("You: ").strip()

    if text.lower() == "bye":
        print("Tutor: Goodbye!")
        if len(questions) > 0:
            print(f"Questions asked: {len(questions)}")
            print(f"First question: {questions[0]}")
            print(f"Last question: {questions[-1]}")
        break
    elif text.lower() == "/reset":
        # Forget the chat but keep the rules, or the tutor loses its role
        messages = [messages[0]]
        print("Tutor: Memory cleared.")
    elif text.lower() == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
    elif text == "":
        print("Tutor: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})
        questions.append(text)

        # Trim old messages, but always keep the system message first
        messages = [messages[0]] + messages[1:][-MAX_MESSAGES:]

        response = llm.invoke(messages)
        answer = response.text

        # Save the reply too, or the tutor forgets what it said. Trim again so memory
        # never holds more than the system message plus the newest MAX_MESSAGES
        messages.append({"role": "assistant", "content": answer})
        messages = [messages[0]] + messages[1:][-MAX_MESSAGES:]

        print(f"Tutor: {answer}")
        print(f"       (tokens sent: {response.usage_metadata['input_tokens']})")
