# ST-03 data access

Route metadata records API #04, #13 and #14 from the screen inventory. No HTTP caller is enabled:

- The Study Web client has no Student session/token provider for the Student Bearer APIs.
- API #13 accepts a JSON Data URL and writes an object before profile persistence.
- API #14 omits `bio`; phone/avatar rules and the upload/update failure policy remain unresolved.
- The inventory requires a follow-up #04 read, while current #14 already returns the updated profile.

Keep upload and save controls disabled until those contracts are approved. Do not treat route metadata as an API request.
