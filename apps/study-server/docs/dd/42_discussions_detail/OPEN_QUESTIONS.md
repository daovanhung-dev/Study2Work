# OPEN_QUESTIONS — Study API #42

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/discussions/{discussion_id}

## Q-42-01 — Required title source

**Evidence:** Reusable Discussion requires title:string; DB guide, ERD and checked-in DDL contain no discussions.title.

**Impact:** A complete Discussion response cannot be populated from the documented table. This DD does not derive the title from content.

**Decision needed:** Identify an approved title source or update the contract/schema.

## Q-42-02 — ACTIVE enrollment and visibility policy

**Evidence:** AC-19 requires course discussion permission. DDL defines enrollment status and discussion status with ACTIVE defaults, but API #42 does not define allowed membership/topic/comment statuses.

**Impact:** The service cannot know which Students may read a topic or which rows are public.

**Decision needed:** Confirm or replace the DERIVED proposal: Student has an enrollment with status ACTIVE for root.course_id; root and visible comments have status ACTIVE.

## Q-42-03 — Root topic and direct child boundary

**Evidence:** API #42 path names discussion_id; DB uses self-referencing parent_id; AC-19 reads topic plus comments. API #41 DD proposes direct-child replies to a root.

**Impact:** Allowing a comment ID could create nested response trees, which are not modeled by DiscussionComment[] in this simple flow.

**Decision needed:** Confirm that #42 accepts root IDs only and returns only their direct child comments.

## Q-42-04 — Comment ordering

**Evidence:** AC-19 says display the latest thread but does not define comment order. Existing API #10 DD orders root items newest first but does not specify reply order.

**Impact:** Thread presentation may differ between reloads or clients.

**Decision needed:** Confirm chronological order by created_at ASC with id ASC as a deterministic tie-break.

## Q-42-05 — Page<Discussion> detail semantics

**Evidence:** Catalog returns Page<Discussion> for one discussion_id and provides no page/query inputs. PageMeta requires page, size, total, total_pages.

**Impact:** The response requires pagination values even though the operation reads one thread.

**Decision needed:** Confirm the DERIVED one-item page: page=1, size=1, total=1, total_pages=1.

## Q-42-06 — All comments or a bounded subset

**Evidence:** Discussion.comments is an array and API #42 has no comment pagination/limit fields.

**Impact:** Returning all active direct comments can make a large thread response costly.

**Decision needed:** Confirm all direct comments are returned; if a limit/cursor is needed, update the catalog before adding request fields.

## Q-42-07 — Required author versus nullable DB relation

**Evidence:** Discussion and DiscussionComment require author:UserSummary; DB guide marks user relation required, but checked-in DDL permits discussions.user_id NULL.

**Impact:** Null/missing author rows cannot satisfy the response schema.

**Decision needed:** Confirm canonical FK nullability and use of a data-integrity 500 when author projection is missing.

## Q-42-08 — Invalid discussion_id parsing

**Evidence:** Catalog path type is int64 and errors omit 422; FastAPI path parsing may normally reject an invalid integer before endpoint logic.

**Impact:** Framework behavior may produce a status/business code outside the approved catalog.

**Decision needed:** Confirm the DERIVED 404 mapping for malformed/unknown/non-root IDs, or update the catalog with the intended validation response.

