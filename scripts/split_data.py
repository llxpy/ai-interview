import json, os

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === 1. Compress: shorter keys, remove whitespace ===
# q=question, c=category, d=difficulty, a=answer
compressed = []
for q in data:
    compressed.append({
        "i": q["id"],
        "q": q["question"],
        "c": q["category"],
        "d": q["difficulty"],
        "a": q["answer"]
    })

# === 2. Split by category ===
categories = {}
for q in compressed:
    cat = q["c"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(q)

# Save compressed full file (for "全部" view)
with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(compressed, f, ensure_ascii=False, separators=(',', ':'))

# Save per-category files
os.makedirs('public/data', exist_ok=True)
for cat, qs in categories.items():
    safe_name = cat.replace('/', '_')
    with open(f'public/data/{safe_name}.json', 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, separators=(',', ':'))

# Save category index
cat_index = [{"name": cat, "count": len(qs), "file": f"data/{cat.replace('/', '_')}.json"} for cat, qs in sorted(categories.items(), key=lambda x: -len(x[1]))]
with open('public/data/index.json', 'w', encoding='utf-8') as f:
    json.dump(cat_index, f, ensure_ascii=False, separators=(',', ':'))

full_size = os.path.getsize('public/data.json')
print(f"Compressed data.json: {full_size / 1024 / 1024:.2f} MB")
print(f"Category files: {len(categories)}")
for cat, qs in sorted(categories.items(), key=lambda x: -len(x[1])):
    size = os.path.getsize(f'public/data/{cat.replace("/", "_")}.json')
    print(f"  {cat}: {len(qs)} questions ({size/1024:.0f}KB)")
