# ST-04 data access

Route metadata records API #08 and #15, but this gate page has no HTTP caller.

- API #08 is a public read, but the route's `courseId` to `course_id:int64` mapping is not approved.
- API #15 has no route/module/query/model/test in the Study Server checkout and its Draft public response does not identify the current Student's enrollment.
- Do not derive free/paid, already-enrolled, or checkout branches from display price or a guessed enrollment row.

Keep the page in its static verification gate until the route parameter and enrollment identity/selection contract are resolved.
