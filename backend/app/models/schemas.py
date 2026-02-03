from pydantic import BaseModel


class Hypothesis(BaseModel):
    """A hypothesis in the proof context."""
    name: str
    type: str
    is_new: bool = False  # For diff highlighting


class Goal(BaseModel):
    """A goal to prove."""
    id: str
    type: str
    is_new: bool = False


class ProofState(BaseModel):
    """The state of a proof at a given point."""
    goals: list[Goal]
    hypotheses: list[Hypothesis]


class StateDiff(BaseModel):
    """What changed between two states."""
    added_hypotheses: list[str] = []
    removed_hypotheses: list[str] = []
    goals_before: int = 0
    goals_after: int = 0
    description: str = ""  # Future: natural language explanation


class TacticStep(BaseModel):
    """A single tactic step in the proof."""
    index: int
    tactic: str
    line: int
    column: int
    state_before: ProofState
    state_after: ProofState
    diff: StateDiff


class ProofTimeline(BaseModel):
    """The complete timeline of a proof."""
    steps: list[TacticStep]
    source_code: str
    success: bool
    error: str | None = None


class AnalyzeRequest(BaseModel):
    """Request to analyze Lean code."""
    code: str


class AnalyzeResponse(BaseModel):
    """Response from proof analysis."""
    timeline: ProofTimeline | None = None
    error: str | None = None
