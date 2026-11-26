# How the proof is organised

This outline is read from the guide files and file headers of
[lsernau/grh-lean](https://github.com/lsernau/grh-lean), the short rewriting of
Levent Alpöge's Lean proof. Lean checks the code, not those comments, and this
outline was not checked by a number theorist. Treat it as a map of the
argument, not as a proof.

## What is proved

For every Dirichlet character χ, L(s, χ) has no zero with real part above 1/2
(except the pole at s = 1 for a principal character). The functional equation
then puts every zero in the critical strip on the line re s = 1/2. Taking the
trivial character gives the Riemann hypothesis.

## Step 1: zeros become a one-sided bound on a prime sum

Fix a modulus q and a prime d, and let K = ℚ(√−d). Define a weight on prime
powers n ≡ 1 mod q:

    λ(n) = Λ(n) · (1 − (n/d))

where Λ is the von Mangoldt function and (n/d) is the Legendre symbol. The
weight is zero on primes that split in K and positive on the others. The
remainder is

    R_q(x) = Σ_{n ≤ x} λ(n)·(1/n − 1/x) − log x / φ(q) − c_q

The criterion (`LFunction_ne_zero_of_primeRemainder_le`): if R_q(x) ≤ x^(β−1)
for all large x and all d in a suitable class, then no L(s, ψ) with ψ mod q
has a zero with re s > β. Only an upper bound is needed. This is a Landau-type
argument from 1905: a transform of a function that is eventually of one sign
has its first singularity on the real axis. The file cites Landau,
Montgomery–Vaughan §15 and Suzuki (2024).

So the whole proof reduces to showing R_q(x) ≤ x^(−1/2 + ε).

## Step 2: the bound comes from size against divisibility

The method is the one behind Stepanov and Bombieri's proof of the Riemann
hypothesis for curves, and behind Gelfond–Schnirelman bounds for primes: build
a nonzero algebraic number, bound its size from above at the complex places,
show it is divisible by many primes, and apply the product formula. The file
header for the main inequality cites exactly these.

The object here is a lattice of automorphic forms. Let E = K(ζ) be a CM field.
Take algebraic modular forms on a definite unitary group over E ("source
forms"), push them through a chain of m theta lifts between unitary groups of
growing rank, and land in "target forms". The number that gets measured is the
Gram determinant (covolume) of the lifted lattice.

The prime sum enters through divisibility. Lifts are built from Taylor
coefficients of theta functions with complex multiplication, and a derivative
of order y at a place σ is divisible by primes by the amount

    Σ_{ν ≤ a} Λ(ν)(1 − χ_K(ν)) · (y/ν − κ)₊

which is the same weight λ as in Step 1. This is the analogue of the fact that
log n! = Σ Λ(ν)⌊n/ν⌋, restricted to the primes that do not split in K.

## Step 3: three theorems and one inequality

- **Theorem A, short forms.** A normalised Poincaré series has lifts of small
  archimedean size and small index. Proved with a seesaw identity and local
  divisibility at each prime (`New/UpperBound`).
- **Theorem B, enough forms.** A few translates of that series span almost all
  target forms. Proved with a second-moment computation of Petersson type,
  with Bessel functions and Kloosterman sums (`New/Spanning`).
- **Theorem C, integral forms are long.** Covolume plus twice the index is at
  least the main amount. Proved by writing the determinant of the chain as a
  product of Hecke L-values (Rallis inner product and Siegel–Weil formulas),
  with a twist chosen for each prime and Selmer-group bounds from Galois
  representations to control denominators (`New/Determinant`, `New/OneLift`,
  `New/Congruences`).

With V the covolume bound, δ the index bound, and `rem` the prime-sum
remainder, these combine into

    mainAmount ≤ (V + 2δ)/dim ≤ mainAmount − (n/dim)·m·rem + errors

The main amount cancels, which leaves `rem` bounded above by the errors. With
m ≈ √x lifts and errors of size log⁶ b, the bound is x^(−1/2 + 6ε). The
exponent 1/2 comes from the number of lifts.

## Step 4: background the proof needs

Mathlib lacks most of the theory used, so the repository proves it, often in a
weaker form that is enough here: class field theory, ℓ-adic and Hodge
cohomology, Galois representations attached to eigenforms, p-adic Hodge theory
and Kisin modules, Shimura varieties, the Siegel–Weil and Rallis formulas, a
simple trace formula, a Chowla–Selberg formula, and the prime number theorem
in progressions. In the readable edition this background is 177,492 lines and
the argument itself is 122,410.

## Status

The proof has passed machine checks. The repository's own README says no
mathematician has read it through and no paper accompanies it.
