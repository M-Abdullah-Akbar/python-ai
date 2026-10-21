"""Lesson 1.5: AI Model Profile Card.

Stores a model profile using str, int, float and bool, prints each value
with its type, and estimates the cost of a chat from the user's token count.
"""

model_name = "gemma3:1b"
context_window = 32768       # tokens, from `ollama show gemma3:1b`
price_per_1k_tokens = 0.5    # PKR, example price for practice, not a real price list
runs_locally = True

print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price_per_1k_tokens} PKR {type(price_per_1k_tokens)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# int() because input() always returns text, and we need to do maths with it
tokens_per_chat = int(input("Tokens per chat: "))

# Price is per 1000 tokens, so divide by 1000 first
chat_cost = tokens_per_chat / 1000 * price_per_1k_tokens

# round() because floats are not exact and money should show 2 decimals
print(f"Estimated cost: {round(chat_cost, 2)} PKR")

# Stretch: a monthly number is what clients ask for before they say yes
chats_per_day = int(input("Chats per day: "))
monthly_cost = chat_cost * chats_per_day * 30
print(f"Estimated monthly cost (30 days): {round(monthly_cost, 2)} PKR")
