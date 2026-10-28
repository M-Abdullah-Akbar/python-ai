# Module 2 Checkpoint 1 Project: AI Content Studio (Design)

**Business:** Home Oven Bakery, Lahore. This name is a placeholder. The prices, hours, address and phone number are examples for practice, not real ones.

**Script:** `code/project_m2_content_studio.py`

## Facts

| Key | Value |
|---|---|
| name | Home Oven Bakery |
| city | Lahore |
| hours | 9 am to 10 pm, every day |
| address | Main Boulevard, Lahore |
| phone | 0300 0000000 (placeholder) |
| delivery | 200 PKR, free from 3,000 PKR |
| prices | chocolate cake 1,500 PKR, cupcake 250 PKR, brownie 300 PKR, donut 200 PKR, mango tart 0 (coming soon) |

## Tones

| Tone | Description sent to the AI |
|---|---|
| fun | playful and full of energy, short sentences |
| premium | elegant and calm, focused on quality |
| urgent | tells the reader to order today, with one clear call to action |

- `/post` with a tone that does not exist uses `fun`, through `.get()` with a default, so a wrong name never crashes.
- No tone may invent discounts, stock levels or deadlines. The prompt says to use only the facts.
- The post prompt lists **priced items only**. A `for` loop with `continue` copies only the priced items into a new dictionary, so the AI never sees the coming-soon item and cannot advertise it. In my first real run the urgent post advertised the mango tart at "PKR 0" even though the prompt said not to sell it, so a prompt rule alone was not enough.

## Config

| Setting | Value | Why |
|---|---|---|
| model | llama3.2 | the model pulled for the course |
| precise temperature | 0.2 | chat answers about prices and hours must be repeatable |
| creative temperature | 0.8 | marketing text should be varied |
| max_messages | 8 | memory is the system message plus the newest 8 messages |
| cloud price per 1K tokens | 0.5 PKR (example) | bonus cost estimate. Not a real price list |

## Which model for which job

| Job | Model and temperature | Why |
|---|---|---|
| Menu descriptions (`/menu`) | creative, 0.8 | Marketing text should be varied |
| Social media posts (`/post`) | creative, 0.8, streamed | Marketing text. Streaming shows the words as they arrive |
| Roman Urdu version of a post (bonus) | precise, 0.2 | A translation must stay close to the English post and not invent new claims |
| Chat questions | precise, 0.2, with facts and memory | Answers about prices and hours must be exact and grounded |
| `/price` | no AI | The dictionary is exact, free and instant |
| A price-0 item in `/menu` | skipped before the AI call | It is not for sale, so it spends no tokens |

## Commands

| Command | What it does | Uses the AI? |
|---|---|---|
| `/menu` | Writes one sentence per priced item, skips the price-0 item, prints a numbered menu with `:,` prices, then the cost estimate (bonus) | Yes, creative model, one call per item |
| `/post <tone>` | Streams a post in the chosen tone, then prints a Roman Urdu version (bonus) | Yes, creative model streamed, then the precise model |
| `/price <item>` | Real price, "coming soon" for price 0, or "not on our menu" | No |
| `/reset` | Clears the chat memory and keeps the system message | No |
| `bye` | Ends the loop and prints the session report | No |
| anything else | Chat question with memory | Yes, precise model |

Commands work in any capitals. Empty input asks again.

## What the streaming probe showed

I tested `llm.stream()` on `llama3.2` twice before writing the script.

- The token counts and the time arrive on **one chunk near the end** of the stream. That chunk is the second to last. The last chunk has empty metadata.
- So the script adds the numbers inside the loop, when `chunk.usage_metadata` has a value, and never reads the last chunk after the loop.
- The time in that chunk (`total_duration`) matched the wall-clock time: 37.9 seconds against 38.0 seconds in the first run. It includes loading the model.
- A post written without facts contained the placeholder `[Bakery Name]` and invented details (traditional Pakistani pastries). So every `/post` prompt includes the real shop name and the facts.

## How the session report counts

| Number | Meaning |
|---|---|
| Chat answers | Chat questions answered by the AI |
| Menu descriptions | Descriptions written by `/menu`. The skipped price-0 item is not counted |
| Posts | `/post` commands that produced a post |
| Price answers | Every `/price` command answered, including "coming soon" and "not on our menu" |
| Total tokens | Tokens of every AI call: chat, menu, posts and the Roman Urdu versions. Printed with `:,` |
| Total AI seconds | Time of every AI call, to one decimal |

## Feature tests

Every row was run on the real `llama3.2` model, except the rows marked "fake model", which replace the AI with a fake one to test only the logic, and row E7, which was not run. A test script typed the lines into the studio. It was not a live terminal, so these runs cannot show the words of a streamed post arriving one by one. "What the studio did" is shortened.

| # | You type | Expected | What the studio did | Pass? |
|---|---|---|---|---|
| 1 | `/MENU` | Price-0 item skipped, numbered menu, prices with commas | Printed `Skipping mango tart (coming soon)`, then 4 numbered items with prices like `1,500 PKR`, then `4 descriptions, 432 tokens` and a cloud cost estimate of 0.22 PKR | Yes |
| 2 | `/post fun`, `/POST Premium`, `/post urgent` | Post streams word by word, in a different style each time | Each command printed its tone line and a post. In my live terminal the post appeared gradually, so streaming works. The tones differ only a little: the urgent post says "Order now" and "Visit us today", and the premium post is longer, but they sound alike | Partly |
| 3 | `/post pirate` | Default tone used, no `KeyError` | Printed the fun tone line and a post | Yes |
| 4 | `/PRICE CUPCAKE` | Correct price | `Cupcake costs 250 PKR.` | Yes |
| 5 | `/price mango tart` | Coming soon | `Mango Tart is coming soon.` | Yes |
| 6 | `/price Pizza` | Not on our menu, no crash | `Sorry, pizza is not on our menu.` | Yes |
| 7 | `My name is Ali`, then `What is my name?` | Remembers the name | `Your name is Ali.` | Yes |
| 8 | `/reset`, then `What is my name?` | Does not know | `Memory cleared.`, then "I don't have that information... I don't know your name." | Yes |
| 9 | Press Enter with no text | Asks again | `Please type a command or a question.` | Yes |
| 10 | `BYE` | Goodbye and the session report with all numbers | `Goodbye!`, then the report: chat answers 3, menu descriptions 4, posts 4, price answers 3, and `2,536 tokens in 532.6 seconds` | Yes |

Extra tests for problems I found along the way:

| # | You type | Expected | What the studio did | Pass? |
|---|---|---|---|---|
| E1 | the four `/post` commands above | The price-0 item is never advertised | I read the final-code posts (urgent, premium, and the fun post in my screenshot) and none mentions the mango tart. In my first real run, before the fix, the urgent post advertised the mango tart at "PKR 0" | Yes |
| E2 | `/reset`, then a question | The system message survives | The next answer showed 3 messages in memory and 186 tokens sent, about the same as the first question (185), so the rules were still sent | Yes |
| E3 | `/post` with no tone (fake model) | Default tone | Printed the fun tone line and a post | Yes |
| E4 | `/price` with no item (fake model) | Help message | `Type /price and an item, like /price cupcake.` | Yes |
| E5 | `/count`, a command that does not exist (fake model) | Help message, no AI call | `I did not understand that command...` | Yes |
| E6 | `/menu` (fake model) | 4 AI calls, not 5 | The price-0 item was skipped before the AI call, so there were 4 calls | Yes |
| E7 | a chat of more than 8 messages | Memory never above the system message plus 8 | Not tested in this script. The trimming code is the same as Task 2.2, which I did test with a fake model | Untested |

**Result:** of the 10 required rows, 9 pass and row 2 passes partly. Streaming word by word was confirmed in my live terminal (`docs/project-m2-cp1-run.png`). The three tones sound too much alike, so I only give row 2 a partial pass.
