# ST-01 data access

The Student route is wrapped by `StudentLayout`, which establishes the Student
session before the page loads. ST-01 independently calls #20 for ACTIVE course
summaries and #38 for recorded achievements through `StudentApiService`. The
page validates each success envelope, exact business code, response projection
and source-backed ordering, and offers per-widget retry. #21 remains gated
because the current endpoint returns `UserProfile`; #43 remains gated because
its query depends on `notification_recipients`, absent from checked-in DDL.
Runtime against a deployed server is not verified.
