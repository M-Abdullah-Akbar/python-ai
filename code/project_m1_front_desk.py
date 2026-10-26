"""Module 1 Checkpoint 2 Project: AI Front Desk.

Front desk assistant for Home Oven Bakery in Lahore (example business).
It answers common questions with free rules, gives exact price quotes with
/quote, and turns every other question into a clean AI prompt with a model
and a cost estimate. It ends with a session report for the owner.
"""

BUSINESS_NAME = "Home Oven Bakery"
BOT_NAME = "Home Oven Desk"

# Example details for practice, not real prices, hours or phone number
CUPCAKE_PRICE = 250
BROWNIE_PRICE = 300
CHOCOLATE_CAKE_PRICE = 1500
OPENING_HOURS = "9 am to 10 pm, every day"
LOCATION = "Main Boulevard, Lahore"
SHOP_PHONE = "0300 0000000"

DISCOUNT_PERCENT = 10
DISCOUNT_MIN_QUANTITY = 10
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000

# Bigger orders need the owner, so the bot refuses to quote them
MAX_QUANTITY = 500

# Example cloud price for practice, not a real price list. qwen3:4b runs on this laptop,
# so it only stands in for a cheap cloud model and the cost below is an estimate
CLOUD_PRICE_PER_1K = 0.1  # PKR
LOCAL_MODEL = "gemma3:1b (local, private)"
CLOUD_MODEL = "qwen3:4b (stand-in for a cheap cloud model)"

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# Memory: the name is asked once, before the loop, so every reply and prompt can use it
name = input(f"{BOT_NAME}: What is your name? ").strip().title()
if name == "":
    name = "friend"

count = 0           # messages typed, for the report
unanswered = 0      # questions the rules could not answer: these show what to add next
quote_requests = 0  # times the customer asked for a quote
quotes = 0          # quotes that were calculated successfully
quoted_value = 0    # total PKR of those quotes
complaints = 0      # complaints received, so the owner knows how many calls to make
ai_cost = 0         # estimated PKR spent on the unanswered questions

while True:
    message = input(f"{name}: ").strip().lower()

    # Extra spaces would also end up inside the AI prompt, so squeeze them down to one
    while "  " in message:
        message = message.replace("  ", " ")

    # Punctuation becomes a space, so "late?" and "bye!" still match as whole words
    text = message.replace("?", " ").replace("!", " ").replace(",", " ").replace(".", " ").strip()
    while "  " in text:
        text = text.replace("  ", " ")

    # Spaces on both ends let " late " match the word "late" but not "chocolate"
    words = " " + text + " "

    # Greetings and goodbyes only count in a short message (3 words at most),
    # so "hi do you make wedding cakes" is still treated as a question
    short_message = text.count(" ") <= 2

    # "late" alone is not a complaint: "are you open late?" and "late night delivery?" are questions.
    # A missed exception only sends a harmless question to a manager, but a missed complaint is worse
    late_complaint = " late " in words and " open late" not in words and " late night" not in words and " till late" not in words and " until late" not in words

    # " deliver" alone would match "delivery" questions, so only the "not delivered" phrases count
    not_delivered = " not deliver" in words or " wasn't deliver" in words or " not arrive" in words or " never arrive" in words or " didn't arrive" in words

    is_complaint = " refund" in words or " complain" in words or " unhappy" in words or " delay" in words or late_complaint or not_delivered

    # An empty line is not a message, so it does not count in the report
    if text != "":
        count += 1

    if text == "exit" or (short_message and (" bye " in words or " goodbye " in words)):
        print(f"{BOT_NAME}: Goodbye, {name}!")
        break
    elif text == "":
        print(f"{BOT_NAME}: Please type a question.")
    # Complaints come before every other rule, so an unhappy customer always reaches a human
    elif is_complaint:
        complaints += 1
        # Someone who is unhappy and asks for a person should get the person at once
        if " human " in words or " agent " in words:
            print(f"{BOT_NAME}: Connecting you to a human...")
            break
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")
    elif " human " in words or " agent " in words:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break
    elif "/quote" in text or " quote" in words:
        quote_requests += 1
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # "in" so that "cupcakes" and "chocolate cakes" work too
        wants_cupcake = "cupcake" in item
        wants_brownie = "brownie" in item
        # A bare "cake" means the chocolate cake, the only cake on the menu. "wedding cake" is not on the menu
        wants_cake = "chocolate cake" in item or item == "cake" or item == "cakes" or item == "chocolate"

        price = 0
        if wants_cupcake:
            item_name = "cupcake"
            price = CUPCAKE_PRICE
        elif wants_brownie:
            item_name = "brownie"
            price = BROWNIE_PRICE
        elif wants_cake:
            item_name = "chocolate cake"
            price = CHOCOLATE_CAKE_PRICE

        # Two items in one answer would be billed as only the first one, so ask for them one at a time
        two_items = (wants_cupcake and wants_brownie) or (wants_cupcake and wants_cake) or (wants_brownie and wants_cake) or " and " in item or "," in item or "&" in item

        if item == "":
            print(f"{BOT_NAME}: Please type an item name.")
        elif two_items:
            print(f"{BOT_NAME}: Please ask for one item at a time, then type /quote again for the next one.")
        elif price == 0:
            print(f"{BOT_NAME}: Sorry, {item} is not on our menu. We have cupcake, brownie and chocolate cake.")
        # isdigit() before int(), because int("abc") would crash the whole bot
        elif not quantity_text.isdigit():
            print(f"{BOT_NAME}: Please type the quantity as a whole number, like 12.")
        # len() is checked first, so int() never has to read a huge text
        elif len(quantity_text) > 9 or int(quantity_text) > MAX_QUANTITY:
            print(f"{BOT_NAME}: Orders above {MAX_QUANTITY} items need the owner. Type human to talk to someone.")
        elif int(quantity_text) < 1:
            print(f"{BOT_NAME}: Please order at least 1.")
        else:
            quantity = int(quantity_text)
            subtotal = price * quantity

            # Discount first, because delivery is judged on the amount the customer really pays
            if quantity >= DISCOUNT_MIN_QUANTITY:
                discount = subtotal * DISCOUNT_PERCENT // 100
                discount_text = f"-{discount:,}"
            else:
                discount = 0
                discount_text = "0"
            after_discount = subtotal - discount

            if after_discount >= FREE_DELIVERY_LIMIT:
                delivery = 0
            else:
                delivery = DELIVERY_FEE
            total = after_discount + delivery

            quotes += 1
            quoted_value += total
            print(f"{BOT_NAME}: {quantity} x {item_name} = {subtotal:,} PKR")
            print(f"     Discount: {discount_text} PKR | Delivery: {delivery:,} PKR")
            print(f"     Total: {total:,} PKR")
    elif " deliver" in words:
        print(f"{BOT_NAME}: Delivery is {DELIVERY_FEE} PKR, and free when your order is {FREE_DELIVERY_LIMIT:,} PKR or more after any discount.")
    elif " price" in words or " cost" in words or " how much " in words or " menu" in words:
        print(f"{BOT_NAME}: Cupcake {CUPCAKE_PRICE} PKR, brownie {BROWNIE_PRICE} PKR, chocolate cake {CHOCOLATE_CAKE_PRICE:,} PKR. {DISCOUNT_PERCENT}% off for {DISCOUNT_MIN_QUANTITY} or more items. Type /quote for an exact total.")
    # No " time" here: "what time will my cake be ready" is not a question about opening hours
    elif " hour" in words or " open" in words or " timing" in words or " close " in words or " closing" in words or " closed" in words:
        print(f"{BOT_NAME}: We are open {OPENING_HOURS}.")
    # Only phrases about the shop: "where is my order" and "change my address" must not get the shop address
    elif " where are you" in words or " where is your" in words or " your location" in words or " your address" in words or " branch" in words or text == "location" or text == "address":
        print(f"{BOT_NAME}: We are on {LOCATION}.")
    # Answered by a rule, so a question about the shop's phone never reaches the AI to be invented
    elif " your phone" in words or " your number" in words or " contact" in words:
        print(f"{BOT_NAME}: You can call or WhatsApp us on {SHOP_PHONE}.")
    # Greetings only at the start of a short message, because "hi" is hiding inside "which" and "this"
    elif short_message and (text == "hi" or text.startswith("hi ") or text.startswith("hello") or text.startswith("salam") or text.startswith("assalam")):
        print(f"{BOT_NAME}: Hello again, {name}! How can I help?")
    else:
        unanswered += 1

        # Cut long questions, because every extra token costs money
        question = message.capitalize()[:150]

        # The facts stop the AI from inventing prices and timings
        prompt = f"""You are the assistant of {BUSINESS_NAME}.
Facts: cupcake {CUPCAKE_PRICE} PKR, brownie {BROWNIE_PRICE} PKR, chocolate cake {CHOCOLATE_CAKE_PRICE:,} PKR. Open {OPENING_HOURS}. Delivery {DELIVERY_FEE} PKR, free from {FREE_DELIVERY_LIMIT:,} PKR.
Use only these facts. If the answer is not here, say you do not know and a manager will call.
Answer {name} in 2 short lines. Question: {question}"""

        # Count the whole prompt, because that is what the model really reads and what costs money
        tokens = round(len(prompt) / 4)

        # Private details must never leave the shop, so they go to the local model.
        # Missing one leaks data, but a false alarm only costs a local run, so the word list is wide
        digits_only = text.replace("-", "").replace(" ", "").replace("+", "").isdigit()
        if " phone" in words or " mobile" in words or " number" in words or " cnic" in words or " email" in words or " address" in words or " password" in words or digits_only or " 03" in words or " +92" in words:
            model = LOCAL_MODEL
            cost = 0
        else:
            model = CLOUD_MODEL
            cost = tokens / 1000 * CLOUD_PRICE_PER_1K
        ai_cost += cost

        indented_prompt = prompt.replace("\n", "\n     ")
        print(f"{BOT_NAME}: Good question! Routed to: {model} (~{tokens} tokens)")
        print(f"     Prompt: {indented_prompt}")

# Everything that was not a quote request or an unanswered question was answered by a rule
answered_by_rules = count - unanswered - quote_requests

print("=" * 50)
print("Session report")
print(f"Messages: {count} | Answered by rules: {answered_by_rules} | Unanswered: {unanswered}")
print(f"Quotes: {quotes} | Quoted value: {quoted_value:,} PKR")
print(f"Complaints: {complaints}")
print(f"Estimated AI cost for unanswered questions: {ai_cost:.4f} PKR")
print("=" * 50)
