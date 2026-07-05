# Platform Identity

This folder is a local identity scaffold for the rebuilt monorepo.

Future options:

- External identity provider with JWKS.
- Self-hosted identity service.
- Local development mock issuer.

Study and Work APIs should validate:

- issuer
- audience
- signature through JWKS
- expiration
- subject as immutable `platformUserId`

This pass only stores a development JWKS placeholder and does not implement authentication flows.
