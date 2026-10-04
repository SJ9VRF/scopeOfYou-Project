# Security

This repository is a research artifact, not a production multi-tenant service.

## Scope

The local inference API binds to `127.0.0.1` by default, caps JSON request bodies at 1 MB, does not return Python stack traces to clients, and does not persist request bodies. Binding to `0.0.0.0` is intended for an isolated container/demo environment only.

Do not expose the demo API directly to the public Internet without authentication, TLS termination, request-rate controls, logging/privacy policy, and network isolation appropriate to the deployment.

## Sensitive data

The released benchmark uses synthetic users. Do not add raw private conversations, access tokens, API keys, credentials, or other secrets to the repository. `make audit` performs a lightweight committed-secret scan, but it is not a substitute for organization-grade secret scanning.

## Reporting

For a public fork, use the hosting provider's private vulnerability reporting mechanism rather than filing an issue containing exploit details or secrets.
