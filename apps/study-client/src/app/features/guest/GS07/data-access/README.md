# GS-07 data access

This screen intentionally has no API service in this implementation slice.
API #12 currently returns a direct resource URL without a verified access
policy or storage signer, while AC-06 and the Draft API design leave those
decisions unresolved. Do not call API #12 or expose/open/download its URL until
the access and URL contract is approved and implemented.
