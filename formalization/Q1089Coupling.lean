import Std
namespace CoupledLottery
open Lean.Grind Std

variable {R I : Type} [CommRing R] [LE R] [LT R] [IsLinearOrder R]
    [LawfulOrderLT R] [OrderedRing R]

def mean (weight value : I → R) : List I → R
  | [] => 0
  | i :: tail => weight i * value i + mean weight value tail

theorem monotone (atoms : List I) (w x y : I → R)
    (h : ∀ i ∈ atoms, 0 ≤ w i ∧ (0 < w i → x i ≤ y i)) :
    mean w x atoms ≤ mean w y atoms := by
  induction atoms with
  | nil => exact Std.le_refl _
  | cons i tail ih =>
    have head := h i (by simp)
    have lower := ih (by grind)
    simp only [mean]
    by_cases positive : 0 < w i
    · have step := OrderedRing.mul_le_mul_of_nonneg_left (head.2 positive) head.1
      grind
    · have zero : w i = 0 := by grind
      rw [zero]
      grind

theorem equal_at_positive_atoms (atoms : List I) (w x y : I → R)
    (h : ∀ i ∈ atoms, 0 ≤ w i ∧ (0 < w i → x i ≤ y i))
    (eq : mean w x atoms = mean w y atoms) :
    ∀ i ∈ atoms, 0 < w i → x i = y i := by
  induction atoms with
  | nil => simp
  | cons i tail ih =>
    have hh := h i (by simp)
    have bound : ∀ j ∈ tail, 0 ≤ w j ∧ (0 < w j → x j ≤ y j) := by grind
    have tailLe := monotone tail w x y bound
    simp only [mean] at eq
    have onHead : 0 < w i → x i = y i := by
      intro pos
      have le := hh.2 pos
      apply Classical.byContradiction
      intro neq
      have prod := OrderedRing.mul_pos pos (show 0 < y i - x i by grind)
      grind
    have headMass : w i * x i = w i * y i := by
      by_cases pos : 0 < w i
      · rw [onHead pos]
      · have zero : w i = 0 := by grind
        rw [zero]
        grind
    have tailEq : mean w x tail = mean w y tail := by grind
    intro j hj pos
    rcases List.mem_cons.mp hj with rfl | mem
    · exact onHead pos
    · exact ih bound tailEq _ mem pos

/-- Applying the scalar result coordinatewise gives identity of the paired
outcomes at every positive-mass atom, for any number of coordinates. -/
theorem same_outcome {C : Type} (atoms : List I) (w : I → R) (x y : I → C → R)
    (h : ∀ c i, i ∈ atoms → 0 ≤ w i ∧ (0 < w i → x i c ≤ y i c))
    (eq : ∀ c, mean w (fun i => x i c) atoms = mean w (fun i => y i c) atoms) :
    ∀ i ∈ atoms, 0 < w i → x i = y i := by
  intro i mem pos
  funext c
  exact equal_at_positive_atoms atoms w _ _ (h c) (eq c) i mem pos
#print axioms same_outcome
end CoupledLottery
