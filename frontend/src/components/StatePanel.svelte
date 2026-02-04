<script lang="ts">
    import type { ProofState, StateDiff } from "../lib/types";

    export let state: ProofState | null = null;
    export let diff: StateDiff | null = null;
    export let explanation: string = "";
    export let title: string = "Proof State";
</script>

<div class="state-panel">
    <!-- Info Bar / Diff Header -->
    {#if diff?.description}
        <div class="diff-header">
            <span class="diff-icon">ℹ</span>
            <span class="diff-text">{diff.description}</span>
        </div>
    {/if}

    {#if explanation}
        <div class="explanation-box">
            <span class="exp-icon">➜</span>
            <span class="exp-text">{explanation}</span>
        </div>
    {/if}

    {#if state}
        <!-- Hypotheses -->
        <div class="section hypotheses">
            <div class="section-header">
                <span class="icon">⊢</span>
                <h4>CONTEXT</h4>
                <span class="count">[{state.hypotheses.length}]</span>
            </div>

            {#if state.hypotheses.length > 0}
                <div class="items">
                    {#each state.hypotheses as hyp}
                        <div class="item" class:new={hyp.is_new}>
                            {#if hyp.is_new}
                                <div class="new-indicator"></div>
                            {/if}
                            <span class="item-name">{hyp.name}</span>
                            <span class="item-sep">:</span>
                            <span class="item-type">{hyp.type}</span>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="empty">-- Empty Context --</div>
            {/if}
        </div>

        <!-- Goals -->
        <div class="section goals">
            <div class="section-header">
                <span class="icon">TARGET</span>
                <h4>GOALS</h4>
                <span class="count">[{state.goals.length}]</span>
            </div>

            {#if state.goals.length > 0}
                <div class="items">
                    {#each state.goals as goal, i}
                        <div class="item goal" class:new={goal.is_new}>
                            {#if goal.is_new}
                                <div class="new-indicator"></div>
                            {/if}
                            <span class="goal-num">#{i + 1}</span>
                            <span class="turnstile">⊢</span>
                            <span class="item-type goal-type">{goal.type}</span>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="success-box">
                    <span class="success-icon">✓</span>
                    <span>NO GOALS REMAINING</span>
                    <span class="qed">Q.E.D.</span>
                </div>
            {/if}
        </div>
    {:else}
        <div class="empty-state">
            <div class="terminal-cursor">█</div>
            <p>WAITING FOR ANALYSIS...</p>
        </div>
    {/if}
</div>

<style>
    .state-panel {
        background: transparent;
        height: 100%;
        padding: 20px;
        overflow: auto;
        font-family: "JetBrains Mono", monospace;
        color: var(--text-primary);
        scrollbar-width: thin;
        scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
        transition: color 0.3s;
    }

    .state-panel::-webkit-scrollbar {
        width: 6px;
    }

    .state-panel::-webkit-scrollbar-thumb {
        background: var(--scrollbar-thumb);
        border-radius: 3px;
    }

    .diff-header {
        background: var(--success-bg);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: var(--accent-color);
        padding: 10px;
        margin-bottom: 24px;
        font-size: 11px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-left: 3px solid var(--accent-color);
        animation: flash 1s ease-out;
    }

    @keyframes flash {
        0% {
            background: rgba(0, 240, 255, 0.2);
        }
        100% {
            background: var(--success-bg);
        }
    }

    .diff-icon {
        font-weight: bold;
    }

    .diff-text {
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .explanation-box {
        background: var(--item-bg);
        border-left: 3px solid var(--text-muted);
        padding: 12px;
        margin-bottom: 24px;
        font-size: 13px;
        color: var(--text-primary);
        display: flex;
        gap: 10px;
        align-items: center;
        font-style: italic;
    }

    .explanation-box .exp-icon {
        color: var(--text-muted);
        font-weight: bold;
    }

    .section {
        margin-bottom: 32px;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 8px;
    }

    .section-header h4 {
        margin: 0;
        font-size: 11px;
        letter-spacing: 2px;
        color: var(--text-muted);
        font-weight: bold;
    }

    .section-header .icon {
        color: var(--accent-color);
        font-size: 12px;
    }

    .section.goals .icon {
        color: var(--accent-secondary);
    }

    .count {
        margin-left: auto;
        color: var(--text-muted);
        font-size: 11px;
    }

    .items {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .item {
        background: var(--item-bg);
        border: 1px solid transparent;
        border-left: 2px solid var(--border-color);
        padding: 12px 14px;
        font-size: 12px;
        display: flex;
        align-items: flex-start;
        gap: 10px;
        position: relative;
        transition: all 0.2s ease;
    }

    .item:hover {
        background: var(--item-bg-hover);
        border-left-color: var(--text-secondary);
    }

    .item.new {
        background: var(--diff-added-bg);
        border-left-color: var(--accent-color);
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.05);
    }

    .section.goals .item.new {
        background: var(--diff-removed-bg);
        border-left-color: var(--accent-secondary);
        box-shadow: 0 0 10px rgba(255, 0, 60, 0.05);
    }

    .new-indicator {
        position: absolute;
        right: 8px;
        top: 8px;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent-color);
        box-shadow: 0 0 5px var(--accent-color);
        animation: pulse 2s infinite;
    }

    .section.goals .new-indicator {
        background: var(--accent-secondary);
        box-shadow: 0 0 5px var(--accent-secondary);
    }

    @keyframes pulse {
        0% {
            opacity: 0.5;
            transform: scale(0.8);
        }
        50% {
            opacity: 1;
            transform: scale(1.2);
        }
        100% {
            opacity: 0.5;
            transform: scale(0.8);
        }
    }

    .item-name {
        color: var(--accent-color);
        font-weight: bold;
    }
    .item-sep {
        color: var(--text-muted);
    }
    .item-type {
        color: var(--text-secondary);
    }

    .goal-num {
        color: var(--accent-secondary);
        font-weight: bold;
    }
    .turnstile {
        color: var(--text-muted);
        margin-right: 4px;
    }
    .goal-type {
        color: var(--text-primary);
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }

    .empty {
        color: var(--text-muted);
        font-size: 11px;
        padding: 10px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .empty-state {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--text-muted);
        font-size: 12px;
        letter-spacing: 2px;
    }

    .terminal-cursor {
        font-size: 24px;
        color: var(--accent-color);
        animation: blink 1s step-end infinite;
        margin-bottom: 16px;
    }

    @keyframes blink {
        50% {
            opacity: 0;
        }
    }

    .success-box {
        border: 1px solid var(--accent-color);
        background: var(--success-bg);
        padding: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        color: var(--accent-color);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
    }

    .success-icon {
        font-size: 24px;
        text-shadow: 0 0 10px var(--accent-color);
    }
    .qed {
        font-weight: bold;
        font-size: 18px;
        letter-spacing: 4px;
        margin-top: 8px;
        text-shadow: 0 0 5px var(--accent-color);
    }
</style>
