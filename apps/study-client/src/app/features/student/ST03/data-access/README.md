# ST-03 data access

`ST03ProfileService` calls API #04 (`GET /api/v1/users/me`), API #13
(`POST /api/v1/users/me/avatar`) and API #14 (`PUT /api/v1/users/me/profile`)
through `StudentApiService`, which adds the Student Bearer token.

- #13 receives only `{ image: Data URL }` with PNG/JPEG/WebP content up to 5 MiB and returns
  `avatar_url`; the page does not send multipart data.
- #14 receives exactly `full_name`, nullable `phone`, and nullable `avatar_url`. It does not persist
  `bio`, so the Bio control stays disabled.
- After a successful #14 update, the page calls #04 again before navigating to ST-02. If that read
  fails, it offers a read-only retry and does not resend the update.

The API behavior is source-backed; live object storage and database configuration are not verified.
