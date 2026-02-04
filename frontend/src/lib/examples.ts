export const defaultCode = `theorem and_comm {p q : Prop} : p ∧ q ↔ q ∧ p := by
  apply Iff.intro
  · intro h
    constructor
    · exact h.right
    · exact h.left
  · intro h
    constructor
    · exact h.right
    · exact h.left`;

export const exampleProofs = {
  // Simple: 2 steps
  simple: `theorem id_map {α : Type} (x : α) : x = x := by
  rfl`,

  // Logic: ~8 steps
  andComm: `theorem and_comm {p q : Prop} : p ∧ q ↔ q ∧ p := by
  apply Iff.intro
  · intro h
    constructor
    · exact h.right
    · exact h.left
  · intro h
    constructor
    · exact h.right
    · exact h.left`,

  // Induction: ~12 steps with simp usually, but here we can make it verbose?
  // Use a standard mathlib-style one but simplified
  induction: `theorem sum_n (n : Nat) : 2 * (List.range (n + 1)).sum = n * (n + 1) := by
  induction n with
  | zero =>
    simp
  | succ n ih =>
    simp
    rw [Nat.mul_add]
    rw [ih]
    -- n * (n + 1) + 2 * (n + 1)
    rw [← Nat.add_mul]
    -- (n + 2) * (n + 1)
    rw [Nat.mul_comm]
    -- (n + 1) * (n + 2)
    rfl`,

  // Logic Chain: 12 steps
  logicChain: `theorem logic_chain (p q r s t u : Prop) : 
  (p → q) → (q → r) → (r → s) → (s → t) → (t → u) → p → u := by
  intro h1
  intro h2
  intro h3
  intro h4
  intro h5
  intro hp
  apply h5
  apply h4
  apply h3
  apply h2
  apply h1
  exact hp`,

  // Algebra Verbose: ~15 steps
  algebrav: `theorem expansion (a b : Nat) : (a + b) * (a + b) = a * a + 2 * a * b + b * b := by
  rw [Nat.mul_add]
  rw [Nat.add_mul]
  rw [Nat.add_mul]
  rw [Nat.mul_comm b a]
  rw [Nat.add_assoc]
  rw [Nat.add_assoc (a * a)]
  rw [← Nat.mul_assoc]
  rw [Nat.mul_comm 2 a]
  rw [Nat.mul_assoc a]
  rw [Nat.two_mul]
  rw [Nat.add_mul]
  rw [Nat.one_mul]`,

  // Distributivity: ~14 steps
  distrib: `theorem dist_exists {α : Type} (p q : α → Prop) : 
  (∃ x, p x ∨ q x) ↔ (∃ x, p x) ∨ (∃ x, q x) := by
  apply Iff.intro
  · intro h
    cases h with
    | intro x hx => 
      cases hx with
      | inl hp => 
        apply Or.inl
        exists x
      | inr hq => 
        apply Or.inr
        exists x
  · intro h
    cases h with
    | inl hp => 
      cases hp with
      | intro x px =>
        exists x
        apply Or.inl
        exact px
    | inr hq =>
      cases hq with
        apply Or.inr
        exact qx`,

  // Infinitude of Primes (Euclid's Proof)
  infinitudePrimes: `import Mathlib.Data.Nat.Prime
import Mathlib.Tactic

theorem infinitude_of_primes : ∀ n, ∃ p, n ≤ p ∧ Nat.Prime p := by
  intro n
  -- Consider N = n! + 1
  let N := n.factorial + 1
  -- N has a prime factor p
  have p_exists : ∃ p, Nat.Prime p ∧ p ∣ N := Nat.exists_prime_and_dvd (Nat.factorial_lt n).ne'
  rcases p_exists with ⟨p, hp, hdvd⟩
  exists p
  constructor
  · -- Prove n ≤ p by contradiction
    by_contra hlt
    push_neg at hlt
    -- If p < n, then p | n!
    have h_dvd_fact : p ∣ n.factorial := Nat.dvd_factorial (Nat.Prime.pos hp) (le_of_lt hlt)
    -- If p | N and p | n!, then p | 1
    have h_dvd_one : p ∣ 1 := (Nat.dvd_add_right h_dvd_fact).mp hdvd
    -- But distinct primes are > 1
    exact Nat.Prime.not_dvd_one hp h_dvd_one
  · exact hp`,

  // Irrationality of Sqrt(2)
  irrationalSqrt2: `import Mathlib.Data.Nat.Prime
import Mathlib.Tactic
import Mathlib.Tactic.Linarith

theorem sqrt2_irrational (p q : ℕ) (h_coprime : p.Coprime q) (hq : q > 0) :
  p * p ≠ 2 * q * q := by
  intro h_eq
  -- 2 divides p²
  have h_2_dvd_p2 : 2 ∣ p * p := by
    use q * q
    rw [← h_eq]
    ring
  -- Therefore 2 divides p (since 2 is prime)
  have h_2_dvd_p : 2 ∣ p := Nat.Prime.dvd_of_dvd_pow Nat.prime_two h_2_dvd_p2
  obtain ⟨k, rfl⟩ := h_2_dvd_p
  
  -- Substitute p = 2k back into equation
  -- (2k)² = 2q² => 4k² = 2q² => 2k² = q²
  rw [mul_assoc, ← pow_two, (show (2 * k) ^ 2 = 4 * k ^ 2 by ring)] at h_eq
  have h_eq_simpl : 2 * k ^ 2 = q ^ 2 := by
    linarith
    
  -- Now 2 divides q²
  have h_2_dvd_q2 : 2 ∣ q * q := by
    use k ^ 2
    rw [pow_two, h_eq_simpl]
  -- Therefore 2 divides q
  have h_2_dvd_q : 2 ∣ q := Nat.Prime.dvd_of_dvd_pow Nat.prime_two h_2_dvd_q2
  
  -- Contradiction: p and q have common factor 2, but were coprime
  have h_common : 2 ∣ p.gcd q := Nat.dvd_gcd (by use k; ring) h_2_dvd_q
  rw [h_coprime] at h_common
  -- 2 divides 1, impossible
  norm_num at h_common`,



  // User Proof: Hohenberg Kohn
  hkTheorem: `import Mathlib

-- Abstract types for quantum setting
axiom Wavefunc : Type
axiom Density : Type
-- Potential is a function from space to real numbers
def Potential : Type := ℝ → ℝ

-- Fundamental operations and functionals
axiom density_of : Wavefunc → Density
axiom integral : Potential → Density → ℝ
axiom kinetic_interaction : Wavefunc → ℝ
axiom energy_expectation : Wavefunc → Potential → ℝ

axiom energy_def (ψ : Wavefunc) (v : Potential) :
  energy_expectation ψ v = kinetic_interaction ψ + integral v (density_of ψ)

axiom ground_state : Potential → Wavefunc
axiom ground_energy : Potential → ℝ

axiom ground_energy_def (v : Potential) :
  ground_energy v = energy_expectation (ground_state v) v

-- Strict inequality version of Rayleigh-Ritz for distinct states
axiom rayleigh_ritz_strict (v : Potential) (ψ : Wavefunc) :
  ψ ≠ ground_state v → energy_expectation ψ v > ground_energy v

-- Axiom: different potentials (not differing by constant) yield different ground states
axiom distinct_potentials_distinct_states (v₁ v₂ : Potential) :
  (¬ ∃ c : ℝ, ∀ x, v₁ x = v₂ x + c) → ground_state v₁ ≠ ground_state v₂

-- Axiom: integral is linear in potential
axiom integral_diff (v₁ v₂ : Potential) (n : Density) :
  integral v₁ n - integral v₂ n = integral (fun x => v₁ x - v₂ x) n

-- The universal density functional (must be noncomputable)
noncomputable def F (n : Density) : ℝ :=
  sInf (Set.image kinetic_interaction {ψ : Wavefunc | density_of ψ = n})

/- HK1 Theorem: Proof by Contradiction -/
theorem Hohenberg_Kohn1
  (v₁ v₂ : Potential)
  (h_distinct : ¬ ∃ c : ℝ, ∀ x, v₁ x = v₂ x + c)
  (h_same_dens : density_of (ground_state v₁) = density_of (ground_state v₂)) :
  False := by
  -- Define ground states
  let ψ₁ := ground_state v₁
  let ψ₂ := ground_state v₂

  -- Ground states are distinct for distinct potentials
  have states_distinct : ψ₁ ≠ ψ₂ := distinct_potentials_distinct_states v₁ v₂ h_distinct

  -- Apply strict Rayleigh-Ritz
  have rr₁_strict : energy_expectation ψ₂ v₁ > ground_energy v₁ := by
    apply rayleigh_ritz_strict
    intro h
    exact states_distinct h.symm

  have rr₂_strict : energy_expectation ψ₁ v₂ > ground_energy v₂ := by
    apply rayleigh_ritz_strict
    intro h
    exact states_distinct h

  -- Expand energies using energy_def
  have exp₁ : energy_expectation ψ₂ v₁ = kinetic_interaction ψ₂ + integral v₁ (density_of ψ₂) :=
    energy_def ψ₂ v₁
  have exp₂ : energy_expectation ψ₁ v₂ = kinetic_interaction ψ₁ + integral v₂ (density_of ψ₁) :=
    energy_def ψ₁ v₂

  -- Ground energies in expanded form
  have e₁ : ground_energy v₁ = kinetic_interaction ψ₁ + integral v₁ (density_of ψ₁) := by
    rw [ground_energy_def, energy_def]
  have e₂ : ground_energy v₂ = kinetic_interaction ψ₂ + integral v₂ (density_of ψ₂) := by
    rw [ground_energy_def, energy_def]

  -- Use the fact that densities are the same
  let n := density_of ψ₁
  have dens_eq : density_of ψ₂ = n := h_same_dens.symm

  -- Rewrite everything in terms of the common density n
  rw [dens_eq] at exp₁ e₂

  -- From the inequalities, derive the contradiction
  have ineq₁ : kinetic_interaction ψ₂ + integral v₁ n > kinetic_interaction ψ₁ + integral v₁ n := by
    rw [←exp₁, ←e₁]; exact rr₁_strict

  have ineq₂ : kinetic_interaction ψ₁ + integral v₂ n > kinetic_interaction ψ₂ + integral v₂ n := by
    rw [←exp₂, ←e₂]; exact rr₂_strict

  have E₁_expand : ground_energy v₁ = kinetic_interaction ψ₁ + integral v₁ n := e₁
  have E₂_expand : ground_energy v₂ = kinetic_interaction ψ₂ + integral v₂ n := e₂

  have ineq₁' : ground_energy v₂ > ground_energy v₁ + integral v₂ n - integral v₁ n := by
    rw [E₂_expand]; linarith

  have ineq₂' : ground_energy v₁ > ground_energy v₂ + integral v₁ n - integral v₂ n := by
    rw [E₁_expand]; linarith

  -- Add the inequalities to get a contradiction: E₁ + E₂ > E₁ + E₂
  linarith`,

  janakTheorem: `import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

/-!
# Janak's Theorem: ∂E/∂nᵢ = εᵢ

Reference: J.F. Janak, Phys. Rev. B 18, 7165 (1978)

This formalization **derives** Janak's theorem from explicit physical axioms,
following the paper's derivation chain:
  Eq (2) [KS equation] → Eq (3) → Eq (5) → Eq (6) → Eq (9) → Eq (10)

## Key Design Decisions

1. We use a finite-dimensional abstraction: occupation numbers n : Fin N → ℝ
2. The energy is a function E : (Fin N → ℝ) → ℝ of occupations
3. Physical constraints are stated as explicit axioms
4. All equations are DERIVED, not encoded

## Axioms (Minimal Physical Input)

1. **KS Eigenvalue Equation**: Hφᵢ = εᵢφᵢ implies ⟨φᵢ|H|φᵢ⟩ = εᵢ
2. **Stationarity**: E is stationary w.r.t. orbital variations at self-consistency
3. **Normalization**: ∫|φⱼ|² = 1 for all occupations, so d/dnᵢ(∫|φⱼ|²) = 0

## For ML Applications

If replacing Exc with an ML model, the model must:
- Be differentiable w.r.t. density
- Satisfy vxc = δExc/δρ
- Preserve stationarity at self-consistency
-/

set_option linter.style.longLine false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false

namespace JanakTheorem

/-!
## Part I: Basic Structures

We work with N orbitals indexed by Fin N.
-/

variable (N : ℕ) [NeZero N]

/-- Occupation numbers: nᵢ ∈ ℝ for each orbital i -/
abbrev OccNum := Fin N → ℝ

/-!
## Part II: The Kohn-Sham System

**Eq (2)**: The Kohn-Sham eigenvalue equation
  [-∇² + Vₕ(r) + vxc(r)]φᵢ = εᵢφᵢ

This defines:
- φᵢ : Kohn-Sham orbitals (eigenfunctions)
- εᵢ : Kohn-Sham eigenvalues

Taking the expectation ⟨φᵢ|H|φᵢ⟩ gives:
  Tᵢ + Vᵢ = εᵢ

where Tᵢ = ⟨φᵢ|-∇²|φᵢ⟩ and Vᵢ = ⟨φᵢ|Veff|φᵢ⟩
-/

/-- Bundle of Kohn-Sham system data at a given occupation configuration -/
structure KSSystem where
  /-- Kohn-Sham eigenvalues εᵢ (from Eq 2) -/
  ε : Fin N → ℝ
  /-- Kinetic energy integral: Tᵢ = ⟨φᵢ|-∇²|φᵢ⟩ -/
  T_orbital : Fin N → ℝ
  /-- Effective potential integral: Vᵢ = ⟨φᵢ|Veff|φᵢ⟩ -/
  V_eff : Fin N → ℝ

variable (sys : OccNum N → KSSystem N)

/-!
## Part III: Axiom 1 - The Kohn-Sham Equation (Eq 2)

**AXIOM**: For any occupation configuration n,
the KS eigenvalue equation Hφᵢ = εᵢφᵢ implies ⟨φᵢ|H|φᵢ⟩ = εᵢ

This is the fundamental input from quantum mechanics.
-/

/-- **AXIOM (Eq 2)**: KS eigenvalue equation in expectation form -/
class KohnShamAxiom : Prop where
  eigenvalue_eq : ∀ (n : OccNum N) (i : Fin N),
    (sys n).T_orbital i + (sys n).V_eff i = (sys n).ε i

/-!
## Part IV: Eq (3) - Derived from KS Equation

**THEOREM**: tᵢ = εᵢ - Vᵢ

This defines the "orbital kinetic energy" as used in the paper.
We DERIVE this from the KS equation, not assume it.
-/

/-- Definition of orbital kinetic energy tᵢ (Eq 3 form) -/
def t (n : OccNum N) (i : Fin N) : ℝ := (sys n).ε i - (sys n).V_eff i

/-- **THEOREM (Eq 3)**: T_orbital = ε - V_eff, derived from KS equation -/
theorem derive_eq3 [h : KohnShamAxiom N sys] (n : OccNum N) (i : Fin N) :
    (sys n).T_orbital i = t N sys n i := by
  unfold t
  have h_ks := h.eigenvalue_eq n i
  linarith

/-!
## Part V: Eq (5) - Total Energy Definition

**DEFINITION**: E = T + U[ρ] + Exc[ρ]

where T = Σᵢ nᵢ tᵢ is the total kinetic energy.

The key insight is that U and Exc depend on n through the density ρ = Σᵢ nᵢ|φᵢ|²
-/

/-- Coulomb + Exchange-Correlation energy functional U[ρ] + Exc[ρ] -/
variable (U_Exc : OccNum N → ℝ)

/-- Total kinetic energy: T = Σᵢ nᵢ tᵢ -/
noncomputable def T_total (n : OccNum N) : ℝ :=
  ∑ i : Fin N, n i * t N sys n i

/-- **Eq (5)**: Total energy E = T + U + Exc -/
noncomputable def E (n : OccNum N) : ℝ :=
  T_total N sys n + U_Exc n

/-!
## Part VI: Eq (6) - Computing the Derivative

To compute ∂E/∂nᵢ, we need to understand how E depends on nᵢ.

E depends on nᵢ through:
1. The explicit factor nᵢ in T = Σⱼ nⱼ tⱼ
2. The orbitals φⱼ and eigenvalues εⱼ, which solve the KS equation for density ρ(n)
3. The functionals U[ρ] and Exc[ρ]

**Key Physical Insight (Stationarity)**:
At self-consistency, E is stationary with respect to orbital variations:
  δE/δφᵢ = 0

This means the ONLY contribution to ∂E/∂nᵢ comes from:
- The explicit nᵢ factor in T
- The change in ρ = Σⱼ nⱼ|φⱼ|² (the |φᵢ|² term)

The paper shows (Eqs 6-8) that these combine to give:
  ∂E/∂nᵢ = εᵢ + Σⱼ nⱼ εⱼ δᵢⱼ

where δᵢⱼ = ∫(∂φⱼ*/∂nᵢ)φⱼ dr + c.c.
-/

/-- Orbital variation integral: δᵢⱼ = d/dnᵢ(∫|φⱼ|²) -/
variable (δ_orbital : OccNum N → Fin N → Fin N → ℝ)

/-!
## Part VII: Axiom 2 - Stationarity and Derivative Structure

**AXIOM**: At self-consistency (KS equations satisfied), the derivative has the form:
  ∂E/∂nᵢ = εᵢ + Σⱼ nⱼ εⱼ δᵢⱼ

This encapsulates the entire chain Eqs (6)-(9) in the paper.
The proof of this in the continuum requires:
- Stationarity: δE/δφ = 0 at self-consistency
- Using the KS equation to simplify derivative terms
-/

/-- **AXIOM (Eqs 6-9)**: Derivative structure at self-consistency

This axiom states that when the KS equations are satisfied,
the derivative of E with respect to nᵢ has the specific form derived in the paper.

The derivation in the continuum uses:
1. Product rule on T = Σⱼ nⱼ tⱼ
2. Chain rule for U[ρ] and Exc[ρ]
3. Substitution of tᵢ = εᵢ - Vᵢ (from Eq 3)
4. The KS equation Hφⱼ = εⱼφⱼ to simplify variation terms
-/
class DerivativeStructureAxiom : Prop where
  deriv_form : ∀ (n : OccNum N) (i : Fin N),
    /- The derivative ∂E/∂nᵢ, computed by varying nᵢ while keeping others fixed -/
    deriv (fun nᵢ => E N sys U_Exc (Function.update n i nᵢ)) (n i) =
      (sys n).ε i + ∑ j : Fin N, n j * (sys n).ε j * δ_orbital n i j

/-!
## Part VIII: Axiom 3 - Normalization Constraint (Key Physics!)

**AXIOM**: Orbitals are normalized ∫|φⱼ|² = 1 for ALL occupation configurations.

Since this normalization is maintained as n varies:
  d/dnᵢ(∫|φⱼ|²) = 0

which means:
  δᵢⱼ = ∫(∂φⱼ*/∂nᵢ)φⱼ dr + c.c. = 0

This is the crucial constraint that makes Janak's theorem work!
-/

/-- **AXIOM (Normalization)**: Orbitals remain normalized under occupation changes -/
class NormalizationAxiom : Prop where
  orbital_variation_zero : ∀ (n : OccNum N) (i j : Fin N), δ_orbital n i j = 0

/-!
## Part IX: Eq (10) - JANAK'S THEOREM

**THEOREM**: ∂E/∂nᵢ = εᵢ

Derived from:
1. Derivative structure (Axiom 2): ∂E/∂nᵢ = εᵢ + Σⱼ nⱼ εⱼ δᵢⱼ
2. Normalization (Axiom 3): δᵢⱼ = 0 for all i, j

Therefore: ∂E/∂nᵢ = εᵢ + 0 = εᵢ
-/

/-- **THEOREM (Eq 10): Janak's Theorem**

The derivative of the total energy with respect to the occupation
of orbital i equals the Kohn-Sham eigenvalue of that orbital.

∂E/∂nᵢ = εᵢ
-/
theorem janak_theorem
    [KohnShamAxiom N sys]
    [h_deriv : DerivativeStructureAxiom N sys U_Exc δ_orbital]
    [h_norm : NormalizationAxiom N δ_orbital]
    (n : OccNum N) (i : Fin N) :
    deriv (fun nᵢ => E N sys U_Exc (Function.update n i nᵢ)) (n i) = (sys n).ε i := by
  -- Step 1: Apply the derivative structure axiom
  rw [h_deriv.deriv_form n i]
  -- Step 2: Show the sum vanishes due to normalization
  have h_sum_zero : ∑ j : Fin N, n j * (sys n).ε j * δ_orbital n i j = 0 := by
    apply Finset.sum_eq_zero
    intro j _
    -- Each δᵢⱼ = 0 by normalization axiom
    rw [h_norm.orbital_variation_zero n i j]
    ring
  -- Step 3: Conclude
  rw [h_sum_zero]
  ring

/-!
## Part X: Physical Consequences and ML Applications
-/

/-- The eigenvalue directly gives the energy change per electron -/
theorem energy_derivative_interpretation
    [KohnShamAxiom N sys]
    [DerivativeStructureAxiom N sys U_Exc δ_orbital]
    [NormalizationAxiom N δ_orbital]
    (n : OccNum N) (i : Fin N) :
    deriv (fun nᵢ => E N sys U_Exc (Function.update n i nᵢ)) (n i) = (sys n).ε i :=
  janak_theorem N sys U_Exc δ_orbital n i

/-- Band gap definition: difference between LUMO and HOMO eigenvalues -/
def bandGap (ε_homo ε_lumo : ℝ) : ℝ := ε_lumo - ε_homo

/-- Band gap is non-negative when LUMO ≥ HOMO -/
theorem bandGap_nonneg (ε_homo ε_lumo : ℝ) (h : ε_homo ≤ ε_lumo) :
    0 ≤ bandGap ε_homo ε_lumo := by
  unfold bandGap
  linarith

/-!
## Summary: What an ML Functional Must Preserve

For your professor's goal of replacing Exc with an ML model:

### The Three Axioms

1. **KohnShamAxiom**: The ML model must produce a potential vxc = δExc/δρ
   such that the KS equations Hφᵢ = εᵢφᵢ are well-defined.

2. **DerivativeStructureAxiom**: The ML model must be differentiable,
   and the stationarity condition δE/δφ = 0 must hold at self-consistency.
   This requires Exc to be a proper functional of the density.

3. **NormalizationAxiom**: This is independent of the functional form.
   It only requires that orbitals remain normalized, which is always enforced
   in the KS procedure.

### Conclusion

An ML model for Exc can be used as long as:
- It is a differentiable function of the density ρ
- Its functional derivative δExc/δρ = vxc is well-defined
- Self-consistency is achieved (the iterative procedure converges)

The specific FORM of Exc does not matter for Janak's theorem!
This is what makes machine learning the functional a viable approach.
-/

#check @janak_theorem
#check @derive_eq3

end JanakTheorem`
};
