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
      | intro x qx =>
        exists x
        apply Or.inr
        exact qx`
};
