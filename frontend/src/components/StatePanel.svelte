<script lang="ts">
    import type { ProofState, StateDiff } from "../lib/types";

    export let state: ProofState | null = null;
    export let diff: StateDiff | null = null;
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
        background: #050510;
        height: 100%;
        padding: 20px;
        overflow: auto;
        font-family: "JetBrains Mono", monospace;
        color: #e0e0e0;
        scrollbar-width: thin;
        scrollbar-color: #333 #050510;
    }

    .state-panel::-webkit-scrollbar {
        width: 6px;
    }

    .state-panel::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 3px;
    }

    .diff-header {
        background: rgba(0, 240, 255, 0.05);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00f0ff;
        padding: 10px;
        margin-bottom: 24px;
        font-size: 11px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-left: 3px solid #00f0ff;
        animation: flash 1s ease-out;
    }

    @keyframes flash {
        0% {
            background: rgba(0, 240, 255, 0.2);
        }
        100% {
            background: rgba(0, 240, 255, 0.05);
        }
    }

    .diff-icon {
        font-weight: bold;
    }
    .diff-text {
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .section {
        margin-bottom: 32px;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        border-bottom: 1px solid #222;
        padding-bottom: 8px;
    }

    .section-header h4 {
        margin: 0;
        font-size: 11px;
        letter-spacing: 2px;
        color: #666;
        font-weight: bold;
    }

    .section-header .icon {
        color: #00f0ff;
        font-size: 12px;
    }

    .section.goals .icon {
        color: #ff003c;
    }

    .count {
        margin-left: auto;
        color: #444;
        font-size: 11px;
    }

    .items {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid transparent;
        border-left: 2px solid #333;
        padding: 12px 14px;
        font-size: 12px;
        display: flex;
        align-items: flex-start;
        gap: 10px;
        position: relative;
        transition: all 0.2s ease;
    }

    .item:hover {
        background: rgba(255, 255, 255, 0.04);
        border-left-color: #666;
    }

    .item.new {
        background: rgba(0, 240, 255, 0.03);
        border-left-color: #00f0ff;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.05);
    }

    .section.goals .item.new {
        background: rgba(255, 0, 60, 0.03);
        border-left-color: #ff003c;
        box-shadow: 0 0 10px rgba(255, 0, 60, 0.05);
    }

    .new-indicator {
        position: absolute;
        right: 8px;
        top: 8px;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #00f0ff;
        box-shadow: 0 0 5px #00f0ff;
        animation: pulse 2s infinite;
    }

    .section.goals .new-indicator {
        background: #ff003c;
        box-shadow: 0 0 5px #ff003c;
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
        color: #00f0ff;
        font-weight: bold;
    }
    .item-sep {
        color: #555;
    }
    .item-type {
        color: #ccc;
    }

    .goal-num {
        color: #ff003c;
        font-weight: bold;
    }
    .turnstile {
        color: #666;
        margin-right: 4px;
    }
    .goal-type {
        color: #fff;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }

    .empty {
        color: #444;
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
        color: #555;
        font-size: 12px;
        letter-spacing: 2px;
    }

    .terminal-cursor {
        font-size: 24px;
        color: #00f0ff;
        animation: blink 1s step-end infinite;
        margin-bottom: 16px;
    }

    @keyframes blink {
        50% {
            opacity: 0;
        }
    }

    .success-box {
        border: 1px solid #00f0ff;
        background: rgba(0, 240, 255, 0.05);
        padding: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        color: #00f0ff;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
    }

    .success-icon {
        font-size: 24px;
        text-shadow: 0 0 10px #00f0ff;
    }
    .qed {
        font-weight: bold;
        font-size: 18px;
        letter-spacing: 4px;
        margin-top: 8px;
        text-shadow: 0 0 5px #00f0ff;
    }
</style>
