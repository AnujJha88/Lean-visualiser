import re
import httpx
from typing import Optional
from ..models.schemas import ProofState, Hypothesis, Goal
from ..config import get_settings

async def explain_tactic(tactic: str, before: Optional[ProofState] = None, after: Optional[ProofState] = None) -> str:
    """
    Generate a natural language explanation for a Lean 4 tactic using context.
    
    Args:
        tactic: The tactic string (e.g., "intro h")
        before: The proof state before the tactic.
        after: The proof state after the tactic.
    """

    t = tactic.strip()
    settings = get_settings()

    # Try LLM if Key is present
    if settings.openai_api_key:
        try:
            explanation = await explain_with_llm(t, before, after, settings.openai_api_key, settings.openai_model)
            if explanation:
                return explanation
        except Exception as e:
            print(f"LLM Explanation failed: {e}")
            # Fallback to regex
            pass
    
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
    # Rewrites (Advanced)
    if m := re.match(r'^(?:rw|rewrite|erw)\s*(?:\[(.*)\])?\s*(.*)', t):
        rules_str = m.group(1)
        rest = m.group(2)
        
        # Parse location
        loc = "the goal"
        if m_at := re.search(r'\s+at\s+(\S+)', rest):
             loc = f"hypothesis `{m_at.group(1)}`"
             
        # Parse rules sequence
        if rules_str:
            rules = [r.strip() for r in rules_str.split(',')]
            desc = " then ".join([f"`{r}`" for r in rules])
            return f"Rewrites {loc} using {desc}"
        else:
             # Handle single rule without brackets if standard regex missed it
             rule = rest.split(' at ')[0].strip()
             return f"Rewrites {loc} using `{rule}`"

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
    # Have / Let / Suffices / Obtain
    if m := re.match(r'^(?:have|let)\s+(\w+)\s*:', t):
        return f"Establishes intermediate fact `{m.group(1)}`"
    
    if m := re.match(r'^suffices\s+(.+?)(?:\s+by)?$', t):
        return f"Claims it suffices to prove `{m.group(1)}` to solve the goal"

    if m := re.match(r'^obtain\s+(.+?)\s*:=\s*', t):
        return f"Extards witness `{m.group(1)}` from an existential hypothesis"
        
    # Generic fallback with diff
    before_goal = get_goal_type(before)
    after_goal = get_goal_type(after)
    if before_goal and after_goal and before_goal != after_goal:
        return f"Executes `{t.split()[0]}`, changing goal to `{after_goal}`"

    return f"Executes `{t}`"


async def explain_with_llm(tactic: str, before: Optional[ProofState], after: Optional[ProofState], api_key: str, model: str) -> Optional[str]:
    """Call OpenAI API to explain the tactic."""
    
    # Construct context
    context = f"Tactic: {tactic}\n"
    if before and before.goals:
        context += f"Before Goal: {before.goals[0].type}\n"
    if after and after.goals:
        context += f"After Goal: {after.goals[0].type}\n"
        
    prompt = f"""
    Explain this Lean 4 tactic step in simple, high-level terms (1 sentence max).
    Focus on the "Why" and the mathematical intuition. Use "Vibe Coding" slang / casual tone if appropriate but keep it accurate.
    Do not mention "Lean 4" explicitly.
    
    {context}
    """
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful math tutor explaining formal proofs."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 60,
                "temperature": 0.7
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
            
    return None
