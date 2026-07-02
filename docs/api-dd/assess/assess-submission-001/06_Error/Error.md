# Error - ASSESS-SUBMISSION-001

## Error Catalog

| ID | HTTP | Error code | Business code | Condition | Safe message | Retry | Log level | Test ID |
|---|---:|---|---|---|---|---|---|---|
| `ASSESS-SUBMISSION-001-ERR-001` | 422 | `E422` | `ASSESS-SUBMISSION-001-INVALID_INPUT` | Request payload, path, query hoặc cross-field rule không hợp lệ. | Dữ liệu yêu cầu không hợp lệ. | No | WARN | `ASSESS-SUBMISSION-001-TC-002` |
| `ASSESS-SUBMISSION-001-ERR-002` | 401 | `E401` | `AUTH-RESP-UNAUTHORIZED` | Missing, expired hoặc invalid token/service credential. | Cần xác thực trước khi thực hiện hành động này. | Refresh/re-login | WARN | `ASSESS-SUBMISSION-001-TC-003` |
| `ASSESS-SUBMISSION-001-ERR-003` | 403 | `E403` | `ASSESS-SUBMISSION-001-FORBIDDEN` | Permission hoặc ownership/scope bị từ chối. | Bạn không có quyền thực hiện hành động này. | No | WARN | `ASSESS-SUBMISSION-001-TC-004` |
| `ASSESS-SUBMISSION-001-ERR-004` | 404 | `E404` | `ASSESS-SUBMISSION-001-NOT_FOUND` | Resource không tồn tại hoặc không visible với actor. | Không tìm thấy tài nguyên. | No | INFO | `ASSESS-SUBMISSION-001-TC-005` |
| `ASSESS-SUBMISSION-001-ERR-005` | 409 | `E409` | `ASSESS-SUBMISSION-001-CONFLICT` | Duplicate, replay, invalid state transition hoặc concurrent update. | Yêu cầu đang xung đột với trạng thái hiện tại. | Maybe | WARN | `ASSESS-SUBMISSION-001-TC-006` |
| `ASSESS-SUBMISSION-001-ERR-006` | 502/503/504 | `E503` | `ASSESS-SUBMISSION-001-DEPENDENCY_UNAVAILABLE` | Provider/cache/worker/database dependency không sẵn sàng. | Hệ thống phụ trợ đang không sẵn sàng. | Safe retry only | ERROR | `ASSESS-SUBMISSION-001-TC-007` |
| `ASSESS-SUBMISSION-001-ERR-007` | 500 | `E500` | `SYSTEM-RESP-INTERNAL_ERROR` | Unexpected server failure. | Lỗi hệ thống nội bộ. | Maybe | ERROR | `ASSESS-SUBMISSION-001-TC-007` |

## Error Envelope

```json
{
  "businessCode": "ASSESS-SUBMISSION-001-INVALID_INPUT",
  "message": "Dữ liệu yêu cầu không hợp lệ.",
  "timestamp": "2026-07-02T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "errors": [
    {
      "field": "request",
      "code": "E422",
      "message": "Kiểm tra lại dữ liệu đầu vào."
    }
  ]
}
```

## Logging Rules

- Không log password, raw access token, refresh token, OAuth secret, hidden test, private PII, prompt nhạy cảm hoặc source code có secret.
- Mọi log phải có `traceId`, `moduleCode`, `apiCode`, timestamp và resource identifier nếu có.
- Stack trace chỉ gửi tới observability tooling, không trả về client.
