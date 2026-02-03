<script lang="ts">
  import Editor from "./components/Editor.svelte";
  import Timeline from "./components/Timeline.svelte";
  import StatePanel from "./components/StatePanel.svelte";
  import { analyzeProof } from "./lib/api";
  import { defaultCode, exampleProofs } from "./lib/examples";
  import type { ProofTimeline, TacticStep } from "./lib/types";

  let code = defaultCode;
  let timeline: ProofTimeline | null = null;
  let currentStepIndex = 0;
  let isLoading = false;
  let isPlaying = false;
  let error: string | null = null;
  let playInterval: ReturnType<typeof setInterval> | null = null;

  let editorComponent: Editor;

  $: currentStep = timeline?.steps[currentStepIndex] ?? null;
  $: stateToShow = currentStep?.state_after ?? null;
  $: diffToShow = currentStep?.diff ?? null;

  async function handleAnalyze() {
    isLoading = true;
    error = null;
    timeline = null;
    currentStepIndex = 0;

    try {
      const result = await analyzeProof(code);

      if (result.error) {
        error = result.error;
      } else if (result.timeline) {
        timeline = result.timeline;
        if (timeline.error) {
          error = timeline.error;
        }
      }
    } catch (e) {
      error = e instanceof Error ? e.message : "Unknown error occurred";
    } finally {
      isLoading = false;
    }
  }

  function handleCodeChange(event: CustomEvent<string>) {
    code = event.detail;
  }

  function handleStepSelect(event: CustomEvent<number>) {
    currentStepIndex = event.detail;
    if (currentStep) {
      editorComponent?.highlightLine(currentStep.line);
    }
  }

  function handlePlay() {
    isPlaying = true;
    playInterval = setInterval(() => {
      if (timeline && currentStepIndex < timeline.steps.length - 1) {
        handleStepSelect(
          new CustomEvent("select", { detail: currentStepIndex + 1 }),
        );
      } else {
        handlePause();
      }
    }, 1000);
  }

  function handlePause() {
    isPlaying = false;
    if (playInterval) {
      clearInterval(playInterval);
      playInterval = null;
    }
  }

  function loadExample(key: keyof typeof exampleProofs) {
    code = exampleProofs[key];
    editorComponent?.setValue(code);
    timeline = null;
    error = null;
    currentStepIndex = 0;
  }
</script>

<div class="app-container">
  <!-- Scanlines & Grid Overlay -->
  <div class="crt-overlay"></div>
  <div class="grid-background"></div>

  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="header-deco-line"></div>
      <div class="header-content">
        <div class="brand">
          <div class="logo-box">
            <span class="logo">◇</span>
          </div>
          <div class="title-group">
            <h1>LEAN VISUALIZER</h1>
            <div class="subtitle">PROOF STATE ANALYZER</div>
          </div>
          <span class="version">V0</span>
        </div>

        <div class="actions">
          <div class="examples-dropdown">
            <span class="dropdown-label">SYSTEM_LOAD:</span>
            <div class="button-group">
              <button class="example-btn" on:click={() => loadExample("simple")}
                >BASIC</button
              >
              <button
                class="example-btn"
                on:click={() => loadExample("induction")}>INDUCTION</button
              >
              <button class="example-btn" on:click={() => loadExample("calc")}
                >CALC</button
              >
              <button class="example-btn" on:click={() => loadExample("prime")}
                >PRIME</button
              >
            </div>
          </div>

          <button
            class="analyze-btn"
            on:click={handleAnalyze}
            disabled={isLoading}
          >
            {#if isLoading}
              <span class="loading-dots">PROCESSING</span>
              <div class="loading-bar"></div>
            {:else}
              RUN ANALYSIS <span class="arrow">>></span>
            {/if}
          </button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="main">
      <!-- Left: Editor -->
      <div class="panel editor-panel">
        <div class="panel-header">
          <div class="panel-title">
            <span class="icon">█</span>
            <span class="text">SOURCE_CODE</span>
          </div>
          <div class="panel-deco">EDIT_MODE: ACTIVE</div>
        </div>
        <div class="editor-wrapper">
          <Editor
            bind:this={editorComponent}
            value={code}
            on:change={handleCodeChange}
          />
        </div>
      </div>

      <!-- Right: State Panel -->
      <div class="panel state-panel-wrapper">
        <div class="panel-header">
          <div class="panel-title">
            <span class="icon">➜</span>
            <span class="text">PROOF_STATE</span>
          </div>
          <div class="panel-deco">
            {#if currentStep}
              <span class="current-tactic">EXEC: {currentStep.tactic}</span>
            {:else}
              STATUS: IDLE
            {/if}
          </div>
        </div>
        <StatePanel
          state={stateToShow}
          diff={diffToShow}
          title={currentStep ? `After: ${currentStep.tactic}` : "Proof State"}
        />
      </div>
    </main>

    <!-- Timeline -->
    <div class="timeline-panel">
      {#if error}
        <div class="error-banner">
          <span class="error-icon">⚠</span>
          <div class="error-content">
            <span class="error-title">SYSTEM ERROR</span>
            <span class="error-msg">{error}</span>
          </div>
        </div>
      {/if}

      {#if timeline}
        <Timeline
          steps={timeline.steps}
          {currentStepIndex}
          {isPlaying}
          on:select={handleStepSelect}
          on:play={handlePlay}
          on:pause={handlePause}
        />
      {:else if !error}
        <div class="timeline-placeholder">
          <div class="placeholder-content">
            <div class="scanner-line"></div>
            <span>AWAITING INPUT_STREAM...</span>
            <small>Execute analysis to generate timeline</small>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  :global(body) {
    font-family: "JetBrains Mono", monospace;
    background: #000;
    color: #e0e0e0;
    min-height: 100vh;
    overflow: hidden;
  }

  /* CRT & Grid Effects */
  .crt-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      rgba(18, 16, 16, 0) 50%,
      rgba(0, 0, 0, 0.1) 50%
    );
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 1000;
    opacity: 0.6;
  }

  .grid-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: linear-gradient(
        rgba(0, 240, 255, 0.03) 1px,
        transparent 1px
      ),
      linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: -1;
  }

  .app-container {
    height: 100vh;
    background: radial-gradient(circle at center, #0a0a14 0%, #000 100%);
  }

  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: relative;
    z-index: 1;
  }

  /* Header */
  .header {
    background: rgba(5, 5, 10, 0.9);
    border-bottom: 1px solid #222;
    padding: 0 24px;
    height: 70px;
    flex-shrink: 0;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .header-deco-line {
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #00f0ff, transparent 50%, #ff003c);
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
  }

  .header-content {
    max-width: 1920px;
    width: 100%;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .logo-box {
    width: 36px;
    height: 36px;
    border: 1px solid #ff003c;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 0, 60, 0.1);
    box-shadow: 0 0 10px rgba(255, 0, 60, 0.2);
  }

  .logo {
    color: #ff003c;
    font-size: 20px;
    text-shadow: 0 0 5px #ff003c;
  }

  .title-group h1 {
    font-size: 18px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 2px;
    line-height: 1;
  }

  .subtitle {
    font-size: 9px;
    color: #00f0ff;
    letter-spacing: 3px;
    margin-top: 2px;
  }

  .version {
    font-size: 10px;
    color: #000;
    background: #00f0ff;
    padding: 2px 6px;
    font-weight: bold;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    transform: skewX(-10deg);
  }

  .actions {
    display: flex;
    align-items: center;
    gap: 32px;
  }

  .examples-dropdown {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .dropdown-label {
    font-size: 10px;
    color: #555;
    letter-spacing: 1px;
    font-weight: bold;
  }

  .button-group {
    display: flex;
    gap: 2px;
    background: #111;
    padding: 2px;
    border: 1px solid #333;
  }

  .example-btn {
    background: #0a0a0a;
    border: none;
    color: #666;
    padding: 6px 16px;
    font-size: 10px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    font-weight: bold;
    letter-spacing: 1px;
  }

  .example-btn:hover {
    background: #222;
    color: #00f0ff;
    text-shadow: 0 0 5px rgba(0, 240, 255, 0.5);
  }

  .analyze-btn {
    background: transparent;
    border: 1px solid #00f0ff;
    color: #00f0ff;
    padding: 0 24px;
    height: 40px;
    font-size: 12px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: relative;
    overflow: hidden;
  }

  .analyze-btn:hover:not(:disabled) {
    background: rgba(0, 240, 255, 0.1);
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    text-shadow: 0 0 5px rgba(0, 240, 255, 0.8);
  }

  .analyze-btn:disabled {
    border-color: #333;
    color: #555;
    cursor: not-allowed;
  }

  .loading-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    background: #00f0ff;
    animation: loadingBar 1s infinite linear;
  }

  @keyframes loadingBar {
    0% {
      width: 0%;
      left: 0;
    }
    50% {
      width: 100%;
      left: 0;
    }
    100% {
      width: 0%;
      left: 100%;
    }
  }

  /* Main content */
  .main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px;
    background: #222;
    min-height: 0;
    padding: 2px;
  }

  .panel {
    display: flex;
    flex-direction: column;
    min-height: 0;
    background: rgba(5, 5, 10, 0.95);
    position: relative;
  }

  .panel::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 1px solid rgba(255, 255, 255, 0.05);
    pointer-events: none;
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    border-bottom: 1px solid #222;
    background: #080810;
  }

  .panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .panel-title .icon {
    color: #ff003c;
    font-size: 10px;
  }

  .panel-title .text {
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    color: #ccc;
  }

  .panel-deco {
    font-size: 9px;
    color: #444;
    letter-spacing: 1px;
  }

  .current-tactic {
    color: #00f0ff;
    text-shadow: 0 0 5px rgba(0, 240, 255, 0.3);
  }

  .editor-wrapper {
    flex: 1;
    overflow: hidden;
  }

  .state-panel-wrapper > :global(.state-panel) {
    flex: 1;
    overflow: auto;
  }

  /* Timeline panel */
  .timeline-panel {
    background: #050510;
    border-top: 1px solid #222;
    flex-shrink: 0;
    position: relative;
    z-index: 5;
  }

  .timeline-placeholder {
    padding: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at center, #0a0a1a 0%, #050510 100%);
  }

  .placeholder-content {
    border: 1px solid #333;
    padding: 30px 60px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
    background: rgba(0, 0, 0, 0.5);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  }

  .scanner-line {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: rgba(0, 240, 255, 0.5);
    animation: scan 2s infinite linear;
    box-shadow: 0 0 10px #00f0ff;
  }

  @keyframes scan {
    0% {
      top: 0;
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      top: 100%;
      opacity: 0;
    }
  }

  .placeholder-content span {
    color: #fff;
    letter-spacing: 4px;
    font-weight: bold;
    font-size: 16px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }

  .placeholder-content small {
    color: #555;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
  }

  .error-banner {
    display: flex;
    align-items: center;
    gap: 20px;
    background: rgba(255, 0, 60, 0.05);
    border-bottom: 2px solid #ff003c;
    padding: 16px 24px;
    color: #ff003c;
    animation: flashError 0.5s ease-out;
  }

  @keyframes flashError {
    0% {
      background: rgba(255, 0, 60, 0.2);
    }
    100% {
      background: rgba(255, 0, 60, 0.05);
    }
  }

  .error-icon {
    font-size: 24px;
    text-shadow: 0 0 10px #ff003c;
  }

  .error-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .error-title {
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    opacity: 0.8;
  }

  .error-msg {
    font-size: 12px;
    letter-spacing: 1px;
  }
</style>
