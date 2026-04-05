<h1>API Documentation</h1>

<p>
  This service exposes REST endpoints for Users, URLs, and Events.  
  All responses are JSON and follow standard HTTP semantics.  
  Errors are returned in a consistent structured format.
</p>

<hr/>

<h2>Users API</h2>

<h3>POST /users</h3>
<p>Create a new user.</p>

<strong>Request Body</strong>
<pre>
{
  "username": "string",
  "email": "string"
}
</pre>

<hr/>

<h3>GET /users</h3>
<p>Return all users.</p>

<hr/>

<h3>GET /users/&lt;id&gt;</h3>
<p>Return one user by ID. Returns 404 if not found.</p>

<hr/>

<h3>PUT /users/&lt;id&gt;</h3>
<p>Update a user's information.</p>

<strong>Request Body (any subset)</strong>
<pre>
{
  "username": "string",
  "email": "string"
}
</pre>

<hr/>

<h3>DELETE /users/&lt;id&gt;</h3>
<p>Delete a user by ID.</p>

<hr/>

<h3>POST /users/bulk</h3>
<p>Upload a CSV file to bulk‑create users.</p>

<strong>CSV Format</strong>
<pre>
username,email
alice,alice@example.com
bob,bob@example.com
</pre>

<hr/>

<h2>URLs API</h2>

<h3>POST /urls</h3>
<p>Create a shortened URL.</p>

<strong>Request Body</strong>
<pre>
{
  "user_id": 1,
  "original_url": "https://example.com",
  "title": "optional"
}
</pre>

<strong>Advanced Behavior</strong>
<ul>
  <li>Identical URLs submitted by the same user return the existing short URL (deduplication).</li>
  <li>Shortcode generation uses collision‑safe retry logic.</li>
</ul>

<hr/>

<h3>GET /urls</h3>
<p>List URLs.</p>

<strong>Filters</strong>
<ul>
  <li>?user_id=&lt;id&gt;</li>
  <li>?is_active=true|false</li>
</ul>

<hr/>

<h3>GET /urls/&lt;id&gt;</h3>
<p>Return URL details.</p>

<hr/>

<h3>PUT /urls/&lt;id&gt;</h3>
<p>Update title or activation status.</p>

<strong>Request Body</strong>
<pre>
{
  "title": "string",
  "is_active": true
}
</pre>

<hr/>

<h3>DELETE /urls/&lt;id&gt;</h3>
<p>Delete a URL by ID.</p>

<hr/>

<h3>GET /urls/&lt;shortcode&gt;/redirect</h3>
<p>Redirect to the original URL.</p>

<strong>Behavior</strong>
<ul>
  <li>302 Found if URL is active</li>
  <li>410 Gone if inactive</li>
  <li>404 Not Found if shortcode is unknown</li>
</ul>

<hr/>

<h2>Events API</h2>

<h3>POST /events</h3>
<p>Create or update an event.</p>

<strong>Request Body</strong>
<pre>
{
  "event_type": "string",
  "url_id": 1,
  "user_id": 1,
  "details": { "key": "value" }
}
</pre>

<strong>Advanced Behavior</strong>
<ul>
  <li>Event entries with identical (event_type, url_id, user_id) are merged.</li>
  <li>Details from repeated events are merged rather than overwritten.</li>
</ul>

<hr/>

<h3>GET /events</h3>
<p>List all events.</p>

<strong>Filters</strong>
<ul>
  <li>?url_id=&lt;id&gt;</li>
  <li>?user_id=&lt;id&gt;</li>
  <li>?event_type=&lt;string&gt;</li>
</ul>

<hr/>
