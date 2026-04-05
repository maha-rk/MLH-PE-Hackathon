<h1>Incident Response Runbook</h1>

<p>
This runbook documents the operational steps required to diagnose and restore service functionality during incidents affecting the URL Shortener platform.
It is intended for engineers responsible for maintaining reliability, performance, and uptime.
</p>

<hr/>

<h2>1. Service Down</h2>

<h3>Symptoms</h3>
<ul>
  <li><code>/health</code> endpoint does not respond</li>
  <li>All API requests fail</li>
  <li>"Service Down" alert email received</li>
</ul>

<h3>Immediate Actions</h3>
<ol>
  <li>Validate service state:<br/>
    <pre>curl http://localhost:5003/health</pre>
  </li>
  <li>Restart application:<br/>
    <pre>
pkill -f python
uv run python run.py
    </pre>
  </li>
  <li>Review logs for stack traces or crashes.</li>
</ol>

<h3>Likely Root Causes</h3>
<ul>
  <li>Application process crash</li>
  <li>Database locked or corrupted</li>
  <li>Memory or CPU exhaustion</li>
</ul>

<hr/>

<h2>2. Elevated Error Rate</h2>

<h3>Symptoms</h3>
<ul>
  <li>Error rate spike visible in Grafana</li>
  <li>"High Error Rate" alert triggered</li>
  <li>API returning 4xx or 5xx responses frequently</li>
</ul>

<h3>Diagnostic Procedure</h3>
<ol>
  <li>Identify failing endpoints on the Grafana dashboard.</li>
  <li>Inspect logs:<br/>
    <pre>tail -f logs/app.log</pre>
  </li>
  <li>Validate state of affected URLs via <code>/urls/&lt;id&gt;</code>.</li>
  <li>Review recent events using the <code>/events</code> endpoint.</li>
</ol>

<h3>Likely Root Causes</h3>
<ul>
  <li>Malformed requests from clients</li>
  <li>URL unintentionally deactivated</li>
  <li>Unhandled application exception</li>
</ul>

<hr/>

<h2>3. High Latency</h2>

<h3>Symptoms</h3>
<ul>
  <li>Latency panel spikes on Grafana</li>
  <li>API responses slow to complete</li>
</ul>

<h3>Troubleshooting</h3>
<ol>
  <li>Check CPU and Memory usage in Grafana.</li>
  <li>Inspect logs for long-running operations.</li>
  <li>Restart service if the issue persists.</li>
</ol>

<h3>Likely Causes</h3>
<ul>
  <li>CPU saturation</li>
  <li>Memory pressure or leak</li>
  <li>Database contention or slow I/O</li>
</ul>

<hr/>

<h2>4. Redirect Failures</h2>

<h3>Symptoms</h3>
<ul>
  <li><code>/r/&lt;shortcode&gt;</code> returns 410 or 404</li>
  <li>Redirect stops functioning for certain URLs</li>
</ul>

<h3>Recovery Steps</h3>
<ol>
  <li>Inspect the URL record:<br/>
    <pre>curl http://localhost:5003/urls/&lt;id&gt;</pre>
  </li>
  <li>If <code>is_active=false</code>, reactivate the URL:<br/>
    <pre>
curl -X PUT -H "Content-Type: application/json" \
  -d '{"is_active": true}' http://localhost:5003/urls/&lt;id&gt;
    </pre>
  </li>
</ol>

<h3>Likely Causes</h3>
<ul>
  <li>URL was manually deactivated</li>
  <li>Incorrect update request</li>
</ul>

<hr/>

<h2>5. Database Issues</h2>

<h3>Symptoms</h3>
<ul>
  <li>Database errors in logs</li>
  <li>Intermittent failing API requests</li>
  <li>Missing or inconsistent records</li>
</ul>

<h3>Procedure</h3>
<ol>
  <li>Stop the service.</li>
  <li>Backup <code>database.db</code>.</li>
  <li>Reinitialize schema if required (development only).</li>
  <li>Restart the service.</li>
</ol>

<hr/>

<h2>6. Full Recovery Checklist</h2>

<ol>
  <li>Restart the service.</li>
  <li>Verify <code>/health</code> returns OK.</li>
  <li>Confirm <code>/prom_metrics</code> responds.</li>
  <li>Check that Grafana dashboards are updating.</li>
  <li>Perform test requests for all major endpoints.</li>
  <li>Document the incident and recovery steps.</li>
</ol>

<hr/>
