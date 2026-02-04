<script lang="ts">
    import { translateToBro } from "../lib/bro_mode";

    export let tactic: string = "";

    $: translation = translateToBro(tactic);
</script>

<div class="bro-panel">
    <div class="header">
        <span class="icon">🤖</span>
        <span class="title">BRO_PLAINER_V1</span>
    </div>
    <div class="content">
        <div class="tactic">> {tactic}</div>
        <div class="translation">
            <span class="prefix">AI says:</span>
            "{translation}"
        </div>
    </div>
</div>

<style>
    .bro-panel {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid var(--accent-color);
        padding: 12px;
        font-family: "JetBrains Mono", monospace;
        margin-top: 10px;
        box-shadow: 0 0 15px rgba(var(--accent-color-rgb), 0.1);
        backdrop-filter: blur(5px);
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        border-bottom: 1px dashed var(--accent-color);
        padding-bottom: 4px;
    }

    .title {
        color: var(--accent-color);
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 2px;
    }

    .icon {
        font-size: 12px;
    }

    .content {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .tactic {
        color: var(--text-muted);
        font-size: 10px;
    }

    .translation {
        color: #0f0; /* Terminal green */
        font-size: 12px;
        line-height: 1.4;
        text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
    }

    .prefix {
        color: var(--text-muted);
        margin-right: 6px;
        font-size: 10px;
    }
</style>
