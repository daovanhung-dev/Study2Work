# ST-04 data access

- Public course detail is revalidated through `GS03CourseDetailService` / API #08.
- Enrollment status and free enrollment use `StudentApiService` / APIs #15 and #19, which attach the in-memory Student Bearer token.
- API #15 currently resolves only the authenticated Student and returns the latest enrollment row for that Student/course. Its catalog actor is still marked Public; keep the contract discrepancy visible.
- A 404 from #15 after a published #08 response means no enrollment row was found for the authenticated Student. Only an `ACTIVE` row takes the already-enrolled path, matching API #19's current duplicate guard.
- API #19 runs only after an explicit free-enrollment action. API #20 must then confirm the course before ST-08 opens. A failed #20 refresh never resends #19.
- Paid courses hand off to ST-05 with the course ID; payment success and paid entitlement are never inferred in ST-04.
