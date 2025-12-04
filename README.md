# 🧠 BPE Tokenizer (GPT-2 Style)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/42charlie/GPT-2-Shakespeare-Tokenizer)

> **A from-scratch implementation of the Byte Pair Encoding (BPE) algorithm to demystify how Large Language Models (LLMs) process text.**

> **⚠️ Note for Learning:** This project was built for educational purposes to reverse-engineer and understand the BPE algorithm. While functional, it is a Python-based implementation optimized for clarity and learning rather than maximum training speed on massive corpora.

---

## 📖 The Story

About 8 months ago, fascinated by the release of powerful LLMs like ChatGPT, I decided that simply _using_ them wasn't enough—I wanted to understand them. I went back to the basics: **The Tokenizer**.

I built this project to reverse-engineer the tokenization process used by models like GPT-2. Instead of relying on pre-built libraries like HuggingFace, I wrote the logic myself in pure Python to fully grasp the mechanics of vocabulary construction, merge rules, and text compression.

## 🚀 Key Features

- **Custom Training:** Capable of training a unique vocabulary on any raw text dataset (e.g., Shakespeare).
- **Persistence:** Saves trained models (vocabulary & merge rules) to disk and "lazy loads" them when needed.
- **GPT-2 Pre-tokenization:** Implements the specific whitespace handling (converting spaces to `Ġ`) used by GPT-2 to preserve sentence structure.
- **Object-Oriented Design:** Clean, modular class structure suitable for integration into larger projects.
- **Efficient Encoding:** Optimized to load merge rules into memory once, preventing redundant I/O operations.

## 🛠️ Technical Implementation

This project implements **Byte Pair Encoding (BPE)**, an iterative algorithm that compresses text by replacing the most frequent pair of adjacent bytes with a new, single token.

### How it works:

1.  **Refinement:** Raw text is converted into a list of characters, with spaces preserved as special tokens.
2.  **Frequency Analysis:** The algorithm scans the corpus to count all adjacent character pairs.
3.  **Merge & Update:** The most frequent pair (e.g., `('t', 'h')`) is merged into a new token (`'th'`).
4.  **Iteration:** This process repeats until the desired vocabulary size is reached.

## 📚 Dataset

This tokenizer was trained on the complete works of William Shakespeare.

To reproduce the training results:

1.  Download the raw text file from [Project Gutenberg](https://www.gutenberg.org/ebooks/100).
2.  Save it as `the_complete_work.txt` in the project root.
3.  Run the training script.

_(Note: The dataset itself is not included in this repository to keep it lightweight.)_

## 💻 Usage

```python
from Tokenizer import Tokenizer

# 1. Initialize
tokenizer = Tokenizer()

# 2. Train on your own dataset (only needs to be done once)
# tokenizer.train("the_complete_work.txt", ntokens=4000)

# 3. Encode text (converts string -> list of integer IDs)
text = "I think the noble Duke is good"
ids = tokenizer.encode(text)
print(f"Token IDs: {ids}")
# Output: [7, 1062, 1959, 315, 1494, 2218]

# 4. Decode (converts IDs -> original string)
decoded_text = tokenizer.decode(ids)
print(f"Decoded: {decoded_text}")
```

## 🧠 What I Learned

Building this project was a deep dive into Natural Language Processing (NLP) and software engineering fundamentals:

- **Algorithm Design:** I learned how to translate a theoretical paper (BPE) into working code.
- **Data Structures:** Gained a deeper appreciation for `dictionaries` and `sets` for O(1) lookups during the frequent pair counting process.
- **Optimization:** My initial version was slow on large datasets. I learned to identify bottlenecks (like file I/O inside loops) and refactored the code to load models into RAM, drastically improving performance.
- **Pythonic Best Practices:** Evolved the project from a simple script into a robust Class with Type Hinting, Docstrings, and proper encapsulation.

## 📄 References & Research

This implementation is based on the methods described in the foundational papers that adapted BPE (originally a compression algorithm) for Neural Machine Translation and LLMs.

**Primary Reference:**

> **"Neural Machine Translation of Rare Words with Subword Units"** > _Rico Sennrich, Barry Haddow, Alexandra Birch (2016)_
>
> _"We introduce a simpler and more effective approach... making the NMT model capable of open-vocabulary translation by encoding rare and unknown words as sequences of subword units."_

**Original Algorithm:**

> **"A New Algorithm for Data Compression"** > _Philip Gage (1994)_

---

_Created by [[Ahmed Sadik](https://www.linkedin.com/in/42sadik/)]_
