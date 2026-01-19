# Meeting Notes: Math Core Module Kickoff

**Date:** 2023-10-27
**Project:** SimpleMathLib
**Goal:** Create a foundational python module for basic arithmetic operations.

---

## 1. Context
We need a lightweight library to handle basic calculations. Currently, we just need addition and multiplication. This will serve as the base for the future "Calculator" project.

## 2. Technical Requirements
* **Language:** Python 3.x
* **Style:** Must use strict type hinting (`int`).
* **Documentation:** Functions must have docstrings.

## 3. Implementation Plan (Action Items)
The AI Agent should execute the following tasks in order:

- [ ] **Setup Structure**: Create a file named `math_core.py`.
- [ ] **Feature 1 (Sum)**: Implement a function `sum(a: int, b: int) -> int` inside `math_core.py`. It should return the addition of the two numbers.
- [ ] **Feature 2 (Multiply)**: Implement a function `multiply(a: int, b: int) -> int` inside `math_core.py`. It should return the product of the two numbers.
- [ ] **Testing**: Create a test file `test_math_core.py` using `pytest`. Add unit tests for both `sum` (e.g., 2+2=4) and `multiply` (e.g., 3*4=12).

---

## 4. Edge Cases to Handle
* Ensure inputs are integers (type hints are sufficient for now, no runtime checks needed yet).