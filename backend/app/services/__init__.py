# Services package
from .lean_client import Lean4WebClient, get_lean_client, parse_goal_state
from .parser import extract_tactic_positions, TacticPosition
from .differ import compute_diff, mark_new_items
from .explainer import explain_tactic

__all__ = [
    "Lean4WebClient",
    "get_lean_client",
    "parse_goal_state",
    "extract_tactic_positions", 
    "TacticPosition",
    "compute_diff",
    "mark_new_items",
    "explain_tactic",
]
