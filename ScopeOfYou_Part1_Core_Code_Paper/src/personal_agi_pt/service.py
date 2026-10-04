from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .learned_policy import LearnedPersonalPolicy
from .schema import InteractionRecord


def _record_from_payload(payload: dict[str, Any]) -> InteractionRecord:
    return InteractionRecord(
        conversation_id=str(payload.get("conversation_id", "api")),
        user_id=str(payload.get("user_id", "anonymous")),
        user_state=dict(payload.get("user_state", {})),
        history=list(payload.get("history", [])),
        current_query=str(payload.get("current_query", "")),
        candidate_response=str(payload.get("candidate_response", "")),
        provenance="synthetic",
        confidence=float(payload.get("confidence", 1.0)),
        dataset_version="api",
        split="test",
        metadata=dict(payload.get("metadata", {})),
    )


class PolicyService:
    def __init__(self, checkpoint: str):
        self.checkpoint = checkpoint
        self.policy = LearnedPersonalPolicy(checkpoint)

    def health(self) -> dict[str, Any]:
        return {"status": "ok", "checkpoint": self.checkpoint}

    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = _record_from_payload(payload)
        if not record.current_query.strip():
            raise ValueError("current_query must be non-empty")
        out = self.policy.predict(record)
        return {
            "conversation_id": record.conversation_id,
            "user_id": record.user_id,
            "response": out.response,
            "behavior": {k: float(v) for k, v in out.behavior.items()},
        }


def make_handler(service: PolicyService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "PersonalAGIPT/0.4"

        def _send(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:  # noqa: N802
            self._send(204, {})

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/health":
                self._send(200, service.health())
            else:
                self._send(404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/predict":
                self._send(404, {"error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_000_000:
                    raise ValueError("invalid request body size")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise ValueError("JSON body must be an object")
                self._send(200, service.predict(payload))
            except (ValueError, json.JSONDecodeError) as exc:
                self._send(400, {"error": "bad_request", "detail": str(exc)})
            except Exception as exc:  # keep API errors structured; no stack traces to client
                self._send(500, {"error": "internal_error", "detail": type(exc).__name__})

        def log_message(self, fmt: str, *args: Any) -> None:
            return

    return Handler


def serve(checkpoint: str, host: str = "127.0.0.1", port: int = 8765) -> None:
    service = PolicyService(checkpoint)
    httpd = ThreadingHTTPServer((host, port), make_handler(service))
    print(json.dumps({"status": "serving", "host": host, "port": port, "checkpoint": checkpoint}))
    httpd.serve_forever()


def main() -> None:
    p = argparse.ArgumentParser(description="Serve a trained behavioral checkpoint over a tiny JSON API")
    p.add_argument("--checkpoint", default="checkpoints/sft_behavior_v31.pt")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    if not Path(a.checkpoint).exists():
        raise SystemExit(f"checkpoint not found: {a.checkpoint}")
    serve(a.checkpoint, a.host, a.port)


if __name__ == "__main__":
    main()
