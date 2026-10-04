# GitHub Publishing — Scope of You

**Author:** Aura Yavary

This repository is publish-ready. A public GitHub URL is not fabricated inside the project because no external repository has been created from this environment.

## Repository contents

- Research paper and technical report
- Reproducible training, reward-model, contract-optimization, evaluation, and failure-mining code
- PersonalBench-Contract benchmark artifacts
- Dataset and model cards
- Interactive demo, trajectory viewer, dashboard, and video
- Public-benchmark adapters
- Tests, CI workflow, Docker configuration, release audits, and no-project-date audit

## Recommended repository name

`bounded-self`

## Publish steps

```bash
git init
git add .
git commit -m "Release Scope of You"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## Before publishing

```bash
make test
make project-page-audit
make date-audit
make audit
```

Do not insert a fake GitHub URL into the homepage. Once an actual repository exists, replace the local Code/GitHub links with that verified URL.
