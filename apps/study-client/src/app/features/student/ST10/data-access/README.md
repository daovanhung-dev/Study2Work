# ST-10 data access

APIs #22, #23 and #24 have current Study Server route/module/query/model/test
source and are assigned in route metadata. ST10 calls #22 when its route opens
and calls #23 only after the learner presses **Bắt đầu học**, and only when #22
returns a matching lesson with `status === 'PUBLISHED'`. `StudentApiService`
obtains the Student access token before dispatching either request. ST11 owns
the #24 detail request after the handoff.

ST10 maps the response to a preview and does not render `content` or
`video_url`. Keep the start action gated on the matching lesson ID and
published status. The server source does not filter lesson status in #22 and
does not independently check publication in #23; access/reason, retry and
idempotency semantics remain unresolved in the DD. The ST-09 screen still has
no lesson selection/`lessonId` handoff, and deployed runtime behavior is not
verified.
