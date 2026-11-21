# ST-06 data access

API #17 and #18 are assigned in route metadata. No request is sent: #17 is
fail-closed while the provider is unavailable, and #18's current source is a
notification-only lookup rather than a payment-operation status endpoint.
