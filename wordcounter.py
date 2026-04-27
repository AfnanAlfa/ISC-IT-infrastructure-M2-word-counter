import time
import string

start = time.time()

with open('book.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.lower()
for p in string.punctuation:
    text = text.replace(p, ' ')

words = text.split()

counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

end = time.time()

print("Top 10 words:")
for word, count in top:
    print(f"  {word}: {count}")
print(f"\nSequential time: {end - start:.4f} seconds")
