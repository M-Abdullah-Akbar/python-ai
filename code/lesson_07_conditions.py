"""Lesson 1.7: Smart Model Router.

Picks the right AI model for a task, warns about long requests, and
estimates the cost, like an agent choosing which tool to use.
"""

task = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))

# Check bad input first, so a typo cannot pick the wrong model or give a negative cost
if task != "code" and task != "private" and task != "chat":
    print("Unknown task type. Please type code, private or chat.")
elif tokens <= 0:
    print("Tokens must be more than 0.")
else:
    # Anything except "yes" counts as a free user, so a typo can never give free access
    paid = input("Is this a paid user? (yes/no): ").strip().lower()

    # Private data must never leave the laptop, so check it first
    if task == "private":
        model = "gemma3:1b (local, Ollama)"
        price = 0  # local model runs on my laptop, so it costs nothing per token
    elif task == "code":
        model = "claude (cloud, strong at code)"
        price = 0.8  # PKR per 1K tokens, example price for practice, not a real price list
    else:
        model = "small cloud model (cheap for chat)"
        price = 0.2  # PKR per 1K tokens, example price for practice

    cost = tokens / 1000 * price

    # Very long requests cost more, so warn before sending
    if tokens > 4000:
        print("Warning: long request, consider shortening it.")
    else:
        print("Length is fine.")

    if paid != "yes" and tokens > 2000:
        print("Upgrade to send long requests.")

    print(f"Chosen model: {model}")
    print(f"Estimated cost: {cost:.2f} PKR")
