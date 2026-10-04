# Security and Privacy Design

This repository uses synthetic identifiers and synthetic user profiles by default. No production user data is required.

For real human studies, the system should enforce data minimization, informed consent, retention windows, deletion support, access control, and separation of identity from research records. Raw free-text should be scanned for accidental secrets and personally identifying data before training. User-state fields should distinguish explicit statements from inferred attributes, and sensitive inference should be excluded unless the study protocol specifically permits it.

Model artifacts can memorize training records. Public releases therefore require a privacy review, membership-inference checks where appropriate, and a decision on whether weights, adapters, or only aggregate metrics should be released.

Annotation exports must avoid exposing one participant's history to another annotator. Logs should redact credentials, tokens, and private tool outputs. External model APIs must not receive private records unless their data handling terms are compatible with the study protocol.
