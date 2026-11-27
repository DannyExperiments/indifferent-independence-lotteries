# Reproducibility

Run from the repository root using Python 3.9 or newer. The replay uses the Python standard library and integer arithmetic for four equiprobable tickets.

```sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
```

Compare with [the checked log](verification/logs/replay.txt). The proof applies to arbitrary finite support and is separate from the finite-grid diagnostics. [PDF build](paper/BUILD.md) · [Visualization build](visualization/README.md)
