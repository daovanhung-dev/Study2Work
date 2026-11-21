# GS06 data access

`GS06ResourcesService` calls Study API #11 for the published course ID. The
approved response is `Resource[]`, sorted by resource ID, with an empty array
representing a valid course with no public resources. API #11 lists only
`PUBLIC` resources; opening a selected item goes through API #12 so resource
access is checked by the backend.
