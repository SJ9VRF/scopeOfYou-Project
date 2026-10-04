# Examples

With the local service running:

```bash
bounded-self-serve --checkpoint checkpoints/sft_behavior_v31.pt
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/predict \
  -H 'Content-Type: application/json' \
  --data @examples/predict_request.json
```

Independent benchmark comparison:

```bash
bounded-self-benchmark \
  --dataset data/samples/personalbench_v31.jsonl \
  --checkpoint checkpoints/post_trained_v31_raw.pt \
  --reference-checkpoint checkpoints/sft_behavior_v31.pt \
  --split test \
  --draws 3000 \
  --output reports/checkpoint_comparison.json
```
