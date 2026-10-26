# Module 1 Checkpoint 2 Project: AI Front Desk (Design)

**Business:** Home Oven Bakery, Lahore. This name is a placeholder. The prices, hours, address and phone number below are examples for practice, not real ones.

**Script:** `code/project_m1_front_desk.py`

## Intents

The bot checks the rules from top to bottom and the first match wins. Exit, empty input and complaints come first, so an unhappy customer always reaches a person.

| # | Intent | Keywords | Reply |
|---|---|---|---|
| 1 | Exit | exit, or bye / goodbye in a message of 3 words or fewer | Goodbye, then the session report |
| 2 | Empty input | nothing typed | Asks for a question again. An empty line is not counted as a message |
| 3 | Complaint | refund, complain, unhappy, delay, late (see exceptions below), not delivered, not arrived | A manager will call within 1 hour. If the customer also asks for a human, the chat connects to a human |
| 4 | Human handover | human, agent | "Connecting you to a human..." and the chat ends |
| 5 | Quote | /quote, quote | Asks for an item and a quantity, then prints an exact total |
| 6 | Delivery | deliver | Delivery fee and the free-delivery limit |
| 7 | Prices | price, cost, how much, menu | Price list and the bulk discount |
| 8 | Hours | hour, open, timing, close, closing, closed | Open 9 am to 10 pm, every day |
| 9 | Location | where are you, where is your, your location, your address, branch, or just location / address | Main Boulevard, Lahore |
| 10 | Shop phone | your phone, your number, contact | The shop phone number (a placeholder) |
| 11 | Greeting | hi, hello, salam, assalam at the start of a message of 3 words or fewer | Friendly hello |
| 12 | Anything else | no match | Clean the question, route it to a model, print the AI prompt |

How the matching works:
- The message is lowercased, punctuation becomes a space, and repeated spaces are squeezed to one.
- A space is added at both ends, so a keyword like " late " matches the whole word "late" but not "chocolate". A keyword with a space only in front, like " price", also matches "prices".
- "Short message" means 3 words or fewer. Goodbye and greeting rules only use short messages, so "hi do you make wedding cakes" stays a question.
- "late" is a complaint, except in "open late", "late night", "till late" and "until late".
- Phrases like "where is my order" and "what time will my cake be ready" match no shop-information rule on purpose. They go to the AI route.

## Business rules

| Rule | Value |
|---|---|
| Item prices (example) | cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR |
| Item names | "cupcakes" works. A bare "cake" or "chocolate" means the chocolate cake. "wedding cake" is not on the menu |
| One item per quote | "cupcake and brownie" asks the customer to quote one item at a time |
| Bulk discount | 10% off the subtotal for 10 or more items |
| Delivery | 200 PKR, free when the amount after the discount is 3,000 PKR or more |
| Maximum quantity | 500 items. Bigger orders need the owner |
| Quantity input | Must be a whole number of at least 1. Anything else gets a polite message |
| Rule order for a quote | subtotal, then discount, then delivery is judged on the discounted amount |
| Private words | phone, mobile, number, cnic, email, address, password, a message that is only digits, numbers starting with 03 or +92 |
| Private questions | go to `gemma3:1b` (local), estimated cost 0 |
| All other unanswered questions | go to `qwen3:4b`, which stands in for a cheap cloud model, at an example price of 0.1 PKR per 1K tokens |
| Question length | cut to 150 characters |
| Token estimate | characters / 4, rounded, counted on the whole prompt the model would read |

**Why the quote order matters:** 12 cupcakes cost 3,000 PKR. After the 10% discount the order is 2,700 PKR, which is below the 3,000 PKR free-delivery limit, so delivery is still charged and the total is 2,900 PKR. If delivery were judged before the discount, it would be free and the total would be 2,700 PKR.

**The AI prompt** includes the bakery's menu, hours and delivery facts and the instruction "Use only these facts. If the answer is not here, say you do not know and a manager will call." This is meant to stop the model from inventing prices and timings.

## How the session report counts

| Number | Meaning |
|---|---|
| Messages | Every non-empty line typed at the main prompt, including the quote request and the goodbye |
| Answered by rules | Messages that a rule answered, including complaints, greetings, handover and the goodbye. Quote requests are counted separately |
| Unanswered | Messages sent to the AI route |
| Quotes | Quotes that were calculated successfully. An unknown item or a bad quantity does not count |
| Quoted value | The sum of those quote totals |
| Estimated AI cost | The sum of the estimated cloud cost of the unanswered questions. Private questions cost 0 |
| Complaints | Messages that hit the complaint rule (bonus) |

## Bonus features

- **Safe quantity:** `.isdigit()` is checked before `int()`, so letters, decimals and signs like `abc`, `2.5` and `-3` never crash the quote. Known limit: `.isdigit()` also accepts a few special characters such as the superscript `²`, and `int("²")` then raises `ValueError`. `try / except` in Module 2 fixes this.
- **Human handover:** `human` or `agent` ends the chat with "Connecting you to a human...", and the report shows the number of complaints.

## Rule tests

Every row was run against `code/project_m1_front_desk.py`. A test script typed the lines into the bot and checked that the expected text appeared in the output and that there was no crash. It was not run in a live terminal. Rows 1 to 10 are the tests the project asks for. Rows E1 to E20 are extra tests for the bugs I found and fixed. "What the bot did" shows the first lines of the reply and is cut at 130 characters.

| # | You type | Expected | What the bot did | Pass? |
|---|---|---|---|---|
| 1 | `  WHAT are your hours  ` | Hours (capitals and spaces handled) | We are open 9 am to 10 pm, every day. | Yes |
| 2 | `which cake is best?` | Fallback, not a greeting | Good question! Routed to: qwen3:4b (stand-in for a cheap cloud model) (~84 tokens) / Prompt: You are the assistant of Home Oven Ba... | Yes |
| 3 | `my order is late` | Manager reply (complaint rule first) | Sorry about that. A manager will call you within 1 hour. | Yes |
| 4 | `/quote`, 1 chocolate cake (most expensive item) | Delivery fee charged | 1 x chocolate cake = 1,500 PKR / Discount: 0 PKR ; Delivery: 200 PKR | Yes |
| 5 | `/quote`, 3 chocolate cakes (4,500 PKR, above the limit) | Delivery free | 3 x chocolate cake = 4,500 PKR / Discount: 0 PKR ; Delivery: 0 PKR | Yes |
| 6 | `/quote`, 10 cupcakes | Discount applied | 10 x cupcake = 2,500 PKR / Discount: -250 PKR ; Delivery: 200 PKR | Yes |
| 7 | `/quote`, pizza (not on the menu) | Not on our menu, no crash | Sorry, pizza is not on our menu. We have cupcake, brownie and chocolate cake. / report printed | Yes |
| 8a | `can I change my phone number on the order?` | Local model, cost 0 | Good question! Routed to: gemma3:1b (local, private) (~90 tokens) / Prompt: You are the assistant of Home Oven Bakery. | Yes |
| 8b | `my cnic is wrong` | Local model, cost 0 | Good question! Routed to: gemma3:1b (local, private) (~84 tokens) / Prompt: You are the assistant of Home Oven Bakery. | Yes |
| 9 | Press Enter with no text | Asks again | Please type a question. | Yes |
| 10 | `BYE` | Goodbye and the session report | Goodbye, Ali Raza! / report printed | Yes |
| E1 | `are you open late?` | Hours, not a complaint | We are open 9 am to 10 pm, every day. | Yes |
| E2 | `late night delivery?` | Delivery info, not a complaint | Delivery is 200 PKR, and free when your order is 3,000 PKR or more after any discount. | Yes |
| E3 | `my order was not delivered` | Manager reply | Sorry about that. A manager will call you within 1 hour. | Yes |
| E4 | `where is my order` | AI route, not the shop address | Good question! Routed to: qwen3:4b (stand-in for a cheap cloud model) (~84 tokens) / Prompt: You are the assistant of Home Oven Ba... | Yes |
| E5 | `what time will my cake be ready` | AI route, not the opening hours | Good question! Routed to: qwen3:4b (stand-in for a cheap cloud model) (~87 tokens) / Prompt: You are the assistant of Home Oven Ba... | Yes |
| E6 | `hi do you make wedding cakes` | A question, not just a greeting | Good question! Routed to: qwen3:4b (stand-in for a cheap cloud model) (~86 tokens) / Prompt: You are the assistant of Home Oven Ba... | Yes |
| E7 | `hello` | Greeting | Hello again, Ali Raza! How can I help? | Yes |
| E8 | `ok thanks bye` | Chat ends at once | Goodbye, Ali Raza! / report printed | Yes |
| E9 | `quote please`, cupcake, 12 | Starts a quote | 12 x cupcake = 3,000 PKR / Discount: -300 PKR ; Delivery: 200 PKR | Yes |
| E10 | `how  much is a brownie` (two spaces) | Price list | Cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR. 10% off for 10 or more items. Type /quote for an exact total. | Yes |
| E11 | `I am unhappy, connect me to a human` | Connects to a human, counts a complaint | Connecting you to a human... | Yes |
| E12 | `/quote`, `cupcake and brownie`, 5 | Asks for one item at a time | Please ask for one item at a time, then type /quote again for the next one. | Yes |
| E13 | `/quote`, `wedding cake`, 1 | Not on our menu | Sorry, wedding cake is not on our menu. We have cupcake, brownie and chocolate cake. | Yes |
| E14 | `/quote`, cupcake, `abc` | Polite message, no crash | Please type the quantity as a whole number, like 12. | Yes |
| E15 | `/quote`, cupcake, 501 | Too big, needs the owner | Orders above 500 items need the owner. Type human to talk to someone. | Yes |
| E16 | `my mobile number is 03001234567` | Local model, cost 0 | Good question! Routed to: gemma3:1b (local, private) (~87 tokens) / Prompt: You are the assistant of Home Oven Bakery. | Yes |
| E17 | `what is your phone number` | Answered by a rule with the shop number | You can call or WhatsApp us on 0300 0000000. | Yes |
| E18 | `/quote`, 9 cupcakes | No discount, delivery charged | 9 x cupcake = 2,250 PKR / Discount: 0 PKR ; Delivery: 200 PKR | Yes |
| E19 | `/quote`, 2 chocolate cakes (exactly 3,000 PKR) | Delivery free at the limit | 2 x chocolate cake = 3,000 PKR / Discount: 0 PKR ; Delivery: 0 PKR | Yes |
| E20 | `/quote`, 12 cupcakes (the discount trap) | Delivery still charged after the discount | 12 x cupcake = 3,000 PKR / Discount: -300 PKR ; Delivery: 200 PKR | Yes |

**Result:** 31 of 31 rows passed.
