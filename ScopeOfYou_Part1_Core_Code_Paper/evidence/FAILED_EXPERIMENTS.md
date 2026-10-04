# What Didn't Work

Failures are retained because they changed the research direction.

## F-01 — Reward optimization exploited the learned reward
**What we expected.** We expected preference fit to improve without breaking factuality. Instead PersonalBench fell to 0.6240 and factuality to 0.0360.
**Why it failed.** The reward became exploitable outside the synthetic-pair support.
**What changed.** Added stronger anchoring/protected objectives; retained the failed run.

## F-02 — Explicit contract phrases produced a shortcut
**What we expected.** The first PCO looked good internally but failed the independent implicit suite.
**Why it failed.** Training/evaluation shared too much contract-language structure.
**What changed.** Kept the harder benchmark and redesigned training around disjoint natural paraphrases and history inference.

## F-03 — Paraphrase consistency optimized the wrong thing
**What we expected.** Macro contract score rose slightly while paraphrase robustness fell by 0.00136.
**Why it failed.** The regularizer moved aggregate behavior without fixing the target failure.
**What changed.** Rejected the variant despite the positive macro score.

## F-04 — Seed disagreement was not calibrated uncertainty
**What we expected.** Ambiguous cases did not show meaningfully larger seed disagreement: 1.032× ratio; AUROC 0.635.
**Why it failed.** Seed variance was an epistemic signal, not a calibrated ambiguity probability.
**What changed.** Report it only as a diagnostic and use selective-abstention curves.

## F-05 — The first dataset split was not trustworthy
**What we expected.** v1 contained 3,201 exact duplicates and users crossed train/validation.
**Why it failed.** The generator did not enforce user-level split integrity.
**What changed.** Rebuilt clean v2 with held-out users and zero exact duplicates; old outputs remain audit history.
