"""Lesson 2.4: Bot battle, rules vs AI.

Runs the same test questions through simple Lesson 1.8 style rules and through
the AI, prints both answers, and counts the questions the rules could not answer.
"""

from langchain.chat_models import init_chat_model

# Example details for practice, not real prices, hours or phone number
facts = {
    "name": "Home Oven Bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "delivery": "200 PKR, free from 3,000 PKR",
    "prices": {"cupcake": 250, "brownie": 300, "chocolate cake": 1500},
}

# Low temperature so the answers are repeatable, which is what you want when testing a bot.
# The model is created once, outside the loop
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

# The facts stop the AI from inventing prices and hours, so the battle is fair
system = (
    f"You are the assistant of {facts['name']} in {facts['city']}. "
    f"Hours: {facts['hours']}. Delivery: {facts['delivery']}. Prices in PKR: {facts['prices']}. "
    "Only use these facts. If you do not know, say you will check with the manager. "
    "Answer in 1 line."
)

questions = [
    "What are your hours?",
    "How much is a cupcake?",
    "Do you deliver?",
    "Do you have sugar-free cakes?",
    "Can I order a cake for 20 people?",
    "Is the brownie made with nuts?",
]

rule_misses = 0  # starts at 0 before the loop, so it counts across all the questions

for question in questions:
    text = question.lower()

    # The same kind of rules as Lesson 1.8: fixed keywords, fixed answers
    if "hour" in text or "open" in text:
        rule_answer = f"We are open {facts['hours']}."
    elif "price" in text or "how much" in text or "cost" in text:
        rule_answer = (
            f"Cupcake {facts['prices']['cupcake']} PKR, brownie {facts['prices']['brownie']} PKR, "
            f"chocolate cake {facts['prices']['chocolate cake']:,} PKR."
        )
    elif "deliver" in text:
        rule_answer = f"Delivery is {facts['delivery']}."
    else:
        rule_answer = "(no rule)"
        rule_misses += 1

    response = llm.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ])

    print(f"Q: {question}")
    print(f"   Rules: {rule_answer}")
    print(f"   AI:    {response.text.strip()}")

print("=" * 50)
print(f"Rules could not answer {rule_misses} of {len(questions)} questions.")
