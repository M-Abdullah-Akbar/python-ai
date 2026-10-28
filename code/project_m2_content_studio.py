"""Module 2 Checkpoint 1 Project: AI Content Studio.

Content studio for Home Oven Bakery in Lahore (example business).
/menu writes a description for every product, /post streams a social media post
in a chosen tone (plus a Roman Urdu version), /price answers from the data
without the AI, and any other text is a chat question answered from real facts
with memory. It ends with a session report of what the AI did.
"""

from langchain.chat_models import init_chat_model

# One config dictionary holds every setting, so changing the model or the memory size is a one-line edit
config = {
    "model": "llama3.2",
    "precise_temperature": 0.2,
    "creative_temperature": 0.8,
    "max_messages": 8,
    "cloud_price_per_1k": 0.5,  # PKR, example price for practice, not a real price list
}

# Example details for practice, not real prices, hours or phone number
facts = {
    "name": "Home Oven Bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "address": "Main Boulevard, Lahore",
    "phone": "0300 0000000",
    "delivery": "200 PKR, free from 3,000 PKR",
    "prices": {"chocolate cake": 1500, "cupcake": 250, "brownie": 300, "donut": 200, "mango tart": 0},
}

tones = {
    "fun": "playful and full of energy, short sentences",
    "premium": "elegant and calm, focused on quality",
    "urgent": "tells the reader to order today, with one clear call to action",
}

# Two models, created once at the top. Precise (low temperature) for facts and chat,
# creative (high temperature) for marketing text. Creating them inside the loop would reload them every time
precise = init_chat_model(config["model"], model_provider="ollama", temperature=config["precise_temperature"])
creative = init_chat_model(config["model"], model_provider="ollama", temperature=config["creative_temperature"])

# The facts go into the system message, so the AI quotes real prices and admits what it does not know
system = (
    f"You are the assistant of {facts['name']} in {facts['city']}. "
    f"Hours: {facts['hours']}. Address: {facts['address']}. Phone: {facts['phone']}. "
    f"Delivery: {facts['delivery']}. Prices in PKR: {facts['prices']}. "
    "A price of 0 means coming soon, not for sale yet. "
    "Only use these facts. If the answer is not here, say you do not know and a manager will confirm. "
    "Do not add up order totals and do not take payments. Answer in 2 short lines."
)
messages = [{"role": "system", "content": system}]

chat_answers = 0
menu_descriptions = 0
posts = 0
price_answers = 0
total_tokens = 0
total_seconds = 0

print("=" * 50)
print(f"   {facts['name']} AI Content Studio")
print("=" * 50)
print("Commands: /menu, /post fun|premium|urgent, /price <item>, /reset, bye")

while True:
    text = input("You: ").strip()
    command = text.lower()

    if command == "bye":
        print("Studio: Goodbye!")
        break
    elif text == "":
        print("Studio: Please type a command or a question.")
    elif command == "/reset":
        # Forget the chat but keep the rules, or the bot loses its facts
        messages = [messages[0]]
        print("Studio: Memory cleared.")
    elif command == "/menu":
        menu = []        # one dictionary per description, filled inside the loop
        menu_tokens = 0  # starts at 0 before the loop, or every round would reset it

        for item, price in facts["prices"].items():
            # A price of 0 means not for sale yet, so skip it BEFORE the AI call and spend nothing
            if price == 0:
                print(f"Studio: Skipping {item} (coming soon)")
                continue

            prompt = (
                f"Write one tempting sentence of at most 15 words that describes the taste and texture of '{item}' "
                "for a bakery menu. Start with a describing word, not a verb like Indulge or Enjoy. "
                "Do not mention the price, money or any shop name. Reply with the sentence only."
            )
            response = creative.invoke([{"role": "user", "content": prompt}])

            menu.append({"item": item, "price": price, "text": response.text.strip()})
            menu_tokens += response.usage_metadata["total_tokens"]
            total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

        print("-" * 50)
        for number, row in enumerate(menu, start=1):
            print(f"{number}. {row['item'].title()} ({row['price']:,} PKR)")
            print(f"   {row['text']}")
        print("-" * 50)

        # Bonus: what the same work would cost on a cloud model, using the example price in config
        cloud_cost = menu_tokens / 1000 * config["cloud_price_per_1k"]
        print(f"Studio: {len(menu)} descriptions, {menu_tokens} tokens. On a cloud model this would cost about {cloud_cost:.2f} PKR.")

        menu_descriptions += len(menu)
        total_tokens += menu_tokens
    elif command == "/post" or command.startswith("/post "):
        tone_name = command[5:].strip()
        # .get with a default, so a wrong tone name still gives a post instead of a KeyError
        style = tones.get(tone_name, tones["fun"])

        # Build the price list for the post from priced items only. The AI must never see a
        # coming-soon item, because a small model ignores "do not sell it" and advertises it anyway
        for_sale = {}
        for item, price in facts["prices"].items():
            if price == 0:
                continue
            for_sale[item] = price

        post_prompt = (
            f"Write a short social media post of 3 short lines for {facts['name']}, a bakery in {facts['city']}. "
            f"Style: {style}. Feature one item from this price list in PKR: {for_sale}. "
            f"Open {facts['hours']}. "
            "Use only these facts. Do not invent discounts, deadlines or offers. No hashtags. Reply with the post only."
        )

        print(f"Studio ({style}):")
        post = ""
        for chunk in creative.stream([{"role": "user", "content": post_prompt}]):
            print(chunk.text, end="", flush=True)
            post = post + chunk.text
            # Only one chunk, near the end, carries the token count and the time, so add them when it arrives.
            # The other chunks have no usage_metadata (None), which counts as False in an if
            if chunk.usage_metadata:
                total_tokens += chunk.usage_metadata["total_tokens"]
                total_seconds += chunk.response_metadata["total_duration"] / 1_000_000_000
        print()

        posts += 1

        # Bonus: the precise model translates, so the Roman Urdu stays close to the English post and adds no new claims
        urdu_prompt = (
            "Rewrite this social media post in Roman Urdu (Urdu written in English letters). "
            f"Keep the same facts and numbers and add nothing new. Reply with the post only.\n\n{post}"
        )
        urdu = precise.invoke([{"role": "user", "content": urdu_prompt}])
        print("Roman Urdu:")
        print(urdu.text.strip())

        total_tokens += urdu.usage_metadata["total_tokens"]
        total_seconds += urdu.response_metadata["total_duration"] / 1_000_000_000
    elif command == "/price" or command.startswith("/price "):
        item = command[6:].strip()

        # Prices are answered from the dictionary: free, instant and never wrong
        if item == "":
            print("Studio: Type /price and an item, like /price cupcake.")
        elif item in facts["prices"]:
            price = facts["prices"][item]
            if price == 0:
                print(f"Studio: {item.title()} is coming soon.")
            else:
                print(f"Studio: {item.title()} costs {price:,} PKR.")
            price_answers += 1
        else:
            print(f"Studio: Sorry, {item} is not on our menu.")
            price_answers += 1
    elif text.startswith("/"):
        print("Studio: I did not understand that command. Use /menu, /post <tone>, /price <item>, /reset or bye.")
    else:
        messages.append({"role": "user", "content": text})

        # Trim old messages, but always keep the system message first
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = precise.invoke(messages)
        answer = response.text.strip()

        # Save the reply too, or the bot forgets what it said, then trim again to stay short
        messages.append({"role": "assistant", "content": answer})
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        print(f"Studio: {answer}")
        print(f"        (memory: {len(messages)} messages, {response.usage_metadata['input_tokens']} tokens sent)")

        chat_answers += 1
        total_tokens += response.usage_metadata["total_tokens"]
        total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 50)
print("Session report")
print(f"Chat answers: {chat_answers} | Menu descriptions: {menu_descriptions} | Posts: {posts} | Price answers: {price_answers}")
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50)
