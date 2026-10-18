"""Lesson 1.4: Business Prompt Builder.
Asks the user for business details and builds a ready-to-use AI prompt.
"""

name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")

# int() because input() always returns text, and a budget must be a number
budget = int(input("Monthly budget (PKR): "))

print(f"\nWelcome, {name}!")

# One f-string keeps the prompt in a single place, so we can send it to an LLM later
prompt = (
    f"Suggest 3 AI solutions for a {business} that struggles with {problem}. "
    f"Budget: {budget} PKR per month."
)

print("--- Your AI Prompt ---")
print(prompt)
