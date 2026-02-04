import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.explainer import explain_tactic
from app.models.schemas import ProofState, Goal, Hypothesis

def test_explainer():
    print("Testing Explainer Improvements...\n")

    # Scenario 1: Intro
    before = ProofState(
        goals=[Goal(id="1", type="A → B")],
        hypotheses=[]
    )
    after = ProofState(
        goals=[Goal(id="1", type="B")],
        hypotheses=[Hypothesis(name="h", type="A", is_new=True)]
    )
    print(f"Intro: {explain_tactic('intro h', before, after)}")

    # Scenario 2: Rewrite
    before = ProofState(
        goals=[Goal(id="1", type="a + b = c")],
        hypotheses=[]
    )
    after = ProofState(
        goals=[Goal(id="1", type="b + a = c")],
        hypotheses=[]
    )
    print(f"Rewrite: {explain_tactic('rw [add_comm]', before, after)}")

    # Scenario 3: Apply (splitting)
    before = ProofState(
        goals=[Goal(id="1", type="A ∧ B")],
        hypotheses=[]
    )
    after = ProofState(
        goals=[Goal(id="1", type="A"), Goal(id="2", type="B")],
        hypotheses=[]
    )
    print(f"Apply (split): {explain_tactic('apply And.intro', before, after)}")

    # Scenario 4: Simp
    before = ProofState(
        goals=[Goal(id="1", type="x + 0 = x")],
        hypotheses=[]
    )
    after = ProofState(
        goals=[Goal(id="1", type="True")],
        hypotheses=[]
    )
    print(f"Simp: {explain_tactic('simp', before, after)}")
    
    # Scenario 5: Exact
    print(f"Exact: {explain_tactic('exact h', before, after)}")

    # Scenario 6: Have
    print(f"Have: {explain_tactic('have h2 : A := by ...')}")

if __name__ == "__main__":
    test_explainer()
