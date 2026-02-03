// Types for the Lean Proof Visualizer

export interface Hypothesis {
    name: string;
    type: string;
    is_new: boolean;
}

export interface Goal {
    id: string;
    type: string;
    is_new: boolean;
}

export interface ProofState {
    goals: Goal[];
    hypotheses: Hypothesis[];
}

export interface StateDiff {
    added_hypotheses: string[];
    removed_hypotheses: string[];
    goals_before: number;
    goals_after: number;
    description: string;
}

export interface TacticStep {
    index: number;
    tactic: string;
    line: number;
    column: number;
    state_before: ProofState;
    state_after: ProofState;
    diff: StateDiff;
    explanation: string;
}

export interface ProofTimeline {
    steps: TacticStep[];
    source_code: string;
    success: boolean;
    error: string | null;
}

export interface AnalyzeResponse {
    timeline: ProofTimeline | null;
    error: string | null;
}
