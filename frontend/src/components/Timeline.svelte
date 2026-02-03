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
        background: #050510;
        padding: 20px;
        border-top: 1px solid #333;
        font-family: "JetBrains Mono", monospace;
    }

    .controls {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .control-btn {
        background: #0a0a1a;
        border: 1px solid #00f0ff;
        color: #00f0ff;
        width: 36px;
        height: 36px;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 5px rgba(0, 240, 255, 0.1);
    }

    .control-btn:hover:not(:disabled) {
        background: rgba(0, 240, 255, 0.1);
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.8);
        transform: translateY(-1px);
    }

    .control-btn:disabled {
        border-color: #333;
        color: #555;
        cursor: not-allowed;
        box-shadow: none;
    }

    .play-btn {
        border-color: #ff003c;
        color: #ff003c;
        box-shadow: 0 0 5px rgba(255, 0, 60, 0.1);
    }

    .play-btn:hover {
        background: rgba(255, 0, 60, 0.1);
        box-shadow: 0 0 12px rgba(255, 0, 60, 0.4);
        text-shadow: 0 0 8px rgba(255, 0, 60, 0.8);
    }

    .step-counter {
        margin-left: auto;
        font-size: 14px;
        display: flex;
        align-items: baseline;
        gap: 4px;
    }

    .curr {
        color: #fff;
        font-weight: bold;
        font-size: 18px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    .sep {
        color: #555;
    }
    .total {
        color: #888;
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
        background: #222;
        z-index: 1;
    }

    .track-progress {
        position: absolute;
        top: 16px;
        left: 0;
        height: 2px;
        background: #00f0ff;
        z-index: 2;
        box-shadow: 0 0 10px #00f0ff;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .progress-glow {
        position: absolute;
        right: -4px;
        top: -4px;
        width: 10px;
        height: 10px;
        background: #00f0ff;
        border-radius: 50%;
        box-shadow:
            0 0 15px #00f0ff,
            0 0 30px #00f0ff;
    }

    .steps-layer {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 3;
        pointer-events: none; /* Allow clicks to pass through empty space if needed, but buttons catch them */
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
        width: 40px; /* Hit area */
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
        background: #000;
        border: 2px solid #555;
        border-radius: 50%;
        transition: all 0.2s ease;
    }

    .step-marker:hover .step-dot {
        border-color: #fff;
        transform: scale(1.2);
    }

    .step-marker.passed .step-dot {
        background: #00f0ff;
        border-color: #00f0ff;
        box-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
    }

    .step-marker.active .step-dot {
        width: 14px;
        height: 14px;
        background: #fff;
        border-color: #fff;
        box-shadow:
            0 0 15px #fff,
            0 0 30px #00f0ff;
    }

    .step-label {
        margin-top: 4px;
        font-size: 10px;
        color: #555;
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
        color: #fff;
    }

    .step-marker.active .step-label {
        color: #00f0ff;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
    }
</style>
