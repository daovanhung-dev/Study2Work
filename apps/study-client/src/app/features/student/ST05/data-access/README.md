# ST-05 data access

ST-05 reuses `GS03CourseDetailService` for public API #08 course revalidation.
It does not send API #16: the descriptor is `UNWIRED`, Student auth is absent,
the checked-in database has no `orders` table, and the current server route has
no focused behavioral tests.
