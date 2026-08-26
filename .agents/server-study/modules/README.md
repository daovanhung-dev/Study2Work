# Study business modules

```text
MODULE_DIRECTORY_STATUS: NOT_FOUND
PATH: apps/study-server/app/module/
```

`app/api/v1.py` still declares imports from:

- `app.module.auth.model`
- `app.module.auth.view`
- `app.module.ai.log.view`

but those packages do not exist at the tracked source snapshot.

Therefore current context intentionally contains **no invented auth/user/chat-log module design**. Historical `apps/study-server/docs/codebase/README.md` or removed `.agent/context` may explain old intent but cannot be used as current contract when they disagree with source.

When a future task restores/creates a module, first require one of: latest user requirement, canonical DD/contract, approved plan, or newly added source. Then add module-specific context after implementation.
