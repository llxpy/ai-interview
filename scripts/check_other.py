import json, random
from collections import Counter

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sample "其他" category questions
other = [q for q in data if q['category'] == '其他']
print(f"'其他' category: {len(other)} questions")
print(f"\nSample questions:")
for q in random.sample(other, min(50, len(other))):
    print(f"  [{q['answer'][:30]}...] {q['question'][:70]}")

# Check answer quality of "其他"
short = sum(1 for q in other if len(q['answer']) < 80)
print(f"\nShort answers (<80 chars): {short}/{len(other)}")
