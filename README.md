# Parallel Word Counter

**Course:** ISC230 — IT Infrastructure  
**Team:** Sara Saed | Afnan Alfalah  

## Setup
1. Open Google Colab (colab.research.google.com)
2. Paste the code into a new cell
3. Run the code it will automatically download the 10 books.
No extra libraries are needed.

## How to Run Sequential Version
Open sequential_word_counter.py in Google Colab and run all cells.

## How to Run Parallel Version
Open parallel.py in Google Colab and run all cells.


Sequential Version: The sequential version processes the 10 books one by one using a normal loop.
Each book is read and cleaned and counted individually before moving to the next book.
After all books are processed we merged the word counts into one final result.
This approach is simple and easy to understand but it is slower because only one task runs at a time.

Parallel Version: The parallel version improves performance by processing multiple books at the same time using Python’s multiprocessing library.
So instead of handling books one by one the program distributes the books across several worker processes using Pool.map(). 
Each worker counts words in a different book simultaneously then all results are merged together.
This reduces execution time and demonstrates the concept of parallel computing.

Difference Between Sequential and Parallel: The main difference between the two approaches is how tasks are executed.
The sequential version handles one book at a time using a single process while the parallel version uses multiple workers to process several books simultaneously.
Sequential execution is simpler but slower for large workloads but parallel execution can improve speed and efficiency when tasks are independent.
Yet too many workers may reduce performance because of process management overhead.
