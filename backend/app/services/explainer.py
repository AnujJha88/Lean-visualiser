import re
from typing import Optional
from ..models.schemas import ProofState, Hypothesis, Goal

def explain_tactic(tactic: str, before: Optional[ProofState] = None, after: Optional[ProofState] = None) -> str:
    """
    Generate a natural language explanation for a Lean 4 tactic using context.
    
    Args:
        tactic: The tactic string (e.g., "intro h")
        before: The proof state before the tactic.
        after: The proof state after the tactic.
    """
    t = tactic.strip()
    
    # Helper to get goal types
    def get_goal_type(state: Optional[ProofState], index: int = 0) -> str:
        if state and state.goals and len(state.goals) > index:
            return state.goals[index].type
        return ""

    # Intro
    if m := re.match(r'^intro\s+(.+)', t):
        vars_str = m.group(1)
        if after:
            # Find new hypotheses in 'after' state
            new_hyps = [h for h in after.hypotheses if h.is_new]
            if new_hyps:
                desc = ", ".join([f"`{h.name}` ({h.type})" for h in new_hyps])
                return f"Introduces {desc}"
        return f"Introduces variable(s): {vars_str}"
    
    if m := re.match(r'^intros\s*(.*)', t):
        if after:
            new_hyps = [h for h in after.hypotheses if h.is_new]
            if new_hyps:
                desc = ", ".join([f"`{h.name}`" for h in new_hyps])
                return f"Introduces variables: {desc}"
        return "Introduces variables"

    # Rewrites
    if m := re.match(r'^(?:rw|rewrite)\s*\[(.+)\]', t):
        rules = m.group(1)
        if m_at := re.search(r'\s+at\s+(\w+)', t):
            loc = m_at.group(1)
            return f"Rewrites hypothesis `{loc}` using {rules}"
        
        # Check if we can see the change
        before_goal = get_goal_type(before)
        after_goal = get_goal_type(after)
        if before_goal and after_goal and before_goal != after_goal:
             return f"Rewrites goal using {rules}, changing it from `{before_goal}` to `{after_goal}`"
             
        return f"Rewrites the goal using {rules}"
    
    if m := re.match(r'^(?:rw|rewrite)\s+(.+)', t):
        # Handle single rewrite
        rule = m.group(1).split(' at ')[0].strip()
        return f"Rewrites using {rule}"

    # Application
    if m := re.match(r'^apply\s+(.+)', t):
        rule = m.group(1)
        if before and after:
            new_goals_count = len(after.goals)
            old_goals_count = len(before.goals)
            if new_goals_count > old_goals_count:
                extra = new_goals_count - old_goals_count + 1
                return f"Applies `{rule}`, splitting the goal into {extra} subgoals"
        return f"Applies `{rule}`"
    
    if m := re.match(r'^exact\s+(.+)', t):
        term = m.group(1)
        return f"Solves the goal exactly using `{term}`"
    
    if t.startswith('refine'):
        return "Refines the goal (filling in parts of the proof)"

    # Structural
    if t == 'constructor':
        if after and len(after.goals) > 1:
            return "Splits the goal into subgoals (AND/IFF introduction)"
        return "Applies constructor"
    
    if m := re.match(r'^cases\s+(\w+)', t):
        var = m.group(1)
        if after:
             return f"Splits into cases considering `{var}`"
        return f"Splits into cases on {var}"
        
    if m := re.match(r'^induction\s+(\w+)', t):
        var = m.group(1)
        return f"Starts induction on `{var}`"

    # Simplification
    if t.startswith('simp') or t.startswith('dsimp'):
        before_goal = get_goal_type(before)
        after_goal = get_goal_type(after)
        if before_goal and after_goal and before_goal != after_goal:
            return f"Simplifies goal to `{after_goal}`"
        if not after or not after.goals:
             return "Simplifies and solves the goal"
        return "Simplifies the goal"
    
    if t == 'rfl':
        return "Proves by reflexivity (LHS = RHS)"
        
    if t == 'trivial':
        return "Solves the goal trivially"
        
    if t == 'assumption':
        return "Solves the goal using a known hypothesis"

    # Calculation
    if t.startswith('calc'):
        return "Starts a step-by-step calculation"
    
    if t.startswith('_') or t.startswith('...'):
        if after:
             return f"Calculates: `{get_goal_type(after)}`"
        return "Calculation step"
        
    # Have / Let
    if m := re.match(r'^(?:have|let)\s+(\w+)\s*:', t):
        name = m.group(1)
        return f"States intermediate result `{name}`"
        
    # Generic fallback with diff
    before_goal = get_goal_type(before)
    after_goal = get_goal_type(after)
    if before_goal and after_goal and before_goal != after_goal:
        return f"Executes `{t.split()[0]}`, changing goal to `{after_goal}`"

    return f"Executes `{t}`"
