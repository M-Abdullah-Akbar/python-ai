# Module 1 Checkpoint 2 Project: AI Test Results

**Business:** Home Oven Bakery, a bakery in Lahore. The name, prices and hours are examples for practice.
**Models:** `gemma3:1b` for the private question and `qwen3:4b` for the cloud-routed question. Both run locally with Ollama. `qwen3:4b` only stands in for a cheap cloud model.

I took each prompt exactly as the Front Desk printed it and sent it to the model through Ollama's local API. The prompt includes the bakery's menu, hours and delivery facts and the instruction to use only those facts.

## AI test 1: Private question (routed to the local model)

**Customer question:** `can I change my phone number on the order?`
**Routed to:** gemma3:1b (local, private), about 90 tokens, estimated cost 0 PKR. The model took 20 seconds.

**Prompt:**

```text
You are the assistant of Home Oven Bakery.
Facts: cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR. Open 9 am to 10 pm, every day. Delivery 200 PKR, free from 3,000 PKR.
Use only these facts. If the answer is not here, say you do not know and a manager will call.
Answer Ali Raza in 2 short lines. Question: Can i change my phone number on the order?
```

**AI answer:**

```text
I do not know. Please call a manager to confirm phone number changes.
```

**Useful?** Yes, mostly. It admitted that it does not know and invented no prices, hours or promises. Two small problems: it gave one line, not two, and it told the customer to call a manager, while the prompt said that a manager will call the customer. A real owner would want to fix that wording.

## AI test 2: Normal question (routed to the cloud stand-in)

**Customer question:** `Do you make sugar-free cakes?`
**Routed to:** qwen3:4b (stand-in for a cheap cloud model), about 87 tokens, estimated cost 0.0087 PKR. The model took 281 seconds on my laptop.

**Prompt:**

```text
You are the assistant of Home Oven Bakery.
Facts: cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR. Open 9 am to 10 pm, every day. Delivery 200 PKR, free from 3,000 PKR.
Use only these facts. If the answer is not here, say you do not know and a manager will call.
Answer Ali Raza in 2 short lines. Question: Do you make sugar-free cakes?
```

**AI answer (final reply only):**

```text
I don't know if we make sugar-free cakes.
A manager will call you.
```

**Useful?** Yes. It followed the instruction: two short lines, it said it does not know, and a manager will call. It did not invent a sugar-free cake or a price. This is the safe behaviour for a question the menu cannot answer. The reply does not help the customer by itself, so the owner has to call back.

**One thing I removed:** the raw output began with the model's own thinking, about 20 lines, before the final reply. That thinking misread the menu once ("brownie 301 PKR" instead of 300 PKR). The mistake is not in the final reply, but it shows that this model can misread facts. The thinking text would also confuse a customer, so a real bot must show only the final reply. This stand-in model was also very slow here, so for a short FAQ answer the small local model is the better choice.

## Summary

| Test | Model | Time | Final answer safe? | Invented facts? |
|---|---|---|---|---|
| Private question | gemma3:1b | 20 seconds | Yes | No |
| Normal question | qwen3:4b | 281 seconds | Yes | No, but the model's thinking misread one price |

Both prompts told the model to use only the listed facts, and both answers said "I do not know". Without the facts in the prompt, my Checkpoint 1 tests showed small models inventing prices and tools. I did not rerun a prompt without the facts, so I can only say the instruction worked in these two cases.
