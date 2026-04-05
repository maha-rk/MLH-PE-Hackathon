# Incident Response Runbook

## Service Down
1. Check /health endpoint.
2. Restart the service.
3. Inspect logs.

## High Error Rate
1. Check Grafana dashboard.
2. Inspect application logs.
3. Restart if necessary.

## Slow Response Time
1. Check CPU/memory usage.
2. Confirm DB is responsive.
3. Restart service if needed.

## Redirect Failures
1. Check URL’s is_active status.
2. Reactivate if needed via PUT request.

## Database Issues
1. Stop service.
2. Backup database.
3. Recreate only in development.

## Recovery Steps
1. Restart.
2. Validate /health.
3. Check Prometheus metrics.
4. Confirm Grafana dashboards updated.
