# Code review checklist

Use this checklist as an evidence guide, not as a requirement to report an
issue in every row. First read the applicable repository rules and contracts.

## Repository-rule compliance

- Identify the requirement or contract that applies to the reviewed behavior.
- Check the correct scope's AGENTS instructions, architecture boundaries, and
  conventions; distinguish mandatory rules from examples or preferences.
- Trace changed behavior through the current caller, callee, side effects,
  response, and relevant tests where applicable.
- Keep expected behavior and current source behavior distinct. Record a
  discrepancy when an approved requirement and current implementation differ.
- Do not invent APIs, fields, validation, permissions, or behavior to fill a
  documentation gap.

## Reuse

- Search the relevant scope for existing helpers, components, adapters, or
  patterns that actually match the responsibility.
- Report duplication only when it creates meaningful drift, inconsistent
  behavior, or repeated maintenance burden.
- Consider existing shared code before suggesting a new abstraction; do not
  force a common abstraction across different app or server boundaries.
- Do not treat a repeated line, similar name, or hypothetical future reuse as a
  defect by itself.

## Mã sạch và dễ bảo trì

- Check that responsibilities remain in the layers and files established by
  the scope's architecture.
- Follow important branches and error paths for unclear state transitions,
  unsafe fallback behavior, swallowed failures, or response mismatches.
- Check edge cases only where the input contract or current caller makes them
  reachable and consequential.
- Flag readability or naming problems only when they cause a concrete risk of
  misunderstanding or violate an explicit repository rule.
- Do not elevate harmless style differences, minor optimization ideas, or
  broad refactoring preferences into findings.

## Security

Check only relevant boundaries and data flows, including:

- authentication and authorization, including object/tenant/role checks;
- validation of untrusted input and safe query/command construction;
- output encoding, injection, unsafe deserialization, and path/URL handling;
- secrets, sensitive data exposure, logging, and error responses;
- file, network, storage, and external-service access where the changed path
  reaches them;
- security configuration or dependency changes when the reviewed change
  affects them.

For each possible issue, demonstrate the attacker-controlled input or reachable
scenario, the missing/incorrect control, and the resulting impact from code
evidence. Do not claim an item is safe merely because no obvious issue was
found in a narrow review.

## Finding gate

Report a finding only when all apply:

1. The affected code path is reachable in the requested target.
2. Evidence supports the behavior and its impact.
3. It is a meaningful rule, correctness, security, reuse, or maintainability
   problem and is actionable.
4. For a diff review, the reviewed diff introduced it.

If one condition is unknown, mark that review area `Chưa đủ bằng chứng` or omit
the speculative finding and state the relevant limit.
