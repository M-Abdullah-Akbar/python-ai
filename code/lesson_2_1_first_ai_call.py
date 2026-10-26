"""Lesson 2.1: AI Tutor.

Asks for a topic and a level, sends them to a local AI model through
LangChain, and prints the answer with its token count and time.
"""

from langchain.chat_models import init_chat_model

topic = input("Topic: ").strip()
level = input("Level (beginner or expert): ").strip()

# The system message sets the role, the length and the level, so every answer is short and fits the student
system = (
    f"You are a friendly tutor. Explain the topic only for a {level}, and do not mention any other level. "
    "Answer in exactly 3 short lines, one sentence per line."
)

# Low temperature keeps the explanation focused and factual instead of creative
tutor = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

response = tutor.invoke([
    {"role": "system", "content": system},
    {"role": "user", "content": topic},
])

# total_duration comes back in nanoseconds, so divide to get seconds
seconds = response.response_metadata["total_duration"] / 1_000_000_000
total_tokens = response.usage_metadata["total_tokens"]

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{total_tokens} tokens in {seconds:.1f} seconds")
