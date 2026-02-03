"""
State Diff Computation

Computes the differences between proof states.
"""

from ..models import ProofState, StateDiff, Hypothesis, Goal


def compute_diff(before: ProofState, after: ProofState) -> StateDiff:
    """
    Compute what changed between two proof states.
    """
    # Get hypothesis names
    before_hyps = {h.name for h in before.hypotheses}
    after_hyps = {h.name for h in after.hypotheses}
    
    added = list(after_hyps - before_hyps)
    removed = list(before_hyps - after_hyps)
    
    # Build description
    parts = []
    if added:
        parts.append(f"Added: {', '.join(added)}")
    if removed:
        parts.append(f"Removed: {', '.join(removed)}")
    if len(after.goals) < len(before.goals):
        parts.append(f"Closed {len(before.goals) - len(after.goals)} goal(s)")
    elif len(after.goals) > len(before.goals):
        parts.append(f"Created {len(after.goals) - len(before.goals)} new goal(s)")
    
    return StateDiff(
        added_hypotheses=added,
        removed_hypotheses=removed,
        goals_before=len(before.goals),
        goals_after=len(after.goals),
        description=" | ".join(parts) if parts else "State unchanged"
    )


def mark_new_items(before: ProofState, after: ProofState) -> ProofState:
    """
    Return the 'after' state with is_new flags set for new items.
    """
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
    
    return ProofState(
        goals=marked_goals,
        hypotheses=marked_hypotheses
    )
