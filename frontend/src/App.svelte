<script lang="ts">
  import Editor from "./components/Editor.svelte";
  import Timeline from "./components/Timeline.svelte";
  import StatePanel from "./components/StatePanel.svelte";
  import { analyzeProof } from "./lib/api";
  import { defaultCode, exampleProofs } from "./lib/examples";
  import type { ProofTimeline, TacticStep } from "./lib/types";

  import ProofGraph from "./components/ProofGraph.svelte";
  import ExampleSelector from "./components/ExampleSelector.svelte";
  import Broplainer from "./components/Broplainer.svelte";
  import { soundManager } from "./lib/sound";

  let code = defaultCode;
  let timeline: ProofTimeline | null = null;
  let currentStepIndex = 0;
  let isLoading = false;
  let isPlaying = false;
  let error: string | null = null;
  let playInterval: ReturnType<typeof setInterval> | null = null;
  let fileInput: HTMLInputElement;
  let isLightMode = false;
  let viewMode: "timeline" | "graph" = "timeline";

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
          soundManager.playError();
        } else if (timeline.success) {
          soundManager.playSuccess();
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
    soundManager.playClick();
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

  function handleImportClick() {
    fileInput.click();
  }

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          code = e.target.result as string;
          editorComponent?.setValue(code);
          timeline = null; // Reset timeline on new file
          error = null;
        }
      };
      reader.readAsText(file);
    }
    // Reset value so same file can be selected again
    input.value = "";
    input.value = "";
  }

  function toggleTheme() {
    isLightMode = !isLightMode;
    console.log("Toggle Theme:", isLightMode ? "Light" : "Dark");
    if (isLightMode) {
      document.body.classList.add("light-mode");
    } else {
      document.body.classList.remove("light-mode");
    }
  }

  function handleExampleSelect(event: CustomEvent<{ code: string }>) {
    code = event.detail.code;
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
          <button
            class="theme-toggle"
            on:click={toggleTheme}
            title="Toggle Theme"
          >
            {isLightMode ? "☀" : "☾"}
          </button>

          <input
            type="file"
            accept=".lean,.lean4"
            style="display: none;"
            bind:this={fileInput}
            on:change={handleFileSelect}
          />
          <button class="action-btn" on:click={handleImportClick}>
            <span class="icon">⏏</span> IMPORT
          </button>

          <ExampleSelector on:select={handleExampleSelect} />

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
            theme={isLightMode ? "light" : "dark"}
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
          explanation={currentStep?.explanation}
          title={currentStep ? `After: ${currentStep.tactic}` : "Proof State"}
        />
        {#if currentStep}
          <Broplainer tactic={currentStep.tactic} />
        {/if}
      </div>
    </main>

    <!-- Timeline / Graph Area -->
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

      <div class="view-controls">
        <button
          class="view-btn"
          class:active={viewMode === "timeline"}
          on:click={() => (viewMode = "timeline")}
        >
          TIMELINE
        </button>
        <button
          class="view-btn"
          class:active={viewMode === "graph"}
          on:click={() => (viewMode = "graph")}
        >
          GRAPH
        </button>
      </div>

      {#if timeline}
        {#if viewMode === "timeline"}
          <Timeline
            steps={timeline.steps}
            {currentStepIndex}
            {isPlaying}
            on:select={handleStepSelect}
            on:play={handlePlay}
            on:pause={handlePause}
          />
        {:else}
          <ProofGraph
            {timeline}
            {currentStepIndex}
            on:select={handleStepSelect}
          />
        {/if}
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
    background: var(--bg-app);
    color: var(--text-primary);
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
      var(--crt-scanline) 50%
    );
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 1000;
    opacity: var(--crt-opacity);
  }

  .grid-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: linear-gradient(var(--grid-color) 1px, transparent 1px),
      linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: -1;
  }

  .app-container {
    height: 100vh;
    background: var(--bg-app);
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
    background: var(--bg-header);
    border-bottom: 1px solid var(--border-color);
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
    background: linear-gradient(
      90deg,
      var(--accent-color),
      transparent 50%,
      var(--accent-secondary)
    );
    box-shadow: 0 0 10px rgba(var(--accent-color-rgb), 0.5);
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
    border: 1px solid var(--accent-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(var(--accent-secondary-rgb), 0.1);
    box-shadow: 0 0 10px rgba(var(--accent-secondary-rgb), 0.2);
  }

  .logo {
    color: var(--accent-secondary);
    font-size: 20px;
    text-shadow: 0 0 5px var(--accent-secondary);
  }

  .title-group h1 {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 2px;
    line-height: 1;
  }

  .subtitle {
    font-size: 9px;
    color: var(--accent-color);
    letter-spacing: 3px;
    margin-top: 2px;
  }

  .version {
    font-size: 10px;
    color: #000;
    background: var(--accent-color);
    padding: 2px 6px;
    font-weight: bold;
    box-shadow: 0 0 10px rgba(var(--accent-color-rgb), 0.4);
    transform: skewX(-10deg);
  }

  .actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .theme-toggle {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s;
  }

  .theme-toggle:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
  }

  .analyze-btn {
    background: transparent;
    border: 1px solid var(--accent-color);
    color: var(--accent-color);
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
    background: rgba(var(--accent-color-rgb), 0.1);
    box-shadow: 0 0 20px rgba(var(--accent-color-rgb), 0.2);
    text-shadow: 0 0 5px rgba(var(--accent-color-rgb), 0.8);
  }

  .analyze-btn:disabled {
    border-color: var(--border-color);
    color: var(--text-muted);
    cursor: not-allowed;
  }

  .loading-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    background: var(--accent-color);
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

  .action-btn {
    background: rgba(var(--accent-color-rgb), 0.1);
    border: 1px solid var(--accent-color);
    color: var(--accent-color);
    padding: 0 16px;
    height: 32px;
    font-size: 10px;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
    font-family: inherit;
    letter-spacing: 1px;
    margin-right: 16px;
  }

  .action-btn:hover {
    background: rgba(var(--accent-color-rgb), 0.2);
    box-shadow: 0 0 10px rgba(var(--accent-color-rgb), 0.2);
  }

  .action-btn .icon {
    font-size: 14px;
  }

  /* Main content */
  .main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px;
    background: var(--border-color);
    min-height: 0;
    padding: 2px;
  }

  .panel {
    display: flex;
    flex-direction: column;
    min-height: 0;
    background: var(--bg-panel);
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
    border-bottom: 1px solid var(--border-color);
    background: rgba(0, 0, 0, 0.2);
  }

  .panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .panel-title .icon {
    color: var(--accent-secondary);
    font-size: 10px;
  }

  .panel-title .text {
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    color: var(--text-secondary);
  }

  .panel-deco {
    font-size: 9px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .current-tactic {
    color: var(--accent-color);
    text-shadow: 0 0 5px rgba(var(--accent-color-rgb), 0.3);
  }

  .editor-wrapper {
    flex: 1;
    overflow: hidden;
  }

  .state-panel-wrapper > :global(.state-panel) {
    flex: 1;
    overflow: auto;
  }

  .timeline-panel {
    background: var(--bg-timeline);
    border-top: 1px solid var(--border-color);
    flex-shrink: 0;
    position: relative;
    z-index: 5;
    display: flex;
    flex-direction: column;
  }

  .view-controls {
    display: flex;
    gap: 1px;
    background: var(--border-color);
    padding-bottom: 1px;
    margin-bottom: -1px; /* overlap border */
    position: absolute;
    top: -24px;
    right: 20px;
    z-index: 10;
  }

  .view-btn {
    background: var(--bg-panel);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    font-size: 10px;
    padding: 4px 12px;
    cursor: pointer;
    font-weight: bold;
    letter-spacing: 1px;
    transition: all 0.2s;
  }

  .view-btn:hover {
    color: var(--text-primary);
    background: var(--item-bg-hover);
  }

  .view-btn.active {
    background: var(--bg-timeline);
    color: var(--accent-color);
    border-bottom-color: var(--bg-timeline);
  }

  .timeline-placeholder {
    padding: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(
      circle at center,
      var(--item-bg-hover) 0%,
      transparent 100%
    );
  }

  .placeholder-content {
    border: 1px solid var(--border-color);
    padding: 30px 60px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
    background: var(--bg-panel);
    box-shadow: 0 0 20px rgba(var(--accent-color-rgb), 0.1);
  }

  .scanner-line {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: rgba(var(--accent-color-rgb), 0.5);
    animation: scan 2s infinite linear;
    box-shadow: 0 0 10px var(--accent-color);
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
    color: var(--text-primary);
    letter-spacing: 4px;
    font-weight: bold;
    font-size: 16px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }

  .placeholder-content small {
    color: var(--text-muted);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
  }

  .error-banner {
    display: flex;
    align-items: center;
    gap: 20px;
    background: rgba(var(--accent-secondary-rgb), 0.05);
    border-bottom: 2px solid var(--accent-secondary);
    padding: 16px 24px;
    color: var(--accent-secondary);
    animation: flashError 0.5s ease-out;
  }

  @keyframes flashError {
    0% {
      background: rgba(var(--accent-secondary-rgb), 0.2);
    }
    100% {
      background: rgba(var(--accent-secondary-rgb), 0.05);
    }
  }

  .error-icon {
    font-size: 24px;
    text-shadow: 0 0 10px var(--accent-secondary);
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

  /* CSS Variables for Theming - Consolidated */
  :global(:root) {
    /* Default Dark Theme */
    --bg-app: radial-gradient(circle at center, #0a0a14 0%, #000 100%);
    --bg-panel: rgba(5, 5, 10, 0.95);
    --bg-header: rgba(5, 5, 10, 0.9);
    --bg-timeline: #050510;

    --text-primary: #e0e0e0;
    --text-secondary: #ccc;
    --text-muted: #555;

    --border-color: #222;
    --accent-color: #00f0ff;
    --accent-secondary: #ff003c;
    --accent-color-rgb: 0, 240, 255;
    --accent-secondary-rgb: 255, 0, 60;

    --grid-color: rgba(0, 240, 255, 0.03);
    --crt-scanline: rgba(0, 0, 0, 0.1);
    --crt-opacity: 0.6;

    --item-bg: rgba(255, 255, 255, 0.02);
    --item-bg-hover: rgba(255, 255, 255, 0.04);
    --diff-added-bg: rgba(0, 240, 255, 0.03);
    --diff-removed-bg: rgba(255, 0, 60, 0.03);
    --success-bg: rgba(0, 240, 255, 0.05);

    --scrollbar-track: #050510;
    --scrollbar-thumb: #333;
  }

  :global(.light-mode) {
    /* Light Theme Overrides */
    --bg-app: radial-gradient(circle at center, #f0f0f5 0%, #e0e0ea 100%);
    --bg-panel: rgba(255, 255, 255, 0.95);
    --bg-header: rgba(245, 245, 250, 0.95);
    --bg-timeline: #fafafa;

    --text-primary: #1a1a2e;
    --text-secondary: #333;
    --text-muted: #888;

    --border-color: #e0e0e0;
    --accent-color: #0070f3;
    --accent-secondary: #d0006f;
    --accent-color-rgb: 0, 112, 243;
    --accent-secondary-rgb: 208, 0, 111;

    --grid-color: rgba(0, 0, 0, 0.03);
    --crt-scanline: rgba(255, 255, 255, 0.1);
    --crt-opacity: 0.2;

    --item-bg: rgba(0, 0, 0, 0.03);
    --item-bg-hover: rgba(0, 0, 0, 0.05);
    --diff-added-bg: rgba(0, 112, 243, 0.1);
    --diff-removed-bg: rgba(208, 0, 111, 0.1);
    --success-bg: rgba(0, 112, 243, 0.1);

    --scrollbar-track: #f0f0f0;
    --scrollbar-thumb: #ccc;
  }
</style>
