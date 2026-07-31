# A Level Computer Science 9618 P1 Sub-Topical & Exam Tool

A feature-rich, interactive command-line application designed to help Cambridge AS Level Computer Science (9618) students revise Paper 1 (Theory Fundamentals). 

Instead of manually flipping through dozens of past paper PDFs, this application lets students search questions by specific subtopics or attempt full 90-minute timed exam papers with interactive answer reveals.

---

## ✨ Key Features

* 🔍 **Scoped Sub-Topical Search:**
  * Search questions by keyword (e.g., `printer`, `operating system`, `RAM`).
  * Filter search scope across **all papers**, a **specific paper** (e.g., `s24_11`), a **specific session** (e.g., `May/June 2025`), or a **year range** (e.g., `2024 to 2025`).

* 📝 **Full Exam Simulation Mode:**
  * Attempt complete yearly past papers by entering Year, Session (May/June or Oct/Nov), and Variant (11, 12, 13).
  * Displays official exam headers: **1 Hour 30 Minutes Duration**, **75 Marks**, and total question count.
  * Choose between **Interactive Mode** (one-by-one with answer reveals) or **Full Review Mode** (displays all questions and mark schemes together).

* ⏱️ **Real-Time Dynamic Exam Timer:**
  * Displays remaining minutes directly on question headers during exam mode.
  * Triggers an automated alert warning: `⚠️ 5 MINUTES LEFT!` when time is almost up.

* 🙈 **Interactive Active Recall:**
  * Hides mark schemes by default to promote active recall.
  * Reveals mark scheme bullet points and examiner reports upon user request (`y/n`).

* 🛡️ **Crash-Proof Data Ingestion:**
  * Defensive `try-except` error handling prevents crashes if `questions.json` is missing, empty, or formatted incorrectly.
  * Uses nested dictionary `.get()` calls to handle variations in key names gracefully.

---

## 📁 Project Structure

```text
📁 SubTopical Revision/
│
├── 📄 app.py              # Main interactive CLI application script
├── 📄 questions.json      # Dataset containing structured 9618 past paper questions
├── 📄 DOCUMENTATION.md    # In-depth project documentation & rubric breakdown
└── 📄 README.md          # Project overview & usage guide (This file)
