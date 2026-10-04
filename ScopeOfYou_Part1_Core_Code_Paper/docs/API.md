# Local inference API

The CPU behavioral checkpoint can be served without FastAPI/Flask or network downloads.

```bash
bounded-self-serve --checkpoint checkpoints/sft_behavior_v31.pt --host 127.0.0.1 --port 8765
```

## Health

`GET /health`

Example response:

```json
{"status":"ok","checkpoint":"checkpoints/sft_behavior_v31.pt"}
```

## Predict

`POST /predict` with `Content-Type: application/json`.

```json
{
  "user_id": "demo-user",
  "user_state": {
    "verbosity": "concise",
    "directness": "high",
    "technical_depth": "advanced",
    "confirmation_policy": "irreversible_only",
    "correction_tolerance": "direct",
    "proactivity": 0.4
  },
  "current_query": "What is the capital of Germany?"
}
```

Response includes the generated behavioral response plus predicted dimensions for personalization, factuality, sycophancy, proactivity, and helpfulness.

The service binds to localhost by default, rejects bodies larger than 1 MB, returns structured errors, and does not emit stack traces to clients. It is a research/demo service, not a production authentication or multi-tenant layer.
