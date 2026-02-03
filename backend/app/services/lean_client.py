"""
Lean4Web WebSocket Client

Communicates with the Lean4Web service using WebSocket and JSON-RPC over LSP protocol.
"""

import asyncio
import json
import re
from typing import Any
import websockets
from websockets.exceptions import WebSocketException

from ..config import get_settings


class Lean4WebClient:
    """
    Client for interacting with Lean4Web using WebSocket.
    
    The Lean4Web server uses JSON-RPC 2.0 over WebSocket with LSP protocol.
    """
    
    def __init__(self):
        self.settings = get_settings()
        # WebSocket URL for Lean4Web (wss for secure WebSocket)
        self.ws_url = self.settings.lean4web_url.replace("https://", "wss://").replace("http://", "ws://")
        self.ws_url = f"{self.ws_url}/websocket"
        self._request_id = 0
    
    def _next_id(self) -> int:
        """Get next request ID."""
        self._request_id += 1
        return self._request_id
    
    async def analyze_code(self, code: str, timeout: float = 30.0) -> dict[str, Any]:
        """
        Send Lean code to Lean4Web and get diagnostics and goal states.
        
        Returns a dict with:
        - diagnostics: list of diagnostic messages
        - goals: list of goal states at various positions
        - success: whether code compiled without errors
        """
        result = {
            "diagnostics": [],
            "goals": [],
            "success": True,
            "messages": []
        }
        
        try:
            async with websockets.connect(
                self.ws_url,
                additional_headers={"Origin": self.settings.lean4web_url},
                close_timeout=5,
                open_timeout=10,
            ) as ws:
                # Initialize connection - similar to how lean4web does it
                # Send the code as a didOpen notification
                doc_uri = "file:///untitled.lean"
                
                # 1. Send initialize request
                init_request = {
                    "jsonrpc": "2.0",
                    "id": self._next_id(),
                    "method": "initialize",
                    "params": {
                        "processId": None,
                        "clientInfo": {"name": "lean-visualizer"},
                        "rootUri": None,
                        "capabilities": {}
                    }
                }
                await ws.send(json.dumps(init_request))
                
                # 2. Wait for initialize response and then send initialized notification
                init_response = await asyncio.wait_for(ws.recv(), timeout=10)
                
                initialized_notification = {
                    "jsonrpc": "2.0",
                    "method": "initialized",
                    "params": {}
                }
                await ws.send(json.dumps(initialized_notification))
                
                # 3. Open the document
                did_open = {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": doc_uri,
                            "languageId": "lean4",
                            "version": 1,
                            "text": code
                        }
                    }
                }
                await ws.send(json.dumps(did_open))
                
                # 4. Collect responses (diagnostics, etc.)
                # The server will send diagnostics and other info as notifications
                deadline = asyncio.get_event_loop().time() + timeout
                
                while asyncio.get_event_loop().time() < deadline:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                        data = json.loads(msg)
                        
                        # Handle diagnostic notifications
                        if data.get("method") == "textDocument/publishDiagnostics":
                            diagnostics = data.get("params", {}).get("diagnostics", [])
                            result["diagnostics"].extend(diagnostics)
                            
                            # Check for errors
                            for diag in diagnostics:
                                if diag.get("severity") == 1:  # 1 = Error in LSP
                                    result["success"] = False
                        
                        # Handle any info messages
                        if "result" in data or "params" in data:
                            result["messages"].append(data)
                        
                        # If we see the $/lean/fileProgress complete, we're done
                        if data.get("method") == "$/lean/fileProgress":
                            processing = data.get("params", {}).get("processing", [])
                            if not processing:  # Empty means done processing
                                break
                                
                    except asyncio.TimeoutError:
                        # No more messages, we're probably done
                        break
                
                # 5. Try to get goal state at various positions
                # Find positions where we have tactics
                tactic_positions = find_tactic_positions(code)
                
                for line, col in tactic_positions[:10]:  # Limit to 10 positions
                    hover_request = {
                        "jsonrpc": "2.0",
                        "id": self._next_id(),
                        "method": "$/lean/plainGoal",  # Lean-specific method for goals
                        "params": {
                            "textDocument": {"uri": doc_uri},
                            "position": {"line": line, "character": col}
                        }
                    }
                    await ws.send(json.dumps(hover_request))
                    
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=2.0)
                        data = json.loads(response)
                        
                        if "result" in data and data["result"]:
                            goal_info = data["result"]
                            result["goals"].append({
                                "line": line + 1,  # Convert to 1-indexed
                                "column": col + 1,
                                "goals": goal_info.get("goals", []),
                                "rendered": goal_info.get("rendered") or str(goal_info)
                            })
                    except asyncio.TimeoutError:
                        continue
                
                # Close document
                did_close = {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {
                        "textDocument": {"uri": doc_uri}
                    }
                }
                await ws.send(json.dumps(did_close))
                
        except WebSocketException as e:
            result["success"] = False
            result["diagnostics"].append({
                "message": f"WebSocket error: {str(e)}",
                "severity": 1
            })
        except asyncio.TimeoutError:
            result["diagnostics"].append({
                "message": "Timeout waiting for Lean server response",
                "severity": 2
            })
        except Exception as e:
            result["success"] = False
            result["diagnostics"].append({
                "message": f"Connection error: {str(e)}",
                "severity": 1
            })
        
        return result


def find_tactic_positions(code: str) -> list[tuple[int, int]]:
    """
    Find positions in code where we might want to query for goals.
    Returns list of (line, column) tuples (0-indexed).
    """
    positions = []
    lines = code.split("\n")
    
    in_tactic_mode = False
    
    for line_num, line in enumerate(lines):
        # Check if entering tactic mode
        if ":= by" in line or line.strip() == "by":
            in_tactic_mode = True
            # Position right after 'by'
            by_pos = line.find("by")
            if by_pos >= 0:
                positions.append((line_num, by_pos + 2))
            continue
        
        if not in_tactic_mode:
            continue
        
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        
        # Position at start of tactic
        col = len(line) - len(line.lstrip())
        positions.append((line_num, col))
    
    return positions


def parse_goal_state(goal_text: str) -> tuple[list[str], list[str]]:
    """
    Parse a goal state string into hypotheses and goals.
    
    Example input:
    ```
    h : A
    h2 : B
    ⊢ C
    ```
    
    Returns: (hypotheses, goals)
    """
    hypotheses = []
    goals = []
    
    lines = goal_text.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("⊢") or line.startswith("|-"):
            goal = line.lstrip("⊢").lstrip("|-").strip()
            if goal:
                goals.append(goal)
        elif ":" in line and not line.startswith("case"):
            hypotheses.append(line)
    
    return hypotheses, goals


# Singleton instance
_client: Lean4WebClient | None = None


def get_lean_client() -> Lean4WebClient:
    """Get or create the Lean4Web client singleton."""
    global _client
    if _client is None:
        _client = Lean4WebClient()
    return _client
