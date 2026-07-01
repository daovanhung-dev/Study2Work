# Huong Dan Su Dung Kien Truc Backend Study2Work

Tai lieu nay giai thich cach dung kien truc backend moi cua Study2Work cho developer va AI agent. Backend canonical nam tai `services/api` va chi phuc vu pham vi Study.

## 1. Nguyen Tac Tong Quan

Backend duoc thiet ke theo modular monolith ket hop Clean Architecture, Ports and Adapters va DDD bounded context.

Quy tac phu thuoc:

```text
presentation -> application -> domain
infrastructure -> application/domain ports
domain -> khong phu thuoc framework
```

Y nghia:

- `presentation` nhan request FastAPI, validate schema, goi use case va tra response.
- `application` dieu phoi use case, transaction, permission, repository port va event.
- `domain` giu invariant, state transition va business rule.
- `infrastructure` chua SQLAlchemy, Redis, Celery, adapter external service va repository implementation.

## 2. Cong Nghe Backend

| Nhom | Cong nghe | Vai tro |
|---|---|---|
| API | FastAPI | REST API va OpenAPI |
| DTO/schema | Pydantic v2 | Validate request/response |
| Database | PostgreSQL | Luu source of truth |
| ORM | SQLAlchemy 2.0 async | Model va query database |
| Migration | Alembic | Quan ly thay doi schema |
| Cache/queue | Redis | Cache, rate-limit, broker |
| Worker | Celery | AI, grading, notification, analytics |
| Tooling | uv, Ruff, mypy, pytest | Dependency, lint, type check, test |

## 3. Cau Truc Thu Muc

```text
services/api/
├── app/
│   ├── core/
│   ├── modules/
│   ├── shared/
│   ├── workers/
│   └── main.py
├── alembic/
├── tests/
└── pyproject.toml
```

Moi module nghiep vu co 4 layer:

```text
module/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

## 4. Cach Them API Moi

1. Kiem tra API trong `docs/checklists/API.md`.
2. Tao hoac doc API DD tai `docs/api-dd/<module>/<api-code>/`.
3. Chi code API chinh thuc khi API DD co status `APPROVED`.
4. Tao schema va route trong `presentation`.
5. Tao command/query va handler trong `application`.
6. Dat state transition va invariant trong `domain`.
7. Tao repository/model/adapter trong `infrastructure`.
8. Viet test unit, API/integration va negative test cho permission/state.
9. Cap nhat checklist va worklog.

## 5. Response Envelope

Moi API phai tra envelope chuan:

```json
{
  "businessCode": "SYSTEM-HEALTH-SUCCESS",
  "message": "Service is healthy.",
  "timestamp": "2026-07-01T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "data": {}
}
```

Loi phai tra `errors` va khong duoc lo stack trace, SQL, token, password, hidden test case hoac secret.

## 6. Quy Tac Quan Trong

- Khong dat business logic trong FastAPI route.
- Moi protected API phai kiem tra auth, RBAC, ownership/scope va state transition.
- Moi mutation API phai co transaction va audit/event neu BD/DD yeu cau.
- AI, auto grading, notification va analytics phai chay async qua worker.
- Code cua hoc vien khong bao gio chay trong main API process.
- Khong build employer, recruitment, job, CV, interview, shortlist, offer hoac matching trong Study scope.

## 7. Lenh Kiem Tra

Chay trong `services/api`:

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

Neu mot command khong chay duoc vi thieu moi truong, ghi ro trong worklog va khong danh dau `VERIFIED`.

