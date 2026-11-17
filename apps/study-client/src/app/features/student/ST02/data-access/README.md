# ST-02 data access

The screen is assigned to API #04 (`GET /api/v1/users/me`) in route metadata.
It does not issue a request: the Angular client has no Student session/token
provider, and the approved screen package has no authenticated profile-ready
layout or error-state mapping. Keep the API call gated until those contracts are
resolved.
