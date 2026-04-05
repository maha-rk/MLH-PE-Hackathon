# API Documentation

## Users API

### POST /users
Create a new user.

### GET /users
Return all users.

### GET /users/<id>
Return one user by ID.

### PUT /users/<id>
Update a user.

### DELETE /users/<id>
Delete a user.

### POST /users/bulk
Upload a CSV file to bulk‑create users.


## URLs API

### POST /urls
Create a shortened URL.

### GET /urls
List URLs. Supports:
- ?user_id=<id>
- ?is_active=true|false

### GET /urls/<id>
Return URL details.

### PUT /urls/<id>
Update title or activation status.

### DELETE /urls/<id>
Delete a URL.

### GET /urls/<shortcode>/redirect
Redirect to original URL.


## Events API

### POST /events
Create or update an event.

### GET /events
List events. Supports:
- ?url_id=<id>
- ?user_id=<id>
- ?event_type=<string>
