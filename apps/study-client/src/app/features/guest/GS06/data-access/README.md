# GS06 data access

No resource service is wired in this implementation slice. API #11 currently
returns a singleton built from only the first database row, while the screen
needs a collection contract. API #12 returns a direct URL without a resource
access policy. Keep both calls out of the UI until those contracts are resolved.
