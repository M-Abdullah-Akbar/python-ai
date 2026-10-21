"""Lesson 1.6: Prompt Cleaner.

Cleans a messy name and question, estimates tokens and cost, checks if the
question mentions Python, and builds a safe, short prompt for an AI model.
"""

raw_name = input("Your name: ")
raw_question = input("Your question: ")

# Users add extra spaces and random capitals; clean them before the text goes to an AI
clean_name = raw_name.strip().title()
clean_question = raw_question.strip().capitalize()

# Lowercase before replacing so "SHIT" and "Stupid" match too, then capitalize again.
# Short words like "ass" are left out on purpose: they would also hit "class" and "assistant"
filtered = clean_question.lower()
filtered = filtered.replace("stupid", "***")
filtered = filtered.replace("idiot", "***")
filtered = filtered.replace("dumb", "***")
filtered = filtered.replace("shit", "***")
filtered = filtered.replace("damn", "***")
filtered = filtered.replace("fuck", "***")
clean_question = filtered.capitalize()

# Rule of thumb: 1 token is about 4 characters of English text
characters = len(clean_question)
estimated_tokens = round(characters / 4)

# Example price for practice, not a real price list
price_per_1k_tokens = 0.5  # PKR
estimated_cost = estimated_tokens / 1000 * price_per_1k_tokens

# lower() so "Python", "PYTHON" and "python" all match
mentions_python = "python" in clean_question.lower()

# Slicing keeps the prompt short, so a very long question cannot run up the token bill
short_question = clean_question[:150]

prompt = f"""You are a friendly Python tutor.
Greet {clean_name} by name and answer in 3 short lines.
Question: {short_question}"""

print("=" * 40)
print(f"Cleaned question: {clean_question}")
print(f"Characters: {characters}, about {estimated_tokens} tokens")
print(f"Estimated cost: {estimated_cost:.2f} PKR")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)
print(prompt)
