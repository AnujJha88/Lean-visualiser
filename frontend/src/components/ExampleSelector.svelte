<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { exampleProofs } from "../lib/examples";

    const dispatch = createEventDispatcher();
    let isOpen = false;

    // Categories structure (since exampleProofs is flat, we'll categorize manually or infer)
    // For V1, let's map keys to categories
    const categories = {
        Basics: ["simple", "logicChain"],
        Algebra: ["algebrav", "distrib"],
        Advanced: ["induction", "cases", "contradiction"],
        Complex: ["sumAnalysis", "listReverse"],
    };

    function selectExample(key: string) {
        dispatch("select", {
            key,
            code: exampleProofs[key as keyof typeof exampleProofs],
        });
        isOpen = false;
    }

    function toggleOpen() {
        isOpen = !isOpen;
    }

    // Close on outside click (naive implementation)
    function handleBackdrop() {
        isOpen = false;
    }

    function isExample(key: string): boolean {
        return key in exampleProofs;
    }
</script>

<div class="example-selector">
    <button class="selector-btn" on:click={toggleOpen} class:active={isOpen}>
        <span class="label">LOAD_PROGRAM:</span>
        <span class="current">SELECT_PROOF</span>
        <span class="arrow">▼</span>
    </button>

    {#if isOpen}
        <div
            class="backdrop"
            role="button"
            tabindex="0"
            on:click={handleBackdrop}
            on:keydown={(e) => e.key === "Escape" && handleBackdrop()}
        ></div>
        <div class="dropdown-menu">
            {#each Object.entries(categories) as [category, keys]}
                <div class="category">
                    <div class="category-header">{category.toUpperCase()}</div>
                    <div class="category-items">
                        {#each keys as key}
                            <!-- Only show if it exists in exampleProofs -->
                            {#if isExample(key)}
                                <button
                                    class="item-btn"
                                    on:click={() => selectExample(key)}
                                >
                                    {key.toUpperCase()}
                                </button>
                            {/if}
                        {/each}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .example-selector {
        position: relative;
        font-family: "JetBrains Mono", monospace;
    }

    .selector-btn {
        background: var(--bg-panel);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        height: 32px;
        padding: 0 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        font-size: 11px;
        transition: all 0.2s;
    }

    .selector-btn:hover,
    .selector-btn.active {
        border-color: var(--accent-color);
        box-shadow: 0 0 10px rgba(var(--accent-color-rgb), 0.2);
    }

    .label {
        color: var(--text-muted);
        font-weight: bold;
    }

    .current {
        color: var(--accent-color);
        font-weight: bold;
    }

    .arrow {
        font-size: 8px;
        color: var(--text-muted);
    }

    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        margin-top: 4px;
        background: var(--bg-panel);
        border: 1px solid var(--accent-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        z-index: 100;
        width: 250px;
        padding: 8px;
        backdrop-filter: blur(10px);
        animation: slideDown 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .category {
        margin-bottom: 12px;
    }

    .category:last-child {
        margin-bottom: 0;
    }

    .category-header {
        font-size: 9px;
        color: var(--text-muted);
        margin-bottom: 4px;
        padding-left: 4px;
        letter-spacing: 1px;
        border-bottom: 1px solid var(--border-color);
    }

    .category-items {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2px;
    }

    .item-btn {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        text-align: left;
        padding: 6px 8px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
        font-family: inherit;
        position: relative;
        overflow: hidden;
    }

    .item-btn:hover {
        background: rgba(var(--accent-color-rgb), 0.1);
        color: var(--accent-color);
        padding-left: 12px;
    }

    .item-btn:hover::before {
        content: "►";
        position: absolute;
        left: 2px;
        font-size: 8px;
        top: 8px;
    }

    .backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 99;
    }
</style>
