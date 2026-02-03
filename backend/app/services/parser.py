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
    Robust regex-based extraction.
    """
    positions = []
    lines = code.split("\n")
    
    # Track if we're inside a tactic block
    in_tactic_mode = False
    
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
            
        # Check if we're entering tactic mode
        # Matches ":= by", " by ", or just "by" at end/start
        if re.search(r':=\s*by\b', line) or stripped == 'by':
            in_tactic_mode = True
            continue # Don't treat the 'by' line itself as a tactic usually
        
        if not in_tactic_mode:
            continue
        
        # Stop at end of proof (naive check for unindented end or similar)
        # But Lean 4 is indentation sensitive. For now assume everything after 'by' is tactic.
        
        # Skip comments
        if stripped.startswith('--'):
            continue
            
        # Detect common tactics and special lines
        # We accept any line that looks like code in the proof block
        
        # Calculation steps often start with nothing (indent), or '_', or variable
        # Tactics start with keywords.
        
        col = len(line) - len(line.lstrip()) + 1
        
        # Remove partial comments at end of line
        clean_code = stripped.split('--')[0].strip()
        if not clean_code: 
            continue

        positions.append(TacticPosition(
            tactic=clean_code,
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
