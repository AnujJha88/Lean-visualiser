
import type { ProofTimeline, TacticStep } from "./types";

export interface GraphNode {
    id: string;
    label: string;
    type: 'root' | 'tactic' | 'solved' | 'error';
    stepIndex?: number;
    children: GraphNode[];
    status?: 'active' | 'future' | 'done';
}

/**
 * Transforms a linear proof timeline into a hierarchical graph structure.
 * This is an inferred structure since we don't have explicit Goal ID dependency graphs from Lean yet.
 */
export function buildProofGraph(timeline: ProofTimeline | null): GraphNode {
    const root: GraphNode = {
        id: "root",
        label: "Theorem",
        type: 'root',
        children: [],
        status: 'done'
    };

    if (!timeline) return root;

    // A rough stack to track which node is the "parent" for the current goal.
    // In a simple linear proof, the previous step is the parent of the next.
    // In branching (case split), a node might have multiple children that are siblings.

    // Simplification for V1: Linear chain with "Context" nodes for branches?
    // Let's try to build a tree where each step becomes a child of the previous step
    // UNLESS the previous step caused a branch (goals increased).

    let currentNode = root;
    const nodeMap = new Map<string, GraphNode>();
    nodeMap.set("root", root);

    // This is a naive linear-with-annotations approach for V1.
    // True DAG requiring goal-id tracing is complex without backend support.

    timeline.steps.forEach((step, index) => {
        const node: GraphNode = {
            id: `step-${index}`,
            label: step.tactic,
            type: 'tactic',
            stepIndex: index,
            children: [],
            status: 'future'
        };

        // Attach to current parent
        currentNode.children.push(node);

        // For now, in a standard proof flow, this node becomes the new parent for the next step.
        // If we wanted to show branching physically, we'd need to know if we are working on a new goal 
        // that is a sibling of the previous goal.

        // SIMPLE V1 GRAPH: Just a line for now, but configured as a tree for D3.
        currentNode = node;
    });

    if (timeline.success) {
        currentNode.children.push({
            id: 'qed',
            label: 'Q.E.D.',
            type: 'solved',
            children: []
        });
    } else if (timeline.error) {
        currentNode.children.push({
            id: 'error',
            label: 'Error',
            type: 'error',
            children: []
        });
    }

    return root;
}
