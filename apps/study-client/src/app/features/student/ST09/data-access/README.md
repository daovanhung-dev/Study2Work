# ST-09 data access

The page runs under `StudentLayout`, paginates #20 with `status=ACTIVE` until
the route course is found, then calls #37. Route changes cancel the prior
lookup/progress chain. Both API responses are checked against current
source-backed business codes and projections before state is rendered.
Public curriculum #09 is not used as an enrollment or lesson-access check. #37
currently counts completion among PUBLISHED lessons only; AC-18's wider
lesson/quiz/assignment aggregate remains a discrepancy. Deployed runtime is
not verified.
