#!/usr/bin/env python3
import json, html
from pathlib import Path
r=json.loads(Path('reports/agentic_contract_suite_v2_summary.json').read_text())
rows=[]
for name,v in r['policies'].items():
    rows.append(f"<tr><td>{html.escape(name)}</td><td>{v['trial_success']:.3f}</td><td>{v['hard_safe']:.3f}</td><td>{v['injection_resistance']:.3f}</td><td>{v['pass@5']:.3f}</td><td>{v['all_success@5']:.3f}</td></tr>")
page='''<!doctype html><meta charset="utf-8"><title>Agentic Contract Suite v2</title><style>body{font-family:system-ui;max-width:980px;margin:48px auto;padding:0 24px;color:#171717}table{border-collapse:collapse;width:100%}th,td{padding:10px;border-bottom:1px solid #ddd;text-align:left}.note{background:#f5f5f5;padding:14px;border-radius:8px}</style><h1>Agentic Contract Suite v2</h1><p class="note">Evaluator stress test only — these are reference-policy sanity checks, not LLM capability results.</p><p>288 stateful scenarios × 5 repeated trials per scenario, including clean, stale-memory, and tool-injection variants.</p><table><thead><tr><th>Policy</th><th>Trial success</th><th>Hard-safe</th><th>Injection resistance</th><th>pass@5</th><th>all-success@5</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table><p>The gap between pass@5 and all-success@5 for the noisy policy demonstrates why repeated-trial reliability must be reported.</p>'''
Path('demo/agentic_eval_v2.html').write_text(page)
