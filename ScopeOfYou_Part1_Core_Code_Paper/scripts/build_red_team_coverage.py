from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'agentic_contract_suite_v2.jsonl'
OUT_JSON = ROOT / 'reports' / 'red_team_coverage.json'
OUT_MD = ROOT / 'reports' / 'RED_TEAM_COVERAGE_MATRIX.md'

rows = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]

def counts(key):
    return dict(sorted(Counter(r[key] for r in rows).items(), key=lambda kv: str(kv[0])))

cross = defaultdict(int)
for r in rows:
    cross[(r['domain'], r['variant'])] += 1

summary = {
    'artifact_scope': 'evaluator_stress_suite_not_model_capability',
    'n_scenarios': len(rows),
    'dimensions': {
        'domain': counts('domain'),
        'variant': counts('variant'),
        'target_action': counts('target_action'),
        'ambiguity': counts('ambiguity'),
        'autonomy': counts('autonomy'),
        'reversibility': counts('reversibility'),
        'stakes': counts('stakes'),
    },
    'domain_by_variant': [
        {'domain': d, 'variant': v, 'n': n}
        for (d, v), n in sorted(cross.items())
    ],
    'coverage_claim': (
        'This artifact measures designed evaluator coverage only. It does not establish '
        'production security, model robustness, or red-team completeness.'
    ),
}
OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')

lines = [
    '# Red-Team Coverage Matrix',
    '',
    '> **Scope:** designed evaluator coverage, not a production-security or LLM-capability claim.',
    '',
    f"The agentic stress suite contains **{len(rows)} scenarios** across six state-changing domains. "
    'Every base task is instantiated as clean, stale-memory, and tool-injection variants.',
    '',
    '## Coverage dimensions',
    '',
    '| Dimension | Coverage |',
    '|---|---|',
]
for key in ['domain','variant','target_action','ambiguity','autonomy','reversibility','stakes']:
    vals = ', '.join(f'`{k}`: {v}' for k,v in summary['dimensions'][key].items())
    lines.append(f'| {key} | {vals} |')
lines += [
    '',
    '## Domain × perturbation',
    '',
    '| Domain | Clean | Stale memory | Tool injection |',
    '|---|---:|---:|---:|',
]
for d in sorted(summary['dimensions']['domain']):
    vals = {v: cross[(d,v)] for v in ['clean','stale_memory','tool_injection']}
    lines.append(f"| {d} | {vals['clean']} | {vals['stale_memory']} | {vals['tool_injection']} |")
lines += [
    '',
    '## Threats represented by the suite',
    '',
    '- **Stale preference application:** remembered preferences can outlive their validity.',
    '- **Tool-text instruction injection:** external tool content can try to bypass confirmation boundaries.',
    '- **Permission confusion:** personalization can be mistaken for authorization to take an action.',
    '- **Irreversible-action overreach:** a preference may justify a suggestion but not a destructive or committing action.',
    '- **Ambiguity under pressure:** uncertain intent should increase ASK/SUGGEST behavior rather than silent execution.',
    '- **Repeated-trial instability:** a policy that succeeds once can still be unreliable across repeats.',
    '',
    '## What this matrix does *not* prove',
    '',
    'The suite currently validates evaluator sensitivity using reference policies. It is **not evidence that PCO-Robust, a frontier LLM, or a deployed agent resists these threats**. Real-model red teaming is an external execution gate.',
]
OUT_MD.write_text('\n'.join(lines) + '\n')
print(f'wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}')
