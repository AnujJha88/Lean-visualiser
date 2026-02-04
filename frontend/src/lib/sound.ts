export class SoundManager {
    private ctx: AudioContext | null = null;
    private gainNode: GainNode | null = null;
    private enabled: boolean = true;

    constructor() {
        if (typeof window !== 'undefined') {
            try {
                this.ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
                this.gainNode = this.ctx.createGain();
                this.gainNode.connect(this.ctx.destination);
                this.gainNode.gain.value = 0.3; // Master volume
            } catch (e) {
                console.error("Web Audio API not supported", e);
            }
        }
    }

    private ensureContext() {
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    public toggle(enabled: boolean) {
        this.enabled = enabled;
    }

    // High pitch blip for UI clicks
    public playClick() {
        if (!this.enabled || !this.ctx || !this.gainNode) return;
        this.ensureContext();

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.connect(gain);
        gain.connect(this.gainNode);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, this.ctx.currentTime + 0.1);

        gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    }

    // Satisfying major triad for success
    public playSuccess() {
        if (!this.enabled || !this.ctx || !this.gainNode) return;
        this.ensureContext();

        const now = this.ctx.currentTime;
        const notes = [440, 554.37, 659.25]; // A4, C#5, E5 (A Major)

        notes.forEach((freq, i) => {
            const osc = this.ctx!.createOscillator();
            const gain = this.ctx!.createGain();

            osc.connect(gain);
            gain.connect(this.gainNode!);

            osc.type = 'triangle';
            osc.frequency.value = freq;

            gain.gain.setValueAtTime(0, now + i * 0.1);
            gain.gain.linearRampToValueAtTime(0.3, now + i * 0.1 + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.1 + 0.5);

            osc.start(now + i * 0.1);
            osc.stop(now + i * 0.1 + 0.5);
        });
    }

    // Glitchy saw wave for error
    public playError() {
        if (!this.enabled || !this.ctx || !this.gainNode) return;
        this.ensureContext();

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.connect(gain);
        gain.connect(this.gainNode);

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(100, this.ctx.currentTime + 0.2);

        gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.2);
    }

    // Very subtle tick for interactions (like hover)
    public playHover() {
        if (!this.enabled || !this.ctx || !this.gainNode) return;
        // Don't resume context just for hover to avoid annoyance if not started
        if (this.ctx.state === 'suspended') return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.connect(gain);
        gain.connect(this.gainNode);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(2000, this.ctx.currentTime);

        gain.gain.setValueAtTime(0.05, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.03);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.03);
    }
}

export const soundManager = new SoundManager();
