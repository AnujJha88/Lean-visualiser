<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { TacticStep } from "../lib/types";

    export let steps: TacticStep[] = [];
    export let currentStepIndex: number = 0;
    export let isPlaying: boolean = false;

    const dispatch = createEventDispatcher<{
        select: number;
        play: void;
        pause: void;
    }>();

    function selectStep(index: number) {
        if (index >= 0 && index < steps.length) {
            dispatch("select", index);
        }
    }

    function togglePlay() {
        if (isPlaying) {
            dispatch("pause");
        } else {
            dispatch("play");
        }
    }

    function goToPrevious() {
        selectStep(currentStepIndex - 1);
    }

    function goToNext() {
        selectStep(currentStepIndex + 1);
    }

    $: progress =
        steps.length > 1
            ? (Math.max(0, Math.min(currentStepIndex, steps.length - 1)) /
                  (steps.length - 1)) *
              100
            : 0;
</script>

<div class="timeline-container">
    <!-- Controls -->
    <div class="controls">
        <button
            class="control-btn"
            on:click={goToPrevious}
            disabled={currentStepIndex === 0}
            title="Previous"
        >
            <span class="icon">❮</span>
        </button>

        <button
            class="control-btn play-btn"
            on:click={togglePlay}
            title={isPlaying ? "Pause" : "Play"}
        >
            <span class="icon">{isPlaying ? "⏸" : "▶"}</span>
        </button>

        <button
            class="control-btn"
            on:click={goToNext}
            disabled={currentStepIndex >= steps.length - 1}
            title="Next"
        >
            <span class="icon">❯</span>
        </button>

        <div class="step-counter">
            <span class="curr">{currentStepIndex + 1}</span>
            <span class="sep">/</span>
            <span class="total">{steps.length}</span>
        </div>
    </div>

    <!-- Timeline track -->
    <div class="timeline-track">
        <div class="track-line"></div>
        <div class="track-progress" style="width: {progress}%">
            <div class="progress-glow"></div>
        </div>

        <div class="steps-layer">
            {#each steps as step, i}
                <button
                    class="step-marker"
                    class:active={i === currentStepIndex}
                    class:passed={i < currentStepIndex}
                    on:click={() => selectStep(i)}
                    title={step.tactic}
                    style="left: {steps.length > 1
                        ? (i / (steps.length - 1)) * 100
                        : 0}%"
                >
                    <div class="dot-wrapper">
                        <div class="step-dot"></div>
                    </div>
                    <div class="step-label">
                        {step.tactic.split(" ")[0].replace("·", "").trim()}
                    </div>
                </button>
            {/each}
        </div>
    </div>
</div>

<style>
    .timeline-container {
        background: var(--bg-timeline);
        padding: 20px;
        border-top: 1px solid var(--border-color);
        font-family: "JetBrains Mono", monospace;
    }

    .controls {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .control-btn {
        background: var(--bg-app);
        border: 1px solid var(--accent-color);
        color: var(--accent-color);
        width: 36px;
        height: 36px;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 5px rgba(var(--accent-color-rgb), 0.1);
    }

    .control-btn:hover:not(:disabled) {
        background: rgba(var(--accent-color-rgb), 0.1);
        box-shadow: 0 0 12px rgba(var(--accent-color-rgb), 0.4);
        text-shadow: 0 0 8px rgba(var(--accent-color-rgb), 0.8);
        transform: translateY(-1px);
    }

    .control-btn:disabled {
        border-color: var(--border-color);
        color: var(--text-muted);
        cursor: not-allowed;
        box-shadow: none;
    }

    .play-btn {
        border-color: var(--accent-secondary);
        color: var(--accent-secondary);
        box-shadow: 0 0 5px rgba(var(--accent-secondary-rgb), 0.1);
    }

    .play-btn:hover {
        background: rgba(var(--accent-secondary-rgb), 0.1);
        box-shadow: 0 0 12px rgba(var(--accent-secondary-rgb), 0.4);
        text-shadow: 0 0 8px rgba(var(--accent-secondary-rgb), 0.8);
    }

    .step-counter {
        margin-left: auto;
        font-size: 14px;
        display: flex;
        align-items: baseline;
        gap: 4px;
    }

    .curr {
        color: var(--text-primary);
        font-weight: bold;
        font-size: 18px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    .sep {
        color: var(--text-muted);
    }
    .total {
        color: var(--text-secondary);
    }

    .timeline-track {
        position: relative;
        height: 48px;
        margin-top: 10px;
    }

    .track-line {
        position: absolute;
        top: 16px;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--border-color);
        z-index: 1;
    }

    .track-progress {
        position: absolute;
        top: 16px;
        left: 0;
        height: 2px;
        background: var(--accent-color);
        z-index: 2;
        box-shadow: 0 0 10px var(--accent-color);
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .progress-glow {
        position: absolute;
        right: -4px;
        top: -4px;
        width: 10px;
        height: 10px;
        background: var(--accent-color);
        border-radius: 50%;
        box-shadow:
            0 0 15px var(--accent-color),
            0 0 30px var(--accent-color);
    }

    .steps-layer {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 3;
        pointer-events: none;
    }

    .step-marker {
        position: absolute;
        top: 0;
        transform: translateX(-50%);
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        pointer-events: auto;
        width: 40px;
    }

    .dot-wrapper {
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .step-dot {
        width: 8px;
        height: 8px;
        background: var(--bg-app);
        border: 2px solid var(--text-muted);
        border-radius: 50%;
        transition: all 0.2s ease;
    }

    .step-marker:hover .step-dot {
        border-color: var(--text-primary);
        transform: scale(1.2);
    }

    .step-marker.passed .step-dot {
        background: var(--accent-color);
        border-color: var(--accent-color);
        box-shadow: 0 0 8px rgba(var(--accent-color-rgb), 0.4);
    }

    .step-marker.active .step-dot {
        width: 14px;
        height: 14px;
        background: var(--text-primary);
        border-color: var(--text-primary);
        box-shadow:
            0 0 15px var(--text-primary),
            0 0 30px var(--accent-color);
    }

    .step-label {
        margin-top: 4px;
        font-size: 10px;
        color: var(--text-muted);
        opacity: 0;
        transform: translateY(-5px);
        transition: all 0.2s ease;
        text-shadow: 0 0 5px rgba(0, 0, 0, 1);
        background: rgba(0, 0, 0, 0.8);
        padding: 2px 4px;
        border-radius: 2px;
    }

    .step-marker:hover .step-label,
    .step-marker.active .step-label {
        opacity: 1;
        transform: translateY(0);
        color: var(--text-primary);
    }

    .step-marker.active .step-label {
        color: var(--accent-color);
        text-shadow: 0 0 8px rgba(var(--accent-color-rgb), 0.6);
    }
</style>
