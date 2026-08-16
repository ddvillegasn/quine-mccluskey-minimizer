# Quine-McCluskey Minimizer

A desktop application that minimizes Boolean functions from a list of minterms, implementing the
Quine-McCluskey tabular method with a Tkinter interface.

Built for a Digital Logic course at Universidad Tecnológica de Pereira.

---

## The problem it solves

Karnaugh maps stop being usable past four or five variables — the map becomes impossible to read by
eye. Quine-McCluskey solves the same problem the other way round: instead of a visual grouping, it
does an exhaustive tabular comparison, which means it can be run by a machine and does not degrade
as the number of variables grows.

Given a set of minterms, the program returns a simplified sum-of-products expression, which
translates directly into fewer logic gates in a circuit.

---

## How it works

**1. Grouping.** Each minterm is converted to binary, padded to the number of variables the function
needs, and filed into a group by how many `1` bits it contains. The variable count is derived from
the input as `ceil(log2(max(minterms) + 1))` — it is not asked for.

**2. Iterative combination.** Terms in adjacent groups are compared. Two terms that differ in exactly
one bit position are merged, with a `-` marking the position that no longer matters:

```
0100  ─┐
       ├─▶  01-0
0110  ─┘
```

Every term that took part in a merge is marked. The process repeats over the newly formed groups
until no further merges are possible. **Terms that never merged are the prime implicants.**

**3. Cover selection.** A coverage table maps each prime implicant to the minterms it covers. The
program then picks implicants one at a time, always choosing the one that covers the most
still-uncovered minterms, until every minterm is covered.

**4. Translation.** Each selected implicant becomes a product term: bit `1` → `A`, bit `0` → `A'`,
`-` → the variable is dropped. The results are joined with `+`.

---

## Honest limitation

**Step 3 is a greedy heuristic, not the exact method.**

Strictly, the Quine-McCluskey algorithm identifies *essential* prime implicants — those that are the
only cover for some minterm — and then resolves what remains with Petrick's method or an equivalent
exact search. This implementation skips that: it takes the largest-coverage implicant at each step.

For most textbook inputs the greedy choice lands on the same answer. **For a cyclic coverage chart it
can return a valid but non-minimal cover** — correct output, just not the shortest one possible.

Other limitations worth naming:

- **No don't-care conditions.** Minterms are all treated as required.
- **Variables are named `A`, `B`, `C`… positionally**, up to 26.
- The label in the interface says *"implicantes esenciales"*; per the above, *"cover terms"* would be
  the accurate word.

---

## Running it

Requires Python 3.8+.

```bash
python mccluskey.py
```

Nothing to install: the program uses only the Python standard library.

Enter minterms separated by spaces and press the calculate button.

```
Input:  0 1 2 5 6 7
Output: Número de variables: 3
        A'B' + A'C' + AC + AB
```

---

## Stack

`Python` · `Tkinter` for the interface · `math` from the standard library. **No external dependencies.**

## Status

Complete as a course project. Not maintained.

The obvious next step, for anyone picking it up: replace the greedy selection in step 3 with
Petrick's method so the result is guaranteed minimal, and add don't-care support.
