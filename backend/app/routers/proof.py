"""
Proof Analysis Router

API endpoints for analyzing Lean proofs.
"""

from fastapi import APIRouter

from ..models import (
    AnalyzeRequest,
    AnalyzeResponse,
    ProofTimeline,
    TacticStep,
    ProofState,
    Goal,
    Hypothesis,
    StateDiff,
)
from ..services import (
    get_lean_client,
    extract_tactic_positions,
    compute_diff,
    parse_goal_state,
)


router = APIRouter(prefix="/api/proof", tags=["proof"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_proof(request: AnalyzeRequest):
    """
    Analyze Lean code and return the proof timeline.
    
    Connects to Lean4Web via WebSocket to get real proof states.
    """
    try:
        client = get_lean_client()
        
        # Get real analysis from Lean4Web
        lean_result = await client.analyze_code(request.code)
        
        # Extract tactic positions from the code
        positions = extract_tactic_positions(request.code)
        
        if not positions:
            return AnalyzeResponse(
                timeline=ProofTimeline(
                    steps=[],
                    source_code=request.code,
                    success=lean_result["success"],
                    error="No tactics found in code. Make sure you're using tactic mode (`:= by`)."
                )
            )
        
        # Build timeline steps from Lean's response
        steps = []
        
        # Parse the theorem signature to get initial goal
        initial_goal = extract_goal_from_code(request.code)
        
        # Map goals from Lean to positions
        goal_map = {}
        for goal_info in lean_result.get("goals", []):
            line = goal_info.get("line", 0)
            goal_map[line] = goal_info
        
        current_state = ProofState(
            goals=[Goal(id="1", type=initial_goal, is_new=False)],
            hypotheses=[]
        )
        
        for i, pos in enumerate(positions):
            state_before = current_state
            
            # Try to get real goal state from Lean
            goal_info = goal_map.get(pos.line)
            
            if goal_info and goal_info.get("rendered"):
                # Parse the rendered goal state
                rendered = goal_info["rendered"]
                hypotheses, goals = parse_goal_state(rendered)
                
                state_after = ProofState(
                    goals=[Goal(id=str(j+1), type=g, is_new=False) for j, g in enumerate(goals)],
                    hypotheses=[parse_hypothesis(h) for h in hypotheses]
                )
            elif goal_info and goal_info.get("goals"):
                # Use goals array directly
                goals_list = goal_info["goals"]
                state_after = ProofState(
                    goals=[Goal(id=str(j+1), type=str(g), is_new=False) for j, g in enumerate(goals_list)],
                    hypotheses=list(state_before.hypotheses)
                )
            else:
                # Fallback: simulate based on tactic
                state_after = simulate_tactic_effect(pos.tactic, state_before, i)
            
            # Mark new items
            state_after = mark_new_items(state_before, state_after)
            
            # Compute diff
            diff = compute_diff(state_before, state_after)
            
            steps.append(TacticStep(
                index=i,
                tactic=pos.tactic,
                line=pos.line,
                column=pos.column,
                state_before=state_before,
                state_after=state_after,
                diff=diff
            ))
            
            current_state = state_after
        
        # Get error messages from diagnostics
        error_msgs = [
            d.get("message", "Unknown error") 
            for d in lean_result.get("diagnostics", [])
            if d.get("severity") == 1
        ]
        
        return AnalyzeResponse(
            timeline=ProofTimeline(
                steps=steps,
                source_code=request.code,
                success=lean_result["success"],
                error="; ".join(error_msgs) if error_msgs else None
            )
        )
        
    except Exception as e:
        return AnalyzeResponse(
            error=f"Analysis failed: {str(e)}"
        )


def parse_hypothesis(hyp_str: str) -> Hypothesis:
    """Parse a hypothesis string like 'h : A ∧ B' into a Hypothesis."""
    parts = hyp_str.split(":", 1)
    if len(parts) == 2:
        return Hypothesis(name=parts[0].strip(), type=parts[1].strip(), is_new=False)
    return Hypothesis(name=hyp_str, type="", is_new=False)


def mark_new_items(before: ProofState, after: ProofState) -> ProofState:
    """Mark items that are new in the 'after' state."""
    before_hyp_names = {h.name for h in before.hypotheses}
    before_goal_types = {g.type for g in before.goals}
    
    marked_hypotheses = [
        Hypothesis(
            name=h.name,
            type=h.type,
            is_new=(h.name not in before_hyp_names)
        )
        for h in after.hypotheses
    ]
    
    marked_goals = [
        Goal(
            id=g.id,
            type=g.type,
            is_new=(g.type not in before_goal_types)
        )
        for g in after.goals
    ]
    
    return ProofState(goals=marked_goals, hypotheses=marked_hypotheses)


def extract_goal_from_code(code: str) -> str:
    """Extract the goal type from theorem signature."""
    import re
    
    # Look for pattern: theorem/lemma name ... : TYPE := by
    match = re.search(r'(?:theorem|lemma|example)\s+\w*[^:]*:\s*(.+?)\s*:=\s*by', code, re.DOTALL)
    if match:
        goal = match.group(1).strip()
        # Clean up whitespace
        goal = ' '.join(goal.split())
        return goal
    
    return "(goal)"


def simulate_tactic_effect(tactic: str, state: ProofState, step_index: int) -> ProofState:
    """
    Simulate the effect of a tactic on the proof state.
    Fallback when real Lean server doesn't provide goal info.
    """
    tactic_clean = tactic.strip()
    tactic_lower = tactic_clean.lower()
    
    # Remove bullet points
    if tactic_clean.startswith('·') or tactic_clean.startswith('|'):
        tactic_clean = tactic_clean[1:].strip()
        tactic_lower = tactic_clean.lower()
    
    new_hypotheses = list(state.hypotheses)
    new_goals = list(state.goals)
    
    # intro - introduces hypothesis
    if tactic_lower.startswith('intro ') or tactic_lower.startswith('intros '):
        parts = tactic_clean.split()[1:]
        for name in parts:
            name = name.strip()
            if name:
                new_hypotheses.append(Hypothesis(name=name, type="(introduced)", is_new=True))
                if new_goals:
                    new_goals[0] = Goal(id="1", type=update_goal_after_intro(new_goals[0].type), is_new=True)
    
    # constructor - splits goal
    elif 'constructor' in tactic_lower:
        if new_goals:
            old_type = new_goals[0].type
            left, right = split_goal(old_type)
            new_goals = [
                Goal(id="1", type=left, is_new=True),
                Goal(id="2", type=right, is_new=True)
            ] + new_goals[1:]
    
    # exact / rfl / trivial - closes goal
    elif any(t in tactic_lower for t in ['exact ', 'exact\n', 'rfl', 'trivial', 'assumption']):
        if new_goals:
            new_goals = new_goals[1:]
    
    # simp - may close or simplify
    elif 'simp' in tactic_lower:
        if new_goals:
            new_goals = new_goals[1:]
    
    return ProofState(goals=new_goals, hypotheses=new_hypotheses)


def update_goal_after_intro(goal: str) -> str:
    """Update goal after intro."""
    if '→' in goal:
        parts = goal.split('→', 1)
        return parts[1].strip() if len(parts) > 1 else "(remaining)"
    if '->' in goal:
        parts = goal.split('->', 1)
        return parts[1].strip() if len(parts) > 1 else "(remaining)"
    return "(remaining goal)"


def split_goal(goal: str) -> tuple[str, str]:
    """Split a conjunction goal."""
    if '∧' in goal:
        parts = goal.split('∧', 1)
        return parts[0].strip(), parts[1].strip() if len(parts) > 1 else "(right)"
    return "(subgoal 1)", "(subgoal 2)"
