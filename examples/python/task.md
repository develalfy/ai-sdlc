# Task — synthetic-healthz-endpoint

## Goal

Add a single read-only HTTP health probe endpoint to the synthetic example
service so external monitors and orchestration systems can verify the process
is reachable and self-reports a known-good state. No persistence, no auth, no
side effects.

## Acceptance criteria

- [ ] Given the FastAPI app is running, when a client sends `GET /api/v1/healthz`
      with no body and no headers, then the response status code is `200`.
- [ ] Given the FastAPI app is running, when a client sends `GET /api/v1/healthz`,
      then the response body decodes as JSON with `status == "ok"` and
      `version == "0.1.0"`.
- [ ] Given the FastAPI app is running, when a client sends `GET /api/v1/healthz`,
      then the response `Content-Type` header starts with `application/json`.

## Out of scope

- Readiness/liveness split, dependency probes, DB ping, cache checks.
- Authentication, rate limiting, CORS, request logging middleware.
- A readiness route under `/api/v1/readyz` or any non-`healthz` paths.
- Versioning beyond the hard-coded `"0.1.0"` string.
- Packaging (Dockerfile, pyproject.toml, CI config).