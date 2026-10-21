"""Lesson 1.8: Business Helper Bot (Module 1 final).

Rule-based chatbot for KIPS tuition academy in Lahore. It answers common
questions, hands complaints to a human, and shows which questions it could not answer.
"""

BOT = "KIPS Bot"

# Example details for practice, not KIPS's real fees or timings. Replace them with the real ones
FEES = "Matric starts at 5,000 PKR per month. Intermediate starts at 8,000 PKR per month."
HOURS = "Classes run 3 pm to 8 pm, Monday to Saturday."
LOCATION = "We are in Lahore. Ask at the front desk for the exact branch address."
ADMISSION = "Admissions are open for Matric (class 9 and 10) and Intermediate (1st and 2nd year). Send your name, class and phone number and the front desk will call you."
SUBJECTS = "We teach Matric (class 9 and 10) and Intermediate (1st and 2nd year). Tell us your class and we will share the subject list."

print(f"{BOT}: Hi! Ask about fees, admission, timings, location or subjects. Type 'bye' to exit.")

# Memory: the bot remembers the name for the whole chat, so ask once, before the loop
name = input(f"{BOT}: What is your name? ").strip().title()
if name == "":
    name = "friend"
print(f"{BOT}: Nice to meet you, {name}!")

count = 0        # messages sent, to show the client how busy the bot is
unanswered = 0   # questions the rules could not answer: these show what to add next
complaints = 0   # complaints received, so the manager knows how many calls to make

while True:
    message = input(f"{name}: ").strip().lower()
    count += 1

    # Punctuation becomes a space, so "fee?" and "bye!" still count as the words "fee" and "bye"
    text = message.replace("?", " ").replace("!", " ").replace(",", " ").replace(".", " ").strip()

    # Spaces on both ends let a keyword match whole words only: " late " is in "is it late"
    # but not in "calculate". A space only before it (" price") also matches "prices"
    words = " " + text + " "

    if text == "bye" or text == "exit":
        print(f"{BOT}: Goodbye, {name}! Thanks for visiting KIPS.")
        break
    elif text == "":
        print(f"{BOT}: Please type a question.")
    # Handover first, so someone who asks for a person is never stuck talking to the bot.
    # Whole words only, because " human" would also match "humanities"
    elif " human " in words or " agent " in words:
        print(f"{BOT}: Connecting you to a human...")
        break
    # Complaints before the other rules, so an unhappy parent reaches the manager, not the fee reply
    elif " refund" in words or " complain" in words or " unhappy" in words or " delay" in words or " late " in words:
        complaints += 1
        print(f"{BOT}: Sorry about that. The academy manager will call you today.")
    # Fees before admission, so "admission fee" gets the fee reply. " fee " is a whole word
    # because " fee" would also match "feel" and "feedback"
    elif " fee " in words or " fees " in words or " price" in words or " cost" in words or " how much " in words:
        print(f"{BOT}: {FEES}")
    # Admission before timings, because "are admissions open?" contains "open"
    elif " admission" in words or " admit" in words or " enrol" in words or " register" in words or " join" in words:
        print(f"{BOT}: {ADMISSION}")
    elif " timing" in words or " time" in words or " hour" in words or " open" in words or " schedule" in words:
        print(f"{BOT}: {HOURS}")
    elif " where" in words or " location" in words or " address" in words or " branch" in words:
        print(f"{BOT}: {LOCATION}")
    elif " subject" in words or " course" in words or " matric" in words or " intermediate" in words or " class" in words:
        print(f"{BOT}: {SUBJECTS}")
    # Exact match for "hi", because "hi" is hiding inside words like "this" and "which"
    elif text == "hi" or text.startswith("hi ") or text.startswith("hello") or text.startswith("salam") or text.startswith("assalam"):
        print(f"{BOT}: Hello again, {name}! How can I help?")
    else:
        unanswered += 1
        prompt = f"You are the friendly assistant of KIPS tuition academy in Lahore. Answer in 2 lines: {message}"
        print(f"{BOT}: I am not sure yet. In Module 2, an AI will answer: {prompt}")

print("=" * 40)
print(f"Chat summary: {count} messages, {unanswered} unanswered.")
print(f"Complaints received: {complaints}")
