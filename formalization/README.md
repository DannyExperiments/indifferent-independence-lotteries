# Lean certificate

`CoupledLottery.same_outcome` is checked using Lean 4.30.0 and its standard library.

For a finite coupling over a linearly ordered commutative ring, coordinatewise domination on positive-mass atoms and equality of all weighted coordinate means force the paired outcomes to agree at every positive-mass atom. The certificate handles zero weights and arbitrary coordinate index sets. The construction of the lottery order and the proof of compatibility of the four axioms remain in the paper.

[Source](Q1089Coupling.lean) · [Verification workflow](../.github/workflows/lean.yml)

To replay from the repository root with Lean 4.30.0 installed, run

```sh
lean -DwarningAsError=true formalization/Q1089Coupling.lean
```

The source requests an axiom report. The GitHub Actions workflow downloads the pinned compiler, verifies its SHA-256 and checks the source with warnings treated as errors.
