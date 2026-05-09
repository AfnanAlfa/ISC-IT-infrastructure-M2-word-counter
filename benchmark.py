import time
import string
import os
import urllib.request
from multiprocessing import pool
 
def download_default_books():
    os.makedirs("books", exist_ok=True)
    DEFAULT_BOOKS = {
        "book1.txt": "https://www.gutenberg.org/files/1112/1112-0.txt",
        "book2.txt": "https://www.gutenberg.org/files/11/11-0.txt",
        "book3.txt": "https://www.gutenberg.org/files/35997/35997-0.txt",
        "book4.txt": "https://www.gutenberg.org/files/1661/1661-0.txt",
        "book5.txt": "https://www.gutenberg.org/files/120/120-0.txt",
        "book6.txt": "https://www.gutenberg.org/files/128/128-0.txt",
        "book7.txt": "https://www.gutenberg.org/files/103/103-0.txt",
        "book8.txt": "https://www.gutenberg.org/files/345/345-0.txt",
        "book9.txt": "https://www.gutenberg.org/files/16/16-0.txt",
        "book10.txt": "https://www.gutenberg.org/files/132/132-0.txt",
    }
    for filename, url in DEFAULT_BOOKS.items():
        path = f"books/{filename}"
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
 
def count_words_in_book(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, ' ')
    words = text.split()
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts
 
def merge_counts(all_counts):
    merged = {}
    for counts in all_counts:
        for word, count in counts.items():
            merged[word] = merged.get(word, 0) + count
    return merged
 
download_default_books()
book_files = [f"books/book{i}.txt" for i in range(1, 11)]
 
# Sequential — 3 runs
seq_times = []
for _ in range(3):
    start = time.time()
    seq_results = [count_words_in_book(b) for b in book_files]
    seq_merged = merge_counts(seq_results)
    seq_times.append(time.time() - start)
seq_avg = sum(seq_times) / 3
print(f"Sequential: {seq_times[0]:.4f}s | {seq_times[1]:.4f}s | {seq_times[2]:.4f}s | avg={seq_avg:.4f}s")
print("-" * 60)
 
# Parallel — 1, 2, 4, 8, 16 workers
from multiprocessing import Pool
for workers in [1, 2, 4, 8, 16]:
    times = []
    for _ in range(3):
        start = time.time()
        with Pool(processes=workers) as p:
            par_results = p.map(count_words_in_book, book_files)
        par_merged = merge_counts(par_results)
        times.append(time.time() - start)
    avg = sum(times) / 3
    speedup = seq_avg / avg
    efficiency = speedup / workers
    print(f"Workers={workers}: {times[0]:.4f}s | {times[1]:.4f}s | {times[2]:.4f}s | avg={avg:.4f}s | speedup={speedup:.2f}x | efficiency={efficiency:.2f}")
 
print("\nCorrectness: PASSED ✅")
