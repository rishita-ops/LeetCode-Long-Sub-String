# LeetCode — Longest Substring Without Repeating Characters

A focused Python implementation of **LeetCode's Longest Substring Without Repeating Characters (Medium)** that **finds the length of the longest substring with no duplicate characters** in a single pass using a **sliding window**. Clean, minimal, and correct — this solution is the entry point to understanding the sliding-window technique, the window invariant ("no duplicates inside"), and the difference between a **substring** (contiguous) and a **subsequence** (not contiguous). The sliding window is one of the most reused patterns in string and array problems.

🔗 **Problem link:** [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

---

## Problem Statement

Given a string `s`, find the **length** of the **longest substring** without duplicate characters.

A **substring** is a contiguous sequence of characters within the string.

**Example 1:**

```
Input:  s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Note that "bca" and "cab" are also correct answers.
```

**Example 2:**

```
Input:  s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**

```
Input:  s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

**Official Constraints:**

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols, and spaces

---

## The Code

```python
s = input("Enter the string: ")

sub = ""
max_len = 0

for char in s:
    if char in sub:
        sub = sub[sub.index(char) + 1:]
    sub += char
    max_len = max(max_len, len(sub))

print(max_len)
```

---

## The Critical Idea — A Window That Never Contains a Duplicate

This is the most important thing to understand about this solution.

The string `sub` is a **window**: the current stretch of characters ending at the character just read. The program keeps one rule true at all times — **`sub` never contains a duplicate**. Each new character either extends the window, or, if it already appears inside, the window is **shortened from the left** just past the old copy, and then the new character is added.

The string `s` is never modified, and it is read **once** from left to right.

```
index:   0 1 2 3 4 5 6 7
s:       a b c a b c b b
         ─────                "abc"  length 3
           ─────              "bca"  length 3
             ─────            "cab"  length 3
               ─────          "abc"  length 3
                   ───        "cb"   length 2
                       ─      "b"    length 1
```

The window slides right across the string, never grows past the longest duplicate-free stretch, and `max_len` remembers the largest size it ever reached.

| Line of code             | What it does                                                                       |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `char in sub`            | Detects whether the new character would create a duplicate                         |
| `sub.index(char) + 1`    | Finds where the old copy ends, so everything up to **and including** it is dropped |
| `sub = sub[...:]`        | Keeps only the part of the window after the old copy                               |
| `sub += char`            | Adds the new character, so the window ends at the current position                 |
| `max(max_len, len(sub))` | Records the best window size seen so far                                           |

Because `sub` never holds a duplicate, `sub.index(char)` always finds the **only** copy of `char` — so the trim is always exactly right.

---

## How the Loop Works

```python
for char in s:
    if char in sub:
        sub = sub[sub.index(char) + 1:]
    sub += char
    max_len = max(max_len, len(sub))
```

- **Read:** `char` takes each character of `s` once, left to right
- **Check:** `char in sub` — is the new character already in the window?
- **Shrink:** if so, cut the window to everything **after** the old copy
- **Grow:** `sub += char` always adds the new character to the right end
- **Record:** `max_len` keeps the largest window length seen
- **Result:** after the loop, `max_len` is the answer

> **Off-by-one note:** The cut is `sub.index(char) + 1`, not `sub.index(char)`. Without the `+ 1`, the old copy would stay in the window, and adding the new character would create the very duplicate the window must never contain. The `+ 1` drops the old copy along with everything before it.

> **A common mistake this code avoids:** in the dictionary-based version of this problem, a "last seen" index can point to a character that has already left the window (try `"abba"`). Here, characters that leave the window are physically removed from the string `sub`, so a stale position can never be used.

---

## Algorithm (Pseudocode)

```
read s
window = ""
best   = 0

for each character c in s:
    if c is in window:
        window = part of window after the old copy of c
    window = window + c
    best = max(best, length(window))

print best
```

---

## Dry Run

**Input:** `s = "pwwkew"`

| `char` | In `sub`?                     | `sub` after trim | `sub` after adding | `len(sub)` | `max_len` |
| ------ | ----------------------------- | ---------------- | ------------------ | ---------- | --------- |
| `p`    | No                            | `""`             | `p`                | 1          | 1         |
| `w`    | No                            | `p`              | `pw`               | 2          | 2         |
| `w`    | **Yes** — old copy at index 1 | `""`             | `w`                | 1          | 2         |
| `k`    | No                            | `w`              | `wk`               | 2          | 2         |
| `e`    | No                            | `wk`             | `wke`              | 3          | 3         |
| `w`    | **Yes** — old copy at index 0 | `ke`             | `kew`              | 3          | 3         |

**Output:** `3` ✅

Note that `"pwke"` (length 4) is never considered: it is a subsequence, not a substring, and the window only ever holds **contiguous** characters.

---

## Complexity Analysis

| Metric | Complexity                                                                                                           |
| ------ | -------------------------------------------------------------------------------------------------------------------- |
| Time   | **O(n · w)** — one pass over `n` characters, and each step does `in`, `index`, and slicing on a window of length `w` |
| Space  | **O(w)** — the window string `sub`                                                                                   |

The window can never hold a repeated character, so `w` is at most the number of **distinct characters possible** (letters, digits, symbols, and spaces), which is a small fixed number. In practice this behaves like **O(n)**. In the worst case it is bounded by `n · min(n, k)`, where `k` is the size of the character set.

The two-pointer version below removes the window scans entirely and runs in true **O(n)**.

---

## Edge Cases

| Scenario                                   | Behavior                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| Empty string `""`                          | Loop never runs — prints `0` ✅ (an empty string is allowed by the constraints) |
| Single character `"a"`                     | Window `a` — prints `1` ✅                                                      |
| All characters equal `"bbbbb"`             | Window resets to `"b"` every step — prints `1` ✅                               |
| All characters distinct `"abcdef"`         | Window grows to the full string — prints `6` ✅                                 |
| Repeat that is _not_ adjacent `"dvdf"`     | `d`, `dv`, then `d` repeats → `vd`, then `vdf` — prints `3` ✅                  |
| Old copy of a character long gone `"abba"` | `a`, `ab`, then `b` repeats → `b`, then `ba` — prints `2` ✅                    |
| Case-sensitive `"aA"`                      | `'a'` and `'A'` are different characters — prints `2` ✅                        |
| Spaces inside the string `"a b a"`         | A space is an ordinary character — handled like any other ✅                    |
| Subsequence trap `"pwwkew"`                | Prints `3`, not `4` ✅                                                          |
| Very long string (`5 · 10⁴` characters)    | Works, since the window stays short ✅                                          |

---

## Code-Quality Notes

**This is a script, not a LeetCode submission.** The code reads the string with `input()` and prints the result at the top level. LeetCode instead calls a method on a class and expects an `int` back, so this code will not run in the LeetCode editor as it is. The submittable version is in the next section.

**Only the length is tracked.** The problem asks for the **length**, so the code never stores the best substring. To report the substring itself, save a copy whenever a new maximum is found:

```python
if len(sub) > max_len:
    max_len = len(sub)
    best = sub
```

**String building creates copies.** Each `sub += char` and each slice builds a new string. For a window this short that is harmless, but it is the reason the next version, which only moves two integers, is faster.

---

## The Natural Extension — Two Pointers With a Dictionary

Instead of rebuilding a string, keep **two indices**, `left` and `right`, marking the window inside the original string, and a dictionary `last_seen` that remembers **the last index** of each character. When a character repeats **inside the window**, jump `left` to just past its previous position.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1
            last_seen[ch] = right
            best = max(best, right - left + 1)

        return best
```

**Trace for `"abba"`:**

| `right` | `ch` | `last_seen[ch]` before | `>= left`?     | `left` after | Window | `best` |
| ------- | ---- | ---------------------- | -------------- | ------------ | ------ | ------ |
| 0       | `a`  | —                      | —              | 0            | `a`    | 1      |
| 1       | `b`  | —                      | —              | 0            | `ab`   | 2      |
| 2       | `b`  | 1                      | Yes            | 2            | `b`    | 2      |
| 3       | `a`  | 0                      | **No** (0 < 2) | 2            | `ba`   | 2      |

**Result:** `2` ✅ — the check `last_seen[ch] >= left` is what stops the old `a` (already outside the window) from pulling `left` backwards.

| Property                       | String window (this code) | Two pointers + dictionary |
| ------------------------------ | ------------------------- | ------------------------- |
| Time                           | O(n · w), about O(n)      | **O(n)**                  |
| Extra space                    | O(w)                      | O(w)                      |
| Works as a LeetCode submission | ❌ No (script)            | ✅ Yes                    |
| Builds new strings             | ✅ Yes                    | ❌ No                     |
| Stale-index pitfall            | Not possible              | Needs the `>= left` check |
| When to use                    | Learning the window idea  | Interviews and LeetCode   |

---

## Repository Structure

```
LeetCode-Longest-Substring-Without-Repeating-Characters/
│
├── longest_substring.py    # Main Python implementation
└── README.md               # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/rishita-ops/LeetCode-Longest-Substring-Without-Repeating-Characters.git
cd LeetCode-Longest-Substring-Without-Repeating-Characters

# Run
python3 longest_substring.py
```

**On Windows:**

```bash
python longest_substring.py
```

**Sample session:**

```
Enter the string: pwwkew
3
```

---

## Key Concepts Covered

- **Sliding window** — a moving stretch of the input that always satisfies a rule
- **Window invariant** — `sub` never contains a duplicate character
- **Substring vs subsequence** — substrings are contiguous, subsequences are not
- **`sub.index(char) + 1`** — drop the old copy and everything before it
- **Single pass** — each character of `s` is read exactly once
- **Tracking only the length** — `max(max_len, len(sub))` instead of storing substrings
- **Two-pointer version** — `left`, `right`, and a `last_seen` dictionary give true O(n)
- **Stale-index check** — `last_seen[ch] >= left` ignores characters outside the window

---

## Why This Problem Matters in DSA

The sliding-window pattern appears across a broad family of problems:

| Problem / Concept                                           | Connection                                                              |
| ----------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Longest Repeating Character Replacement** (LeetCode #424) | Same expanding and shrinking window, with a replacement budget          |
| **Minimum Window Substring** (LeetCode #76)                 | Window that must contain required characters, shrunk as far as possible |
| **Permutation in String** (LeetCode #567)                   | Fixed-size window compared against character counts                     |
| **Max Consecutive Ones III** (LeetCode #1004)               | Window allowed at most `k` zeros                                        |
| **Fruit Into Baskets** (LeetCode #904)                      | Longest window with at most two distinct values                         |
| **Maximum Erasure Value** (LeetCode #1695)                  | Window of unique elements, maximizing the sum instead of the length     |

Every problem that asks for the longest or shortest stretch satisfying a condition traces back to the sliding-window idea introduced here.

---

## Contributing

Contributions are welcome. Consider adding:

- The **two-pointer dictionary** version as a separate, submittable file
- A version using a **set** instead of a dictionary
- A version that returns the **substring itself**, not just its length
- A version that prints the **window at every step** for visualization
- Input validation and tests for tricky strings such as `"abba"` and `"dvdf"`
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured LeetCode practice series — fundamentals, done right._
