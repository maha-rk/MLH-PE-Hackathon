<h1>Root Cause Analysis (RCA)</h1>

<h2>Incident Summary</h2>
<p>
On April 4th, the system experienced a noticeable spike in redirect failures. A URL had been unintentionally updated with 
<code>"is_active": false</code>, causing the redirect endpoint to return <code>410 Gone</code> for all requests to that shortcode.
The system behaved correctly based on its internal rules; however, the update was unintended and triggered a temporary outage for redirect functionality.
</p>

<hr/>

<h2>Timeline</h2>

<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Time</th><th>Event</th></tr>
  <tr><td>14:26</td><td>High Error Rate alert triggered</td></tr>
  <tr><td>14:27</td><td>Grafana dashboard shows spike in error count</td></tr>
  <tr><td>14:28</td><td>Redirect failures confirmed</td></tr>
  <tr><td>14:29</td><td>Logs show repeated 410 responses</td></tr>
  <tr><td>14:30</td><td><code>/events</code> reveals update event marking URL inactive</td></tr>
  <tr><td>14:32</td><td>URL manually reactivated via API</td></tr>
  <tr><td>14:33</td><td>Redirect behavior restored</td></tr>
  <tr><td>14:35</td><td>Error metrics return to normal baseline</td></tr>
</table>

<hr/>

<h2>Root Cause</h2>
<p>
A URL record was mistakenly updated to be inactive. 
The redirect handler returns <code>410 Gone</code> for inactive URLs, which is correct behavior. 
The issue was due to operator error rather than a code defect.
</p>

<hr/>

<h2>Impact</h2>
<ul>
  <li>Redirect functionality unavailable for approximately 9 minutes</li>
  <li>Increased error counts and latency in monitoring</li>
  <li>Alert system successfully notified operators</li>
</ul>

<hr/>

<h2>Contributing Factors</h2>
<ul>
  <li>No user-facing confirmation step for changes to URL activation status</li>
  <li>No dashboard panel highlighting inactive URLs</li>
  <li>Testing was performed on production-like URL data</li>
</ul>

<hr/>

<h2>Resolution</h2>
<p>The affected URL was reactivated with the following command:</p>

<pre>
curl -X PUT -H "Content-Type: application/json" \
  -d '{"is_active": true}' http://localhost:5003/urls/&lt;id&gt;
</pre>

<p>Redirect functionality was restored immediately.</p>

<hr/>

<h2>Preventative Actions</h2>
<ul>
  <li>Add Grafana visual indicators showing inactive URLs</li>
  <li>Add warnings or confirmation prompts for activation-state updates</li>
  <li>Improve runbook guidance around URL lifecycle management</li>
  <li>Establish safe testing procedures using isolated test records</li>
</ul>

<hr/>

<p><b>End of RCA</b></p>
