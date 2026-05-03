import time
import string
import os
import urllib.request

# Default books
DEFAULT_BOOKS = {
    "book1.txt": "https://www.gutenberg.org/files/1112/1112-0.txt",   # Romeo and Juliet
    "book2.txt": "https://www.gutenberg.org/files/11/11-0.txt",       # Alice in Wonderland
    "book3.txt": "https://www.gutenberg.org/files/35997/35997-0.txt", # The Jungle Book
    "book4.txt": "https://www.gutenberg.org/files/1661/1661-0.txt",   # Sherlock Holmes
    "book5.txt": "https://www.gutenberg.org/files/120/120-0.txt",     # Treasure Island
    "book6.txt": "https://www.gutenberg.org/files/128/128-0.txt",     # Arabian Nights
    "book7.txt": "https://www.gutenberg.org/files/103/103-0.txt",     # Around the World in 80 Days
    "book8.txt": "https://www.gutenberg.org/files/345/345-0.txt",     # Dracula
    "book9.txt": "https://www.gutenberg.org/files/16/16-0.txt",       # Peter Pan
    "book10.txt": "https://www.gutenberg.org/files/132/132-0.txt",    # The Art of War
}

def download_default_books():
    os.makedirs("books", exist_ok=True)
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

if __name__ == "__main__":
    download_default_books()
    book_files = [f"books/book{i}.txt" for i in range(1, 11)]

    start = time.time()
    all_results = []
    for book in book_files:
        result = count_words_in_book(book)
        all_results.append(result)

    merged = merge_counts(all_results)
    end = time.time()

    top10 = sorted(merged.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n📊 Top 10 most common words:")
    for word, count in top10:
        print(f"   {word}: {count}")

    print(f"\n⏱️ Sequential time: {end - start:.4f} seconds")
