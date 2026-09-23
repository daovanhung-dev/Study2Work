# AI workflow

```text
classify task -> worklog preflight/read same-type logs
->
scope AGENTS
-> chat/API or copied-core page
-> exact runtime import path from app/main.py
-> Ollama external effects
-> dependency impact if wiring copied core
-> focused tests (currently must be added with implementation if required)
-> update affected context
-> context validator
```

Any decision to activate copied DB/security/response infrastructure is an architecture + dependency change, not a documentation-only cleanup.

Mọi task phải dùng `.agents/worklog/TEMPLATE.md`; ghi rõ `UNWIRED` nếu logic
chưa reachable từ `app/main.py` và chạy context validator sau khi cập nhật page.
