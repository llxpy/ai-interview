import json, random

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

remaining = [q for q in data if '建议结合项目经验' in q.get('answer', '')]
print(f"Remaining generic: {len(remaining)}")
print(f"\nRandom 30 samples:")
for q in random.sample(remaining, min(30, len(remaining))):
    print(f"  - {q['question'][:70]}")
