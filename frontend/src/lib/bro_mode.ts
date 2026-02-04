/**
 * Translates standard Lean tactics into "Bro/Vibe" speak.
 */
export function translateToBro(tactic: string): string {
    const t = tactic.trim();

    // Heuristics
    if (t.startsWith("rw") || t.startsWith("rewrite")) {
        return "Remix the equation with that identity.";
    }
    if (t.startsWith("intro")) {
        return "Bring in the new players.";
    }
    if (t.startsWith("apply")) {
        return "Use that special move.";
    }
    if (t.startsWith("exact")) {
        return "Boom. Exactly what we needed.";
    }
    if (t.startsWith("simp")) {
        return "Ez clap. Clean up the mess.";
    }
    if (t.startsWith("induction")) {
        return "Break it down, scene by scene (Base & Step).";
    }
    if (t.startsWith("cases")) {
        return "Split the timeline. We got options.";
    }
    if (t.startsWith("have")) {
        return "Hold up, let me cook this sub-proof real quick.";
    }
    if (t.startsWith("calc")) {
        return "Run the numbers. Big brain calculation time.";
    }
    if (t.startsWith("rfl") || t.startsWith("refl")) {
        return "Mirror mirror on the wall. It's the same thing.";
    }
    if (t.startsWith("contradiction")) {
        return "No shot. That's impossible. GG.";
    }
    if (t.startsWith("linarith")) {
        return "Let the linear algebra solver carry us.";
    }
    if (t.startsWith("ring")) {
        return "Ring theory magic. It just works.";
    }

    // Default fallbacks
    return "Execute the next instruction.";
}
