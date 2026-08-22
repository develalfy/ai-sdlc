# Task — healthz endpoint

## Goal

Add a `GET /api/v1/healthz` endpoint that returns a small JSON payload so
uptime probes and smoke tests can confirm the service is responding.

## Acceptance criteria

1. **Given** the Symfony router is configured for the `/api/v1` prefix,
   **when** a client sends `GET /api/v1/healthz`,
   **then** the response is HTTP 200 with `Content-Type: application/json`
   and body `{"status":"ok","version":"0.1.0"}`.

2. **Given** a successful response from the endpoint,
   **when** the client decodes the body as JSON,
   **then** the decoded payload has exactly two keys: `status` (string,
   value `"ok"`) and `version` (string, value `"0.1.0"`).

3. **Given** the endpoint exists at `/api/v1/healthz`,
   **when** a client sends `POST /api/v1/healthz`,
   **then** the response is HTTP 405 (Method Not Allowed) — the route is
   only registered for `GET`.

## Out of scope

- Authentication, rate limiting, CORS, or any cross-cutting middleware.
- Database, cache, or external dependency checks (this is a static liveness
  probe, not a readiness/readiness probe with downstream checks).
- Version discovery from `composer.json`, env vars, or git tags; the version
  string is a literal constant in the controller.
- New routes other than `GET /api/v1/healthz`.
- Refactoring of existing controllers, services, or the Symfony kernel.
- Documentation beyond what the protocol requires (`task.md` + `DONE.md`).
