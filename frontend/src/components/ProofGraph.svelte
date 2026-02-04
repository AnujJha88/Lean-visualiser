<script lang="ts">
    import { onMount, createEventDispatcher, afterUpdate } from "svelte";
    import * as d3 from "d3";
    import { buildProofGraph, type GraphNode } from "../lib/graph";
    import type { ProofTimeline } from "../lib/types";

    export let timeline: ProofTimeline | null = null;
    export let currentStepIndex: number = 0;

    const dispatch = createEventDispatcher();
    let container: HTMLElement;
    let svg: any;

    // Config
    const margin = { top: 20, right: 90, bottom: 30, left: 90 };
    const width = 800; // Initial mock width
    const height = 400; // Initial mock height

    $: root = buildProofGraph(timeline);
    $: if (container && root) {
        renderGraph();
    }

    // React to step changes to highlight nodes
    $: if (currentStepIndex !== undefined) {
        highlightNode(currentStepIndex);
    }

    function renderGraph() {
        if (!container) return;

        // Clear previous
        d3.select(container).selectAll("*").remove();

        const w = container.clientWidth || width;
        const h = container.clientHeight || height;

        // Create the Zoom Behavior first
        const zoom = d3.zoom().on("zoom", (event) => {
            // We need to select the g here because it might be created after the behavior
            d3.select(container).select("g").attr("transform", event.transform);
        });

        // Create SVG and attach zoom
        svg = d3
            .select(container)
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", [0, 0, w, h])
            .call(zoom as any);

        // Create the group for content *before* triggering any zoom transforms
        const g = svg.append("g");

        // Initial translation to center vertically and padding left
        // With nodeSize, root is at (0,0). x is vertical, y is horizontal.
        const initialTransform = d3.zoomIdentity
            .translate(margin.left, h / 2)
            .scale(1);

        // Apply the transform (this triggers the zoom event synchronously)
        svg.call(zoom.transform as any, initialTransform);

        // Continue using g for drawing
        // const g = svg.select("g"); // Logic above now ensures g exists
        // Since we rotate x/y for horizontal layout:
        // nodeSize([height-per-node, width-per-level])
        const treeLayout = d3.tree<GraphNode>().nodeSize([40, 200]);
        const hierarchy = d3.hierarchy(root);
        const treeData = treeLayout(hierarchy);

        // Links
        g.selectAll(".link")
            .data(treeData.links())
            .enter()
            .append("path")
            .attr("class", "link")
            .attr(
                "d",
                d3
                    .linkHorizontal()
                    .x((d: any) => d.y)
                    .y((d: any) => d.x),
            )
            .style("fill", "none")
            .style("stroke", "var(--text-muted)")
            .style("stroke-width", "2px")
            .style("opacity", "0.5");

        // Nodes
        const nodes = g
            .selectAll(".node")
            .data(treeData.descendants())
            .enter()
            .append("g")
            .attr("class", (d: any) => `node ${d.data.type}`)
            .attr("transform", (d: any) => `translate(${d.y},${d.x})`)
            .on("click", (event: any, d: any) => {
                if (d.data.stepIndex !== undefined) {
                    dispatch("select", d.data.stepIndex);
                }
            });

        // Node Circles/Rects
        nodes
            .append("circle")
            .attr("r", 5)
            .style("fill", "var(--bg-app)")
            .style("stroke", "var(--accent-color)")
            .style("stroke-width", "2px");

        // Add Tooltip for full text
        nodes.append("title").text((d: any) => d.data.label);

        // Node Labels (Truncated)
        nodes
            .append("text")
            .attr("dy", ".35em")
            .attr("x", (d: any) => (d.children ? -13 : 13))
            .style("text-anchor", (d: any) => (d.children ? "end" : "start"))
            .text((d: any) => {
                const label = d.data.label;
                return label.length > 20
                    ? label.substring(0, 20) + "..."
                    : label;
            })
            .style("fill", "var(--text-primary)")
            .style("font-size", "12px")
            .style("font-family", "JetBrains Mono");

        highlightNode(currentStepIndex);
    }

    function highlightNode(index: number) {
        if (!svg) return;

        svg.selectAll(".node circle")
            .style("fill", "var(--bg-app)")
            .style("r", 6)
            .style("filter", "none");

        svg.selectAll(".node text")
            .style("fill", "var(--text-primary)")
            .style("font-weight", "normal");

        // Highlight active
        svg.selectAll(".node")
            .filter((d: any) => d.data.stepIndex === index)
            .select("circle")
            .style("fill", "var(--accent-color)")
            .style("r", 8)
            .style("filter", "drop-shadow(0 0 5px var(--accent-color))");

        svg.selectAll(".node")
            .filter((d: any) => d.data.stepIndex === index)
            .select("text")
            .style("fill", "var(--accent-color)")
            .style("font-weight", "bold");
    }

    onMount(() => {
        window.addEventListener("resize", renderGraph);
        renderGraph();
        return () => window.removeEventListener("resize", renderGraph);
    });
</script>

<div class="graph-container" bind:this={container}></div>

<style>
    .graph-container {
        width: 100%;
        height: 100%;
        min-height: 300px;
        background: var(--bg-panel);
        overflow: hidden;
        cursor: grab;
    }

    .graph-container:active {
        cursor: grabbing;
    }

    :global(.node) {
        cursor: pointer;
        transition: all 0.3s ease;
    }

    :global(.node:hover circle) {
        r: 8px;
        stroke: var(--accent-secondary);
    }

    :global(.node:hover text) {
        fill: var(--accent-secondary);
    }
</style>
