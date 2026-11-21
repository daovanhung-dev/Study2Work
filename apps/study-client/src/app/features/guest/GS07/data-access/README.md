# GS-07 data access

`GS07ResourceService` calls API #12 with the exact path `resource_id`. Guest
requests are public; an authenticated Student request carries the Student
Bearer token. Current backend source returns public resource URLs directly and
issues a five-minute signed URL for private resources only after ACTIVE
enrollment is confirmed. The client validates the returned resource identity,
metadata and URL scheme before exposing an external link, and opens it with
`noopener noreferrer`.

The response ID is a JSON number while the backend accepts signed-int64 paths;
the page fails closed if the returned ID is outside JavaScript's safe integer
range or does not match the requested ID. The page has no embedded preview or
MIME-specific download policy. `resources` also has no current writer from
ME-04 (#47), which persists upload references in `lesson_uploads` instead.
