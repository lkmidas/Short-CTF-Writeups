# PBCTF2020: RGNN (RE)
1. Given file: `RGNN` (ELF64 binary).
2. Very short `main`, other (4) functions are hidden in `fini_array`.
3. First function reads number from 0 to 3 from a file into a 50x50 matrix.
4. Second and third functions perform checks on input matrix's rows and columns.
5. It checks for the existence of specific number sequences in the rows and columns, making this a `colored nonogram` solving problem.
6. Final function prints the flag based on the correct nonogram.
7. To solve the `nonogram`: using solver tools (for example `pynogram` - check `a.py`) or using z3 solver (author's solution - check `b.py`).
