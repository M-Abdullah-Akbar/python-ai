"""Lesson 2.4: Batch Product Writer.

Writes a one-sentence AI description for every product on the price list in one
run, skips items with no price, and reports the total tokens and time.
"""

from langchain.chat_models import init_chat_model

# Create the model once, outside the loop, so every product reuses it.
# A little creative (0.7) suits marketing text
writer = init_chat_model("llama3.2", model_provider="ollama", temperature=0.7)

# Example prices for practice, not a real price list
products = {"chocolate cake": 1500, "cupcake": 250, "brownie": 300, "old stock": 0, "donut": 200}

results = []      # one dictionary per description, filled inside the loop
total_tokens = 0  # accumulators start at 0 BEFORE the loop, or every round would reset them
total_seconds = 0

for name, price in products.items():
    # Items with no price are not for sale, so do not spend tokens on them
    if price == 0:
        print(f"Skipping {name} (no price)")
        continue

    # The menu already prints the price, so the sentence describes taste and texture instead.
    # Starting with a describing word stops every line from opening with a verb like "Indulge"
    prompt = (
        f"Write one tempting sentence of at most 15 words that describes the taste and texture of '{name}' "
        "for a bakery menu. Start with a describing word, not a verb like Indulge or Enjoy. "
        "Do not mention the price, money or any shop name. Reply with the sentence only."
    )
    response = writer.invoke([{"role": "user", "content": prompt}])

    results.append({"item": name, "price": price, "text": response.text.strip()})
    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 50)
for number, row in enumerate(results, start=1):
    print(f"{number}. {row['item'].title()} ({row['price']} PKR)")
    print(f"   {row['text']}")
print("=" * 50)
print(f"{len(results)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")
