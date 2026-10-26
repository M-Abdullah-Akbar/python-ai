"""Lesson 2.3: Persona Bot with Real Facts.

A bakery assistant that answers from real business facts, switches personality
on command, and answers price questions straight from a dictionary.
Commands: /persona <name>, /price <item>, /add <item> <price>, bye.
"""

from langchain.chat_models import init_chat_model

# One config dictionary controls the bot, so every setting lives in one place
config = {"model": "llama3.2", "temperature": 0.3, "max_messages": 8}

# Example details for practice, not real prices, hours or phone number
facts = {
    "name": "Home Oven Bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "address": "Main Boulevard, Lahore",
    "phone": "0300 0000000",
    "delivery": "200 PKR, free from 3,000 PKR",
    "prices": {"cupcake": 250, "brownie": 300, "chocolate cake": 1500},
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, no jokes",
    "sales": "excited, always suggests one extra item to buy",
}

# Create the model once, before the loop, so every question reuses it
llm = init_chat_model(config["model"], model_provider="ollama", temperature=config["temperature"])

# Facts go into the system message so the AI does not invent prices or hours
rules = (
    f"You are the assistant of {facts['name']} in {facts['city']}. "
    f"Hours: {facts['hours']}. Address: {facts['address']}. Phone: {facts['phone']}. "
    f"Delivery: {facts['delivery']}. Prices in PKR: {facts['prices']}. "
    "Only use these facts. If you do not know, say you will check with the manager. "
    "Answer in 2 short lines."
)

style = personas["friendly"]
messages = [{"role": "system", "content": f"{rules} Your style: {style}."}]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, /add <item> <price>, bye")

while True:
    text = input("You: ").strip()
    command = text.lower()

    if command == "bye":
        print("Bot: Goodbye!")
        break
    elif text == "":
        print("Bot: Please type a question.")
    elif command.startswith("/persona "):
        name = command[9:].strip()
        # .get with a default, so a wrong persona name keeps the bot working instead of crashing
        style = personas.get(name, personas["friendly"])
        messages[0]["content"] = f"{rules} Your style: {style}."
        print(f"Bot: Style changed to: {style}")
    elif command.startswith("/price "):
        item = command[7:].strip()
        # Price questions are answered from the dictionary: free, instant and never wrong
        if item in facts["prices"]:
            print(f"Bot: {item.title()} costs {facts['prices'][item]} PKR.")
        else:
            print(f"Bot: Sorry, {item} is not on our menu.")
    elif command.startswith("/add "):
        rest = command[5:].strip()
        # The price is the last word, so the item name can have spaces, like "red velvet cake"
        space = rest.rfind(" ")
        item = rest[:space].strip()
        price_text = rest[space + 1:]

        if space == -1:
            print("Bot: Type /add, then the item and its price, like /add donut 200.")
        # isdigit() and a length limit before int(), so a wrong price never crashes the bot
        elif not price_text.isdigit() or len(price_text) > 6 or int(price_text) < 1:
            print("Bot: Please type the price as a whole number, like 200.")
        else:
            price = int(price_text)
            facts["prices"][item] = price

            # The prices changed, so rebuild the system message (same text as above),
            # or the AI would not know the new item
            rules = (
                f"You are the assistant of {facts['name']} in {facts['city']}. "
                f"Hours: {facts['hours']}. Address: {facts['address']}. Phone: {facts['phone']}. "
                f"Delivery: {facts['delivery']}. Prices in PKR: {facts['prices']}. "
                "Only use these facts. If you do not know, say you will check with the manager. "
                "Answer in 2 short lines."
            )
            messages[0]["content"] = f"{rules} Your style: {style}."
            print(f"Bot: Menu updated: {item.title()} is now {price} PKR.")
    elif text.startswith("/"):
        print("Bot: I did not understand that command. Use /persona <name>, /price <item>, /add <item> <price> or bye.")
    else:
        messages.append({"role": "user", "content": text})

        # Trim old messages, but always keep the system message first
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = llm.invoke(messages)
        answer = response.text

        # Save the reply too, or the bot forgets what it said, then trim again to stay short
        messages.append({"role": "assistant", "content": answer})
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        print(f"Bot: {answer}")
