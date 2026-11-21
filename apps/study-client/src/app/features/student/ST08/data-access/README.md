# ST-08 data access

The page runs under `StudentLayout` and calls #20 with the requested page. The
response is checked against the current 20-row `CourseSummaryPage` projection,
including the requested page, pagination metadata, enrollment fields and
enrolled-time ordering. #21 currently returns `UserProfile` and is not used as
course progress. Deployed runtime remains unverified.
