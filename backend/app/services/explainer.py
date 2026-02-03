import re

def explain_tactic(tactic: str) -> str:
    """
    Generate a natural language explanation for a Lean 4 tactic.
    """
    t = tactic.strip()
    
    # Intro
    if m := re.match(r'^intro\s+(.+)', t):
        vars = m.group(1).replace(' ', ', ')
        return f"Introduces new variable(s) or hypothesis: {vars}"
    
    if m := re.match(r'^intros\s*(.*)', t):
        vars = m.group(1).strip()
        if vars:
            return f"Introduces variables: {vars}"
        return "Introduces all available variables"

    # Rewrites
    if m := re.match(r'^(?:rw|rewrite)\s*\[(.+)\]', t):
        rules = m.group(1)
        return f"Rewrites the goal using: {rules}"
    
    if m := re.match(r'^(?:rw|rewrite)\s+at\s+(\w+)', t):
        loc = m.group(1)
        return f"Rewrites hypothesis {loc}"

    # Application
    if m := re.match(r'^apply\s+(.+)', t):
        rule = m.group(1)
        return f"Applies the rule {rule} to split or solve the goal"
    
    if m := re.match(r'^exact\s+(.+)', t):
        term = m.group(1)
        return f"Proves the goal exactly using {term}"

    # Structural
    if t == 'constructor':
        return "Splits the goal into subgoals (e.g. for AND/IFF)"
    
    if m := re.match(r'^cases\s+(\w+)', t):
        var = m.group(1)
        return f"Splits the proof into cases based on {var}"
    
    if m := re.match(r'^induction\s+(\w+)', t):
        var = m.group(1)
        return f"Starts mathematical induction on {var}"

    # Simplification
    if t.startswith('simp'):
        return "Simplifies the goal using standard rewriting rules"
    
    if t == 'rfl':
        return "Proves equality by reflexivity (x = x)"
    
    # Calculation
    if t.startswith('calc'):
        return "Starts a calculation block"
    
    if t.startswith('_') or t.startswith('...'):
        return "Continues the calculation step"

    # Default fallback
    return f"Executes tactic: {t.split()[0]}"
