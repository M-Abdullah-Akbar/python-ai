# Module 2 Checkpoint 1 Project: AI Test Results

**Business:** Home Oven Bakery, a bakery in Lahore. The name, prices, hours and phone number are examples for practice.
**Models:** `llama3.2` for both the precise model (temperature 0.2) and the creative model (temperature 0.8), running locally with Ollama.

I ran the studio on the real model in two ways. A test script typed the lines for the scripted sessions, so those are not live terminals. One session I typed myself in my own terminal, and it is shown in `docs/project-m2-cp1-run.png`.

## AI quality test: three chat questions

I asked the three questions in a fresh scripted session, so the memory was empty at the start. The chat uses the precise model, with the real facts in the system message.

### 1. A question the facts answer: the hours

**Question:** `What are your opening hours?`
**Answer:** We are open from 9 am to 10 pm every day.
**Judgement:** Correct. It matches the facts exactly and adds nothing. My live session gave the same answer.

### 2. A question about a price

**Question:** `How much is a brownie?`
**Answer:** A brownie costs 300 PKR.
**Judgement:** Correct. 300 PKR is the price in the facts. (`/price brownie` gives the same answer without the AI.)

### 3. A question the facts cannot answer

**Question:** `Do you sell pizza?`
**Answer:** No, we do not have pizza on our menu. (In my live session: "No, we don't have pizza on our menu.")
**Judgement:** No hallucination. Pizza is not on the price list, and the model invented no price, offer or promise. The system message asks it to say it does not know and that a manager will confirm, and it said a plain "no" instead. That is a fair answer here, because the price list is the whole menu. An earlier run gave "No, we do not have information about selling pizza.", so the wording changes from run to run, even at temperature 0.2.

## Best `/post` and best tone

**Best post (fun tone), from my live session, shown in the screenshot.** The words appeared gradually in my terminal, so the streaming works.

> "Sweet tooth alert! Get your cake fix at Home Oven Bakery - try our rich chocolate cake for just PKR 1500! Open 9 am to 10 pm daily, so satisfy your cravings anytime!"

**Which tone worked best for my business: fun, and why.** It features one item with its real price and the real opening hours, and it invents no discount, deadline or stock level. It is also the only one of the three that does not start with the word "Indulge". The other two tones, from a scripted run of the final code, were weaker:

- **Premium** is the longest of the three. "Made with love and care" and "the finest treats" are claims that are not in my data, and they could describe any bakery.
- **Urgent** has a clear call to action ("Order now", "Visit us today"), but the rest is filler like "a sweet delight".

This is my judgement from a few runs. The creative model runs at 0.8, so another run will word things differently.

## Other findings

- **The coming-soon item.** In my first real run, the urgent post advertised "our famous mango tart ... at an unbeatable price of PKR 0". The prompt said not to sell it, and the model ignored that. I changed the code so the post prompt lists priced items only. In the final code, I read the urgent post, the premium post and the fun post from my screenshot, and none of them mentions the mango tart. A rule in code worked where a rule in the prompt did not.
- **Roman Urdu bonus.** Across my four real runs (three scripted, one live), 9 of the 11 Roman Urdu versions were an exact copy of the English post. Only 2 were written in Roman Urdu. One of those was garbled: "Meethay cheezen ki barf" and "khana khana karein" make no sense to me. The other is the one in my screenshot. It keeps the numbers (1500 PKR, 9 am to 10 pm), but some phrases look wrong to me. For example "Meetha saanskar alart" is meant to be "sweet tooth alert", and I do not think "saanskar" means tooth. A native Urdu speaker should check my reading. `llama3.2` cannot be trusted for Roman Urdu, so a real client would need a stronger model or a human to check it.
- **Menu descriptions.** In my live session, three of the four start with "Rich" or "Richly", and all four use "velvet" or "velvety". They also add details that are not in my data, such as "rich velvet cake" for the cupcake and "freshly baked" for the donut. The owner would need to check them.
- **Menu cost estimate bonus.** `/menu` used 436 tokens in my live session. At the example price of 0.5 PKR per 1K tokens, the studio printed a cloud cost of about 0.22 PKR.
- **Speed.** My live session made 8 AI calls (4 menu descriptions, 1 post and its Roman Urdu version, 2 chat answers). The report said 1,232 tokens in 224.4 seconds, a bit under 4 minutes. A scripted run of two posts (4 calls) took 198.3 seconds, so the posts are the slow part: a post is a long creative answer, and the Roman Urdu step adds a second call. I did not time `/menu` alone.
