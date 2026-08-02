# VERIFICATION REPORT — PLAN-01

## Result

- Technical validation: `PASS`.
- Source completeness gate: `FAIL — unresolved approved-source gaps`.
- Overall plan status: `PARTIALLY COMPLETED — NEEDS USER DECISION`.

## Counts

| Metric | Result |
|---|---:|
| API folders | 3 |
| Markdown files | 45 |
| Relative links checked | 371 |
| Anchor references checked | 370 |
| JSON fences parsed | 9 |
| Validation errors introduced | 0 |

## Quality gates

| Gate | Result | Notes |
|---|---|---|
| Coverage | PASS | Skill/template/examples/5 canonical docs/plan read fully; manifest recorded. |
| Template | PASS | 8-file template fingerprinted; core headings/table headers retained; DB mapping duplicated from `07_table.md`. |
| Structure | PASS | Exactly 3 API folders; prefix ordering and required files present. |
| Markdown tables | PASS | Column counts checked programmatically. |
| Code fences | PASS | Every fence closed. |
| JSON | PASS | Every `json` fence parsed. |
| Relative links/anchors | PASS | File existence and explicit anchors checked. |
| One-field/one-column | PASS by authored structure | Request, response, errors and DB columns use separate rows; query columns listed separately. |
| Cross-file consistency | PASS with marked gaps | Method/path/table/step links reconciled; SOURCE_REQUIRED/CONFLICT preserved. |
| Source completeness | FAIL | Agreement table, response schema, authVersion/session_epoch, event/dedupe/ownership proof unresolved. |
| ZIP | PASS | Archive opened successfully; `zipfile.testzip()` and `unzip -t` reported no error. |

## Template fingerprints

| File | SHA-256 |
| --- | --- |
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Output fingerprints

> Fingerprint table excludes `VERIFICATION_REPORT.md` itself to avoid recursive self-hashing.

| File | SHA-256 |
| --- | --- |
| `API-IAM-001_Register/00_Cover.md` | `7a1fe9becb5c8e805c98bba1056bae9daa0048410a05c40b782a53dfd9233a58` |
| `API-IAM-001_Register/01_Lich_su.md` | `3ece96b2eb473c9093aa96b857bd4107235893684d37814dbaf08bf551907abe` |
| `API-IAM-001_Register/02_Overview.md` | `1b16cb4c8794849c3cd2ca5ba24e94f22aaae6f355f3f679293444e486e8dc25` |
| `API-IAM-001_Register/03_Request.md` | `519e981b2a1147cf8f8898d1feb53ca77a7ba348338daa472053531e3d23af3c` |
| `API-IAM-001_Register/04_Response.md` | `9b2339fb15ef7704cb47a07ebb82908784b432ea4ea688f3b237af6426914193` |
| `API-IAM-001_Register/05_Data_Mapping.md` | `874c2c9875ec2c6d4c718cd6acbe91d1755d17b828ac2e5854f86e350eae71c3` |
| `API-IAM-001_Register/06_Error.md` | `ac57bfdfa0c1d64e2842dd321e3eb647ece308d1c3904e207b2fff9e09e01d9e` |
| `API-IAM-001_Register/07_idempotency_keys_insert.md` | `c2902226774fc0d81d1775e38d9dbd925e52f2344e1fb4ea419c69cc0acbc7eb` |
| `API-IAM-001_Register/08_users_insert.md` | `be44a8ce35da20c3059dd600cd03ea3f71549ed22bc36e8df076b75b1688e095` |
| `API-IAM-001_Register/09_user_emails_insert.md` | `ea97a0088f6373d9c54d0c59f480441e48335dc1abdcbcf141d14fc4354fa8c4` |
| `API-IAM-001_Register/10_password_credentials_insert.md` | `3ab0fe3d71f84ed2931709b4b11af824f022ce53d0b10bf30b69b1c4193d7f2c` |
| `API-IAM-001_Register/11_email_verification_tokens_insert.md` | `68eb39c6fd97b13738b63768e2784799ff828a5d3c69f069d1d5131d06273d99` |
| `API-IAM-001_Register/12_security_audit_events_insert.md` | `0a207c949f8a9f4e3868a02df53d3b6b03dfccb95fce0a3a57db6ccb94f2257b` |
| `API-IAM-001_Register/13_outbox_events_insert.md` | `474e1acbc895e7e2c2e807e51b163335778866a3b1ee8e01409e407c39d4a301` |
| `API-IAM-001_Register/14_idempotency_keys_update.md` | `607f2bd8720d057dde90484f8852b316789ed69b8675b69391071cf62abbe027` |
| `API-IAM-002_Verify_Email/00_Cover.md` | `82292cdcc0e192ba151a3a30a7212865c00fa029578de54378e31c5ed63dd31b` |
| `API-IAM-002_Verify_Email/01_Lich_su.md` | `9e5031f976d56d1c3444ac1d864403b9f15e23203ce0a0bed5a64725d5bb22e8` |
| `API-IAM-002_Verify_Email/02_Overview.md` | `479ccd304b06fc43733997d54172d0b4be6a2452c4a4c12256b853914fa95a9d` |
| `API-IAM-002_Verify_Email/03_Request.md` | `a156f7b413d9bb7bd34c5fb2de146d107c24b298e9a48dba0dd2016babb07832` |
| `API-IAM-002_Verify_Email/04_Response.md` | `12fe0084bf30ad54cee3209e3b20c5369aa2249564eeea143a21fb071040d2be` |
| `API-IAM-002_Verify_Email/05_Data_Mapping.md` | `4723d2e07aa24c58a093d74136ee1584db129ddbe6ccd730d50414e6b7ba8829` |
| `API-IAM-002_Verify_Email/06_Error.md` | `ded72ccabeb351fb0e98553d7806c80ffa4fcd9210f63b2942de8c0781083dc4` |
| `API-IAM-002_Verify_Email/07_idempotency_keys_insert.md` | `1d49ca9a8b1ac1eef9337486ef996957e7b425d0ff69102694db9014b9e48e44` |
| `API-IAM-002_Verify_Email/08_email_verification_tokens_update.md` | `b535a665e5b0bec8fdfbcff75dddd368cb1852e0bc832eecfa14adcfe91ba55b` |
| `API-IAM-002_Verify_Email/09_users_update.md` | `6bff1622eb923761b86c66639808508c6423e75bc6b9d69542d23574e0af5ccc` |
| `API-IAM-002_Verify_Email/10_user_emails_update.md` | `1270dbb293d1988d7479848e3e49467bca878a3a838823c2270827257d7e6f24` |
| `API-IAM-002_Verify_Email/11_auth_sessions_insert.md` | `fef0f9d68a3e1275153dea807f0ae014a5fe406f11f1160886eef96962d141d1` |
| `API-IAM-002_Verify_Email/12_refresh_tokens_insert.md` | `40b907a0f5e8125e951e8b98fd5ec7008f24ffc5f212204dd49b46e4853711a8` |
| `API-IAM-002_Verify_Email/13_outbox_events_insert.md` | `26db60e98e1c0800156dfbe526e083d27f964de9520884ac7d7804ab60b2a401` |
| `API-IAM-002_Verify_Email/14_idempotency_keys_update.md` | `072db1bab84e7df8b86a929c0dfd2e754458bbf5f97e22c9cd17eed0a4de0010` |
| `API-IAM-003_Resend_Verification/00_Cover.md` | `56c09ad24957864289ae0ebf1665d5b3f5b314eba2ef6ba9f564f73e577a66c4` |
| `API-IAM-003_Resend_Verification/01_Lich_su.md` | `d37933a5a48d5f9870088c58625819e5a24c63b4f0c068005264f56c1ca97967` |
| `API-IAM-003_Resend_Verification/02_Overview.md` | `7aad40303dc7cfadfdcfa4fb5bb42149a07e0c1405d93f3d79ae07f902ca61bb` |
| `API-IAM-003_Resend_Verification/03_Request.md` | `79e9f421f737e43d9e36f144d2a97c30dddf5b6274fc857a1f4ad53d8ec61739` |
| `API-IAM-003_Resend_Verification/04_Response.md` | `770957444eb466c5b308a620eb322999e767448613685c9fbf16198188023f0f` |
| `API-IAM-003_Resend_Verification/05_Data_Mapping.md` | `0f5e53734359b069893331bc7883b2eb2c784cf8724cdcaa3023ea4944e140d1` |
| `API-IAM-003_Resend_Verification/06_Error.md` | `535369d0fb256ef023f8ada5b139c5667fa35b7eaa2caf572968885abd0301be` |
| `API-IAM-003_Resend_Verification/07_email_verification_tokens_update.md` | `b94a14c3e3d57ef2b2a919d06f3eb5320cfb1f6e53a419f4c6775161ead7c3b0` |
| `API-IAM-003_Resend_Verification/08_email_verification_tokens_insert.md` | `17d3bca71ad30b0d4636727deb7e9897df21d59b57c86761ac955f5e6a735ee2` |
| `API-IAM-003_Resend_Verification/09_outbox_events_insert.md` | `2b508f0db78bdd395fcfdd4b43f3c4a8daab8f5c1c48aaeb6d005a461581ade2` |
| `API_REQUIREMENT_MATRIX.md` | `497292a8b3d124047446b2fd26bc71837d85c219c2de0c7351d30186a98b4637` |
| `OPEN_QUESTIONS.md` | `9e5c2dfcc4ca953a1f3256c8ab9d822ba92c67319ad34403c438b514bd1950a1` |
| `PLAN_RESULT.md` | `804870cec1810e9adda5759fe6d8d333e9be431f59e4230d16caeec14992c73a` |
| `SOURCE_READ_REPORT.md` | `c3b3c0ae2c6accba10c35a411eab5f7a08e58f020d8dc096f26ece77dd34291f` |

## Source defects preserved

- API table aliases differ from DB canonical names.
- Agreement acceptance exists in API/class/sequence but not DB schema.
- Endpoint-specific codes lack full HTTP/message mapping.
- Verify event naming is versioned inconsistently.
- Anonymous resend ownership proof is absent.
- `authVersion`/`session_epoch` source is absent.

## Introduced defects

- None detected by automated validation.

## ZIP validation

- ZIP validation: `PASS` — archive opens successfully and all entries pass CRC validation.
- Entry count: `46` files.
- `ZIP_VALIDATION.txt` is included in the package.
