# Privacy

Sanitization and trajectory handling requirements.

## Data Handling

- Raw jobs and trajectories must live in `ERIKFRYSCOK_HARBOR_JOBS_DIR` outside the repo.
- Published artifacts must be sanitized.

## Redaction Rules

Sanitization must remove or redact:

- credentials/tokens
- emails and user home paths
- repository URLs and sensitive absolute paths
- unsanitized trajectory payloads

## Credential Isolation

- Do not mount or expose host Git credentials.
- Use named environment variables only for optional hosted credentials.
- Evaluation environments should fail closed when required services are unavailable.
