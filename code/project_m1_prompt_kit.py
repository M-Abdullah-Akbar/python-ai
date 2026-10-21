"""AI Prompt Kit for a Local Business (Module 1, Checkpoint 1 Project).

Asks a small business owner five questions and prints four ready-to-use
AI prompts (marketing, customer service, growth, WhatsApp auto-reply).
The owner can paste them into Ollama, Claude or ChatGPT.

Built for local business owners who want AI help but don't know what to type.
"""

business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# int() because input() always returns text, and a budget must be a number
budget = int(input("Monthly budget (PKR): "))

# A fixed line keeps the header the same width, so the output looks tidy
line = "========================================="

print()
print(line)
print(f"   AI Prompt Kit for {business_name}")
print(line)

# Each prompt names a role, a task, the audience and a tone or number,
# because vague prompts get vague answers from the AI
marketing = f"""Write a short Instagram post for {business_name}, a {business_type} in {city}.
Target {customers}. Friendly, encouraging tone, 1 call to action to message us."""

# Asking the AI to apologise AND ask for details stops it from inventing the problem
service = f"""You are the manager of {business_name}, a {business_type} in {city}.
Write a polite reply, under 100 words, to an unhappy customer.
Apologise, ask what went wrong, and offer to fix it."""

# The budget goes into the prompt so the AI suggests ideas the owner can afford
growth = f"""Suggest 3 low-cost AI tools a {business_type} in {city} can use
to attract {customers} with a budget of {budget} PKR per month."""

# Bonus prompt: most small businesses in Pakistan talk to customers on WhatsApp
whatsapp = f"""You are the front-desk assistant of {business_name}, a {business_type} in {city}.
Write a friendly WhatsApp auto-reply, under 60 words, in simple English,
for {customers} who ask about fees, timings or admission.
Ask them to share their name, class and phone number."""

print("\n[1] Marketing")
print(marketing)

print("\n[2] Customer Service")
print(service)

print("\n[3] Growth")
print(growth)

print("\n[4] WhatsApp Auto-Reply")
print(whatsapp)
