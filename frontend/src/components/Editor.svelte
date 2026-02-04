<script lang="ts">
  import { onMount, onDestroy, createEventDispatcher } from "svelte";
  import * as monaco from "monaco-editor";

  export let value: string = "";
  export let readonly: boolean = false;
  export let theme: "dark" | "light" = "dark";

  const dispatch = createEventDispatcher<{ change: string }>();

  let container: HTMLDivElement;
  let editor: monaco.editor.IStandaloneCodeEditor;

  // Register Lean4 language
  function registerLeanLanguage() {
    // Check if already registered
    if (monaco.languages.getLanguages().some((lang) => lang.id === "lean4")) {
      return;
    }

    monaco.languages.register({ id: "lean4" });

    monaco.languages.setMonarchTokensProvider("lean4", {
      keywords: [
        "theorem",
        "lemma",
        "def",
        "example",
        "axiom",
        "constant",
        "structure",
        "class",
        "instance",
        "inductive",
        "where",
        "if",
        "then",
        "else",
        "match",
        "with",
        "do",
        "return",
        "let",
        "have",
        "show",
        "by",
        "fun",
        "forall",
        "exists",
        "import",
        "open",
        "namespace",
        "section",
        "variable",
        "private",
        "protected",
        "public",
        "partial",
        "unsafe",
        "set_option",
        "attribute",
        "deriving",
      ],
      tactics: [
        "intro",
        "intros",
        "exact",
        "apply",
        "rw",
        "rewrite",
        "simp",
        "constructor",
        "cases",
        "induction",
        "have",
        "let",
        "show",
        "assumption",
        "contradiction",
        "trivial",
        "rfl",
        "ring",
        "linarith",
        "omega",
        "decide",
        "norm_num",
        "ext",
        "funext",
        "congr",
        "left",
        "right",
        "use",
        "exists",
        "obtain",
        "rcases",
      ],
      types: [
        "Prop",
        "Type",
        "Sort",
        "Nat",
        "Int",
        "Bool",
        "String",
        "List",
        "Option",
      ],
      operators: ["→", "←", "↔", "∧", "∨", "¬", "∀", "∃", "⊢", "·", ":=", "|"],

      tokenizer: {
        root: [
          // Comments
          [/--.*$/, "comment"],
          [/\/-/, "comment", "@comment"],

          // Strings
          [/"([^"\\]|\\.)*$/, "string.invalid"],
          [/"/, "string", "@string"],

          // Numbers
          [/\d+/, "number"],

          // Keywords and identifiers
          [
            /[a-zA-Z_]\w*/,
            {
              cases: {
                "@keywords": "keyword",
                "@tactics": "keyword.tactic",
                "@types": "type",
                "@default": "identifier",
              },
            },
          ],

          // Operators
          [/[→←↔∧∨¬∀∃⊢·]/, "operator"],
          [/:=/, "operator"],
          [/[{}()\[\]]/, "delimiter.bracket"],
          [/[,:]/, "delimiter"],
        ],
        comment: [
          [/[^-/]+/, "comment"],
          [/-\//, "comment", "@pop"],
          [/./, "comment"],
        ],
        string: [
          [/[^\\"]+/, "string"],
          [/\\./, "string.escape"],
          [/"/, "string", "@pop"],
        ],
      },
    });

    // Define theme colors for Lean
    monaco.editor.defineTheme("lean-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "keyword", foreground: "c586c0" },
        { token: "keyword.tactic", foreground: "4fc1ff", fontStyle: "bold" },
        { token: "type", foreground: "4ec9b0" },
        { token: "operator", foreground: "d4d4d4" },
        { token: "comment", foreground: "6a9955" },
        { token: "string", foreground: "ce9178" },
        { token: "number", foreground: "b5cea8" },
      ],
      colors: {
        "editor.background": "#1a1a2e",
        "editor.foreground": "#e4e4e7",
        "editor.lineHighlightBackground": "#24243e",
        "editorCursor.foreground": "#8b5cf6",
        "editor.selectionBackground": "#3b3b5c",
      },
    });

    // Define light theme for Lean
    monaco.editor.defineTheme("lean-light", {
      base: "vs",
      inherit: true,
      rules: [
        { token: "keyword", foreground: "af00db" },
        { token: "keyword.tactic", foreground: "0000ff", fontStyle: "bold" },
        { token: "type", foreground: "267f99" },
        { token: "operator", foreground: "383838" },
        { token: "comment", foreground: "008000" },
        { token: "string", foreground: "a31515" },
        { token: "number", foreground: "098658" },
      ],
      colors: {
        "editor.background": "#ffffff",
        "editor.foreground": "#000000",
        "editor.lineHighlightBackground": "#f0f0f0",
        "editorCursor.foreground": "#000000",
        "editor.selectionBackground": "#add6ff",
      },
    });
  }

  onMount(() => {
    registerLeanLanguage();

    editor = monaco.editor.create(container, {
      value,
      language: "lean4",
      theme: theme === "light" ? "lean-light" : "lean-dark",
      fontSize: 14,
      fontFamily: "'JetBrains Mono', monospace",
      minimap: { enabled: false },
      lineNumbers: "on",
      scrollBeyondLastLine: false,
      automaticLayout: true,
      padding: { top: 16, bottom: 16 },
      readOnly: readonly,
      wordWrap: "on",
      renderLineHighlight: "all",
      cursorBlinking: "smooth",
      smoothScrolling: true,
    });

    editor.onDidChangeModelContent(() => {
      const newValue = editor.getValue();
      dispatch("change", newValue);
    });
  });

  onDestroy(() => {
    editor?.dispose();
  });

  export function getValue(): string {
    return editor?.getValue() ?? value;
  }

  export function setValue(newValue: string) {
    editor?.setValue(newValue);
  }

  export function highlightLine(line: number) {
    editor?.revealLineInCenter(line);
    editor?.setPosition({ lineNumber: line, column: 1 });
  }

  $: if (editor) {
    monaco.editor.setTheme(theme === "light" ? "lean-light" : "lean-dark");
  }
</script>

<div class="editor-container" bind:this={container}></div>

<style>
  .editor-container {
    width: 100%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
  }
</style>
