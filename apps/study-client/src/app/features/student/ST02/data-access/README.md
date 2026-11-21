# ST-02 data access

`ST02ProfileService` calls API #04 (`GET /api/v1/users/me`) through
`StudentApiService`, which obtains the in-memory Student Bearer token and ends
the local session on protected 401 responses. The page displays only the
response-backed `full_name` and `email`; avatar URL rendering, role/status
claims, bio, permissions and edit behavior are not inferred.
