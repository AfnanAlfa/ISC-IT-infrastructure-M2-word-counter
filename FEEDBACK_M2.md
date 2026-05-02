# M2 Pregrade — ISC230 Final Project (Project 2: Parallel Word Counter)

**Team:** Sara, Afnan Alfa
**Reviewed commit:** `7afb861` — *Update wordcounter.py / Update sequential word counter to handle 10 books*
**Reviewed:** Sat May 2, 2026

> **What this is:** a **pregrade** — a preliminary review from me to flag things while you still have time to fix them before M3. **The official M2 grade will be assigned by Eng. Aseel (IT)** based on your full submission (repo + Moodle PDF + demo video). Treat this document as advice, not a final mark.
>
> **Scope:** repository contents only. The PDF report and demo video are submitted directly on Moodle and will be graded from there.
>
> **Please read this carefully** — there is one important issue (the parallel version isn't in the repo) and you still have time to address it before M3.

---

## Pregrade (repo-only portion): 6 / 100

| Rubric component | Max | Pregrade |
|---|---:|---:|
| Parallel code works | 25 | 0 |
| Correctness verification | 15 | 0 |
| Code quality (sequential) | 15 | 4 |
| Technical explanation (in repo) | 15 | 0 |
| Timing measurement | 10 | 2 |
| Demo video (linked in repo) | 10 | 0 |
| Challenges reflection (in repo) | 5 | 0 |
| Week 3 plan + AI disclosure (in repo) | 5 | 0 |

If your PDF report and demo video were uploaded to Moodle, the four "in repo" rows will be re-scored from those Moodle deliverables. But the four code/repo rows depend on the repository state, and that's where most of the gap is right now.

---

## What's working well

- Your sequential pipeline is **correct and clean**. The pattern `count_words_in_book` → list of dicts → `merge_counts` → top-10 is exactly right and is the foundation `Pool.map()` will plug into. You don't have to rewrite anything to parallelize — you just have to swap how `count_words_in_book` is called across the 10 books.
- Auto-downloading the 10 Project Gutenberg books (`download_default_books`) is a nice touch. It makes the script reproducible.
- Good separation of `count_words_in_book` and `merge_counts` into pure functions. That's exactly the structure that `Pool.map()` needs.

---

## The one thing I want you to focus on right now

### `wordcounter.py` is still sequential

For Project 2, the M2 brief is very explicit:

> **P2 Word Counter:** 10 books word-counted **in parallel**, merged results correct
> **Parallel Tool:** `Pool.map()`

But the current `wordcounter.py` counts books sequentially:

```python
all_results = []
for book in book_files:
    result = count_words_in_book(book)   # one book at a time
    all_results.append(result)
```

There's no `multiprocessing` import in the file, and the most recent commit message itself reads *"Update sequential word counter to handle 10 books"* — so I think you already know this. The good news is that **your sequential code is already structured perfectly for `Pool.map()`** — you only need to change about 4 lines:

```python
from multiprocessing import Pool
import time

if __name__ == "__main__":
    download_default_books()
    book_files = [f"books/book{i}.txt" for i in range(1, 11)]

    # ----- Sequential -----
    start = time.time()
    seq_results = [count_words_in_book(b) for b in book_files]
    seq_merged = merge_counts(seq_results)
    seq_time = time.time() - start

    # ----- Parallel -----
    NUM_WORKERS = 4   # configurable — try 1, 2, 4, 8
    start = time.time()
    with Pool(processes=NUM_WORKERS) as pool:
        par_results = pool.map(count_words_in_book, book_files)
    par_merged = merge_counts(par_results)
    par_time = time.time() - start

    # ----- Correctness check -----
    assert seq_merged == par_merged, "Parallel result differs from sequential!"
    print("Correctness: PASSED")

    # ----- Comparison -----
    print(f"Sequential: {seq_time:.3f} s")
    print(f"Parallel  : {par_time:.3f} s  ({NUM_WORKERS} workers)")
    print(f"Speedup   : {seq_time / par_time:.2f}x")
```

A few important details for this to work:

1. **The `if __name__ == "__main__":` block is required.** On macOS and Windows, `multiprocessing.Pool` will spawn new processes that re-import your script; without this guard you'll get an infinite recursion or a pickling error.
2. **`count_words_in_book` must be defined at module level** (top of the file, not inside another function). It already is — good.
3. **Move the `input()` prompt out of the main script flow.** Right now `wordcounter.py` calls `input()` at module level, which will hang any automated benchmark. For M3 you'll want a clean script that runs end-to-end without user interaction.

If you fix this for M3 (you have until May 9), the "Parallel code works" row goes from 0 to a strong score, and you'll have a real story to tell in your benchmarking analysis.

---

## Other suggestions (smaller items)

### 1. Pair work — Sara should have commits too

The full git history shows commits only from `AfnanAlfa`. The M2 rubric explicitly looks for "both partners have commits" under Code Quality. For M3, please make sure Sara owns part of the code (e.g. the benchmarking script, the plotting code for the speedup graph, the top-20 words visualization) and commits it directly. The commit history is something the grader can check at a glance, so this matters.

### 2. The `input()` prompt blocks reproducibility

```python
print("Do you want to upload your own book? (yes / no)")
user_input = input().strip().lower()
```

This is an interactive prompt at module top-level, which means:
- A grader can't run `python wordcounter.py` and just get results — it hangs waiting for stdin.
- Your M3 benchmarking script (running 1, 2, 4, 8 workers × 3 repeats = 12 runs) will be impossible to automate around this.

For M3, suggest moving the upload-vs-default-books choice to a CLI flag or just removing it for the benchmark version:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--workers", type=int, default=4)
args = parser.parse_args()
```

The user-upload Colab feature is fine to keep in a separate notebook for the demo, but the main benchmark script should run unattended.

### 3. The `from google.colab import files` import

This sits inside an `if user_input == "yes":` branch, which is fine — but it means the script won't run outside Colab. If you want this to work both locally and on Colab for M3, wrap it:

```python
try:
    from google.colab import files
    uploaded = files.upload()
except ImportError:
    print("Local mode: skipping upload, using default books")
    download_default_books()
    book_files = [f"books/book{i}.txt" for i in range(1, 11)]
```

### 4. Repo hygiene for M3

M3 will require a clean repository structure. None of this affects your M2 mark, but starting now will save real stress next week:

- A real `README.md` with: project description, setup steps, how to run the sequential version, how to run the parallel version, where to find the report. (Right now there's no README at all.)
- A `requirements.txt` (this project actually only needs the standard library, so the file would be empty or just have `pytest` if you write tests — fine to note that explicitly).
- A `.gitignore` that ignores `books/` (the downloaded Gutenberg files), `__pycache__/`, and `.ipynb_checkpoints/`.
- Folder layout: `sequential/`, `parallel/`, `benchmarks/`, `data/` (or `books/`).

### 5. One subtle correctness improvement

Project Gutenberg files have a header and footer that aren't part of the book text (license boilerplate, table of contents, transcriber notes). For raw word counts this might be OK for M2, but be aware: when you compare top-10 results across books, words like "Project", "Gutenberg", and "License" can show up artificially. Worth a one-line mention in your report. Not something you have to fix.

### 6. `urllib.request.urlretrieve` without a User-Agent

Project Gutenberg sometimes returns 403 to requests with no User-Agent. If `download_default_books()` ever silently downloads a 100-byte HTML error page instead of the actual book, your word counts will be wrong but the script won't notice. A defensive check after downloading (e.g. `assert os.path.getsize(path) > 10000`) would catch this. Optional, but worth knowing.

---

## What I'd prioritize before May 9 (M3)

In rough order of impact on your final grade:

1. **Add `Pool.map()` parallelization to `wordcounter.py`** (snippet above). This single change moves the largest pile of marks. Without it, M2 has no parallel deliverable and M3's benchmarking section has nothing to benchmark.
2. **Fix the `input()` blocking issue** so the script can be benchmarked end-to-end.
3. **Sara: own and commit a piece of the M3 work** (benchmarking script and/or the top-20 words visualization are both well-scoped).
4. **Add a real `README.md`** with run instructions for both versions.
5. **Run your benchmark with workers = 1, 2, 4, 8 (3 repeats each)** and produce a speedup graph and an efficiency graph — those are M3 requirements.
6. **Apply Amdahl's Law** to your measured speedup to estimate the parallel fraction. With 10 books and `Pool.map`, the parallelizable fraction should be high — your serial fraction is dominated by file I/O for the merge step and the process spawn overhead.

---

## Reminder on Moodle deliverables

The PDF report (6–8 pages, 7 specified sections), the demo video (3–5 min, English narration), and the AI Use appendix are graded from your Moodle submission. Please **don't** push the PDF or video into this repo — keep the repo focused on code, results, and a clean README.

You have a clean foundation and the parallelization is a small change away. Don't get discouraged — focus on points 1–3 above and your M3 will be in much better shape.

— Dr. Shaikhah
