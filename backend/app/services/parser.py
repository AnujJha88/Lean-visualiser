"""
Lean Proof Parser

Parses Lean code to extract tactic positions and structure.
"""

import re
from dataclasses import dataclass


@dataclass
class TacticPosition:
    """Location of a tactic in the source code."""
    tactic: str
    line: int        # 1-indexed
    column: int      # 1-indexed
    end_line: int
    end_column: int


def extract_tactic_positions(code: str) -> list[TacticPosition]:
    """
    Extract all tactic positions from Lean code.
    
    This is a simplified parser that looks for common patterns.
    A full implementation would use Lean's actual parser.
    """
    positions = []
    lines = code.split("\n")
    
    # Track if we're inside a tactic block
    in_tactic_mode = False
    
    # Common tactic patterns
    tactic_patterns = [
        r'\b(intro)\s+(\w+)',
        r'\b(intros)\s+([\w\s]+)',
        r'\b(exact)\s+(.+)',
        r'\b(apply)\s+(.+)',
        r'\b(rw)\s*\[(.+?)\]',
        r'\b(rewrite)\s*\[(.+?)\]',
        r'\b(simp)\s*(?:\[(.+?)\])?',
        r'\b(constructor)\b',
        r'\b(cases)\s+(\w+)',
        r'\b(induction)\s+(\w+)',
        r'\b(have)\s+(\w+)\s*:',
        r'\b(let)\s+(\w+)\s*:',
        r'\b(show)\s+(.+)',
        r'\b(assumption)\b',
        r'\b(contradiction)\b',
        r'\b(trivial)\b',
        r'\b(rfl)\b',
        r'\b(ring)\b',
        r'\b(linarith)\b',
        r'\b(omega)\b',
        r'\b(decide)\b',
        r'\b(norm_num)\b',
        r'\b(ext)\b',
        r'\b(funext)\b',
        r'\b(congr)\b',
        r'\b(left)\b',
        r'\b(right)\b',
        r'\b(use)\s+(.+)',
        r'\b(exists)\s+(.+)',
        r'\b(obtain)\s+(.+)',
        r'\b(rcases)\s+(.+)',
        r'·\s*(.+)',  # Bullet point tactic
        r'\|\s*(.+)',  # Alternative bullet
    ]
    
    combined_pattern = '|'.join(f'({p})' for p in tactic_patterns)
    
    for line_num, line in enumerate(lines, 1):
        # Check if we're entering tactic mode
        if ':= by' in line or 'by\n' in line or line.strip() == 'by':
            in_tactic_mode = True
            continue
        
        if not in_tactic_mode:
            continue
        
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith('--'):
            continue
        
        # Look for tactics
        # Simple approach: each non-empty line in tactic mode is a tactic
        col = len(line) - len(line.lstrip()) + 1
        
        # Extract the tactic name for display
        tactic_match = re.search(r'^[\s·\|]*(\w+)', line)
        if tactic_match:
            tactic_name = stripped
            positions.append(TacticPosition(
                tactic=tactic_name,
                line=line_num,
                column=col,
                end_line=line_num,
                end_column=len(line)
            ))
    
    return positions


def is_proof_complete(code: str, diagnostics: list[dict]) -> bool:
    """Check if the proof is complete based on diagnostics."""
    for diag in diagnostics:
        msg = diag.get("message", "").lower()
        if "unsolved goals" in msg or "type mismatch" in msg:
            return False
    return True
