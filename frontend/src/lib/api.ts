// API client for communicating with the backend

import type { AnalyzeResponse } from './types';

// Use environment variable for API URL if set (production), otherwise default to relative (proxy)
const BASE_URL = import.meta.env.VITE_API_URL || '';
const API_BASE = `${BASE_URL}/api`;

export async function analyzeProof(code: string): Promise<AnalyzeResponse> {
    const response = await fetch(`${API_BASE}/proof/analyze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
}

export async function healthCheck(): Promise<boolean> {
    try {
        const response = await fetch(`${BASE_URL}/health`);
        return response.ok;
    } catch {
        return false;
    }
}
