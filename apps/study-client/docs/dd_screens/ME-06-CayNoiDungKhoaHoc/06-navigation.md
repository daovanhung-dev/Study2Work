# ME-06 — Navigation

## 1. Route definition

- Current route: /mentor/courses/:courseId/content
- Status: registered in mentor.route.ts; browser/runtime not verified.
- Route parameter: courseId must be a safe positive int64 before calling API #49.
- Authentication/authorization: MentorApiService supplies the Mentor token; API #49 checks MENTOR role and direct course ownership.

## 2. Entry points

| From | Trigger | Params | Current behavior |
|---|---|---|---|
| ME-03 workspace | Open content tree | courseId | Link targets this route. |
| ME-05 lecture detail | Open content tree | Validated course_id from #48 | Link targets this route. |

## 3. Destinations

| Destination | Trigger | Params | Condition |
|---|---|---|---|
| ME-07 editor | Add content or edit a row | courseId; contentId for edit | Links appear after #49 successfully confirms owner access. |
| ME-08 actions | Open a row's action flow | contentId; courseId in router state | Link appears after #49 successfully confirms owner access. |
| ME-03 workspace | Return to workspace | Current courseId | Available after successful load. |
| Mentor courses | Invalid/not-found/forbidden fallback | None | Available in error states. |

## 4. Refresh, route changes and errors

- paramMap follows a changed course ID and switchMap cancels the previous #49 request.
- Retry repeats the current course ID; component teardown closes the subscription.
- Invalid IDs stop before the API. API #49 maps malformed/out-of-range IDs and missing courses to 404.
- 403 is shown as an access-denied state; no course data or create/edit/action links are rendered.
- Browser refresh and deployed route behavior were not exercised.

## 5. API links

- Read: GET /api/v1/mentor/courses/{course_id}/content (#49), no body/query.
- Add/edit/publish/delete are separate ME-07/ME-08 routes and APIs #50–#53; ME-06 does not submit mutations or reorder requests.
