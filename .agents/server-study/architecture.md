# Study Server architecture

## Intended composition visible in current source

```text
app/main.py:create_app
  -> app/api/v1.py:router
  -> app/core/config.py
  -> app/core/database.py
  -> app/core/middleware.py
  -> app/core/responses.py
  -> app/core/trace.py
```

Current composition, API #1 register flow, API #2 verify-email dispatch stub,
API #3 login/refresh flow, API #4 current-user flow, API #5 category flow,
API #6 public course flow, API #7 course-search flow, API #12 resource detail,
API #13 avatar upload and API #14 profile update are present. The auth,
verification, category and course test modules use the `guest`
namespace and the full test collection is available; routes without a current
implementation remain unwired.

## Verified ownership

- `app/main.py`: FastAPI composition root, CORS, middleware/exception-handler registration, root/health routes.
- `app/api/v1.py`: declared `/api/v1` routes; exposes health-adjacent utility
  routes, API #1 register, API #2 verification dispatch, API #3 auth, API #4
  current-user profile, API #5 categories, API #6 courses, API #7 course search,
  API #12 resource detail, API #13 avatar upload and API #14 profile update.
- `app/core/config.py`: typed settings backed by `app/core/constants.py`.
- `app/core/database.py`: sync SQLAlchemy engine/session/query primitives.
- `app/core/middleware.py`: trace middleware and shared FastAPI exception handlers.
- `app/core/security/*`: password, access token, refresh token primitives.
- `app/utils/auth.py`: shared Bearer/JWT parsing and claim checks, Student current-user guard, refresh-token input validation, access/refresh token issuance, expiry metadata and public auth payload mapping. It delegates cryptographic operations to `app/core/security`.
- `app/utils/validate.py`: shared pure input normalization/validation helpers used by API validators, such as email, blank-value, sort and search handling; it does not own Bearer/JWT/token helpers.
- `app/modules/guest/api_03_auth_login/models.py`: login and refresh request contracts.
- `app/modules/guest/api_03_auth_login/query.py`: SQL constants for user lookup and refresh-token persistence.
- `app/modules/guest/api_03_auth_login/view.py`: login credential flow, refresh rotation, transaction and response mapping.
- `app/modules/guest/api_04_users_me/models.py`: safe current-user profile response model.
- `app/modules/guest/api_04_users_me/query.py`: parameterized public profile lookup by user ID.
- `app/modules/guest/api_04_users_me/view.py`: Student role check, profile lookup and canonical response/error mapping.
- `app/modules/guest/api_05_categories/models.py`: API #5 query and public category page model classes.
- `app/modules/guest/api_05_categories/query.py`: parameterized active-category lookup by exact locale.
- `app/modules/guest/api_05_categories/view.py`: default-locale resolution, category mapping and canonical response/error mapping.
- `app/modules/guest/api_06_courses/models.py`: API #6 list query contract.
- `app/modules/guest/api_06_courses/query.py`: parameterized published-course/count queries.
- `app/modules/guest/api_06_courses/view.py`: public course list filtering, mentor-integrity checks and response mapping.
- `app/modules/guest/api_07_courses_search/models.py`: API #7 search query contract.
- `app/modules/guest/api_07_courses_search/query.py`: parameterized published-course search/count queries.
- `app/modules/guest/api_07_courses_search/view.py`: public course search filtering and response mapping.
- `app/modules/guest/api_12_resources_detail/view.py`: public resource metadata retrieval and published-parent check; current response returns the stored resource URL directly.
- `app/modules/guest/api_13_users_me_avatar/models.py`: strict JSON Data URL request and `AvatarUploadResult` response model.
- `app/modules/guest/api_13_users_me_avatar/validate.py`: Student Bearer guard plus strict Base64, MIME/signature and decoded-size validation.
- `app/modules/guest/api_13_users_me_avatar/view.py`: upload orchestration and safe storage-failure mapping without database access.
- `app/service/object_storage/avatar.py`: lazy, injectable S3-compatible avatar provider backed by process environment and public URL base.
- `app/modules/guest/api_14_users_me_profile/view.py`: Student profile update; consumes `avatar_url` submitted in the follow-up request.
- `app/modules/guest/_shared/course_catalog/models.py`: shared course, mentor and pagination response contracts.
- `app/modules/guest/_shared/course_catalog/helpers.py`: shared sort, course mapping and safe error helpers.
- `app/modules/guest/api_02_auth_verify_email_send/models.py`: strict public `user_id` and `email` request contract.
- `app/modules/guest/api_02_auth_verify_email_send/view.py`: provider dispatch orchestration and canonical response/error mapping without DB access.
- `app/service/email/provider.py`: injectable verification-email provider Protocol, result type and development stub.
- `app/modules/guest/api_01_auth_register/models.py`: API #1 register request
  model fields and type conversion.
- `app/modules/guest/api_01_auth_register/validate.py`: active request validator
  for email, password and full name; returns `error_response(...)` for invalid
  input and normalized model data otherwise.
- `app/modules/guest/api_01_auth_register/query.py`: duplicate lookup and users
  insert SQL constants; query execution is owned by `view.py`.
- `app/modules/guest/api_01_auth_register/view.py`: register orchestration,
  business check, password hashing, transaction and response mapping.
- `app/service/ai/ollama_service.py`: Ollama adapter copied/shared with Study codebase; no live Study caller after business modules disappeared.

## Unwired ownership

No current source establishes:

- chat log business flow;
- real Email Provider delivery, verification token/link generation or retry worker;
- Study domain modules beyond API #1 register, API #2 stub dispatch, API #3 auth,
  API #4 current-user profile, API #5 categories, API #6 courses, API #7 course
  search, API #12 resource detail, API #13 avatar upload and API #14 profile update.

## Runtime compatibility repairs

1. `app.api.v1` imports the existing `app.modules.guest` package.
2. `responses.py` exposes `success_response` and `error_response(...)`; the latter directly builds an error `JSONResponse`.
3. `TraceIdMiddleware` uses the current trace helper names.

Together these repairs restore the current composition; future fix tasks must
re-evaluate the complete import chain rather than stop at the first error.

## Validation workflow boundary

```text
models.py: declarative model classes, fields/types/defaults and data conversion
→ app/utils/validate.py: shared pure input validation/normalization helpers
→ app/utils/auth.py: shared authentication and token helpers used by API #3, #4, #13 and #14
→ API-specific validate.py when request input rules exist; invalid input returns `error_response(...)`
→ query.py (only when SQL is needed): SQL statement constants
→ view.py: main API flow, query/provider calls, business checks, transactions and response mapping
```

Examples such as no whitespace or an allowed email domain are only applicable
when the API contract confirms them. Current API #1, #2, #3, #4, #6 and #7
validators map invalid input only through `error_response(...)`; API #5's
locale resolver currently only supplies a default and has no invalid-input
branch. API #2 calls an email provider without database access, so it has no
`query.py`. The current API #5 source still declares `DEFAULT_LOCALE` in
`models.py`; this is a placement discrepancy from the model-only rule and must
not be treated as the pattern for new code. No runtime relocation is implied by
this context note.

Auth login/refresh uses shared token helpers from `app/utils/auth.py` and input
normalization from `app/utils/validate.py`. APIs #4, #13 and #14 call the shared
Student authentication guard from `app/utils/auth.py`; API #13 validates its
Data URL before calling the injectable storage provider and does not access DB.
API #4 has no separate validator module. Module validators handle API-specific input rules before
business/DB operations; DB-backed business checks and transaction ownership
stay in `view.py`. Comments in `view.py` must explain
each meaningful operation in handlers and helpers; cohesive consecutive
statements may share a comment.
