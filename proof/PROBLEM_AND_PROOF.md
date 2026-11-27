# Problem and proof outline

Can Good Expectations, Negative Dominance, positive-mass Stochastic Dominance and Indifferent Independence hold together? The order on sure outcomes is coordinatewise. The theorem uses the positive-mass strict coupling condition in the pinned catalog. Lederman’s generalized lottery definition allows zero weights; those matched atoms are deleted before checking strictness. [Source](https://arxiv.org/pdf/2311.08471v1#page=26)

## Convex indifference classes

For each vector mean, identify every finite convex mixture of the good lotteries with that mean. Also allow passage to any lottery that dominates under a coupling. Take the reflexive transitive closure of these steps. The vector mean increases coordinatewise. A dominating coupling with the same mean is an identity in distribution, so these convex sets and the remaining singleton lotteries are exactly the indifference classes.

## Strict comparisons

In a generating chain, glue the stochastic couplings before the first class move and after the last. At these two intermediate lotteries, ordered support extrema bound their means. Lifting those extrema through the outer couplings gives a cross-support witness. If the intermediate means are equal, the original strictness occurs in an outer mean comparison. An extreme atom of a non-Dirac good component is strictly beyond the corresponding mean. For a Dirac endpoint the outer coupling itself gives a strict atom. Hence the witness is strict even when the two intermediate means coincide.

[Complete argument](../paper/manuscript.pdf)
