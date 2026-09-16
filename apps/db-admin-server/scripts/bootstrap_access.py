#!/usr/bin/env python3
"""Bootstrap the DB Admin control plane on both configured PostgreSQL targets.

This is an operator command, deliberately separate from business migrations.
It never accepts a password as a command-line argument and never prints a
generated secret. ``--dry-run`` only performs metadata checks.
"""

from __future__ import annotations

import argparse
import getpass
import json
import secrets
import sys
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from sqlalchemy import Connection, Engine, text
from sqlalchemy.exc import SQLAlchemyError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import Settings, get_settings  # noqa: E402
from app.core.database import build_engine  # noqa: E402
from app.core.passwords import hash_password, verify_password  # noqa: E402
from app.services.identifiers import quote_identifier  # noqa: E402

CONTROL_SCHEMA = "db_admin"


@dataclass(frozen=True)
class TargetSpec:
    username: str
    schema: str
    user_id: UUID


TARGETS: dict[str, TargetSpec] = {
    "study_server": TargetSpec(
        username="study_dev",
        schema="study_dev",
        user_id=UUID("10000000-0000-0000-0000-000000000002"),
    ),
    "work_server": TargetSpec(
        username="work_dev",
        schema="work_dev",
        user_id=UUID("10000000-0000-0000-0000-000000000003"),
    ),
}
ROOT_ID = UUID("10000000-0000-0000-0000-000000000001")
ROOT_ROLE_ID = UUID("00000000-0000-0000-0000-000000000001")
DEVELOPER_ROLE_ID = UUID("00000000-0000-0000-0000-000000000002")


def _bootstrap_sql() -> list[str]:
    sql_path = ROOT / "sql" / "db_admin" / "001_bootstrap.sql"
    return [
        statement.strip()
        for statement in sql_path.read_text(encoding="utf-8").split(";")
        if statement.strip()
    ]


def _engine_for(settings: Settings, target: str) -> Engine:
    url = settings.target_urls().get(target)
    if url is None:
        raise RuntimeError(f"Target is not configured: {target}")
    return build_engine(settings.model_copy(update={"database_url": url, "database_targets": {}}))


def _role_name(value: str, trace_id: str) -> str:
    return quote_identifier(value, "postgres_role_name", trace_id)


def _password_literal(password: str) -> str:
    if "\x00" in password:
        raise ValueError("Password contains an invalid character")
    escaped = password.replace("\\", "\\\\").replace("'", "\\'")
    return "E'" + escaped + "'"


def _safe_database_error(error: SQLAlchemyError) -> str:
    """Return only the driver diagnostic, never SQL text or bound values."""

    original = getattr(error, "orig", None)
    diagnostic = getattr(original, "diag", None)
    message = getattr(diagnostic, "message_primary", None)
    if isinstance(message, str) and message.strip():
        return " ".join(message.split())[:240]
    return "The database rejected the bootstrap statement."


def _allow_schema_ownership(connection: Connection, role: str) -> None:
    """Allow the creating role to SET ROLE while assigning schema ownership.

    PostgreSQL 16+ automatically grants a newly-created role back to its
    creator with SET FALSE. CREATE SCHEMA ... AUTHORIZATION requires SET ROLE,
    so enable only that membership option for this bootstrap session. The
    developer role itself remains NOINHERIT/NOCREATEROLE.
    """

    connection.execute(text(f"GRANT {role} TO CURRENT_USER WITH SET TRUE"))


def _validate_password(password: str, label: str) -> None:
    if len(password) < 12:
        raise ValueError(f"{label} must contain at least 12 characters.")
    if len(password) > 256:
        raise ValueError(f"{label} must contain at most 256 characters.")
    if "\x00" in password:
        raise ValueError(f"{label} contains an invalid character.")


def _update_developer_password(
    connection: Connection,
    target: str,
    developer_password: str,
    password_hash: str,
) -> None:
    spec = TARGETS[target]
    control = quote_identifier(CONTROL_SCHEMA, "control_schema", "bootstrap")
    role = _role_name(spec.username, "bootstrap")

    control_exists = connection.execute(
        text("SELECT to_regclass(:name)"), {"name": f"{CONTROL_SCHEMA}.admin_users"}
    ).scalar_one_or_none()
    if control_exists is None:
        raise RuntimeError(f"control plane is not ready on {target}")

    account = connection.execute(
        text(
            f"SELECT user_id, is_root, status FROM {control}.admin_users "
            "WHERE LOWER(username) = LOWER(:username)"
        ),
        {"username": spec.username},
    ).mappings().one_or_none()
    if account is None:
        raise RuntimeError(f"developer account {spec.username} is missing on {target}")
    if str(account["user_id"]) != str(spec.user_id) or bool(account["is_root"]):
        raise RuntimeError(f"developer account metadata conflict on {target}")
    if str(account["status"]) != "active":
        raise RuntimeError(f"developer account {spec.username} is disabled on {target}")

    role_state = connection.execute(
        text(
            """
            SELECT r.rolcanlogin, r.rolsuper, r.rolcreatedb, r.rolcreaterole,
                   r.rolinherit,
                   EXISTS (
                       SELECT 1 FROM pg_namespace n
                       WHERE n.nspname = :schema_name AND n.nspowner = r.oid
                   ) AS owns_schema
            FROM pg_roles r
            WHERE r.rolname = :role_name
            """
        ),
        {"schema_name": spec.schema, "role_name": spec.username},
    ).mappings().one_or_none()
    if role_state is None:
        raise RuntimeError(f"PostgreSQL role {spec.username} is missing on {target}")
    if not bool(role_state["rolcanlogin"]) or bool(role_state["rolsuper"]):
        raise RuntimeError(f"PostgreSQL role {spec.username} has invalid login flags on {target}")
    if bool(role_state["rolcreatedb"]) or bool(role_state["rolcreaterole"]):
        raise RuntimeError(f"PostgreSQL role {spec.username} has excessive privileges on {target}")
    if bool(role_state["rolinherit"]) or not bool(role_state["owns_schema"]):
        raise RuntimeError(f"PostgreSQL role/schema ownership is invalid on {target}")

    binding_exists = connection.execute(
        text(
            f"""
            SELECT 1 FROM {control}.admin_user_schema_bindings
            WHERE user_id = :user_id AND database_target = :database_target
              AND schema_name = :schema_name AND postgres_role_name = :role_name
              AND is_active = TRUE
            """
        ),
        {
            "user_id": spec.user_id,
            "database_target": target,
            "schema_name": spec.schema,
            "role_name": spec.username,
        },
    ).scalar_one_or_none()
    if binding_exists is None:
        raise RuntimeError(f"developer schema binding is missing on {target}")

    updated = connection.execute(
        text(
            f"""
            UPDATE {control}.admin_users
            SET password_hash = :password_hash,
                password_algorithm = 'argon2id',
                must_change_password = TRUE,
                failed_login_attempts = 0,
                locked_until = NULL,
                password_changed_at = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = :user_id
            """
        ),
        {"password_hash": password_hash, "user_id": spec.user_id},
    )
    if updated.rowcount != 1:
        raise RuntimeError(f"developer account update was not applied on {target}")
    connection.execute(text(f"ALTER ROLE {role} PASSWORD {_password_literal(developer_password)}"))


def _set_developer_password(settings: Settings, developer_password: str) -> int:
    _validate_password(developer_password, "Developer password")
    password_hash = hash_password(developer_password)
    for target in ("study_server", "work_server"):
        engine = _engine_for(settings, target)
        try:
            with engine.begin() as connection:
                _update_developer_password(connection, target, developer_password, password_hash)
            print(f"{target}: developer password updated")
        except (SQLAlchemyError, RuntimeError, ValueError) as exc:
            reason = _safe_database_error(exc) if isinstance(exc, SQLAlchemyError) else str(exc)
            print(
                f"{target}: developer password update failed ({type(exc).__name__}): {reason}; "
                "remaining targets were not changed",
                file=sys.stderr,
            )
            return 1
        finally:
            engine.dispose()
    return 0


def _prompt_confirmed_password() -> str | None:
    password = getpass.getpass("Temporary developer password: ")
    confirmation = getpass.getpass("Confirm developer password: ")
    if password != confirmation:
        print("Developer password confirmation does not match.", file=sys.stderr)
        return None
    try:
        _validate_password(password, "Developer password")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return None
    return password


def _dry_run(settings: Settings) -> int:
    for target in TARGETS:
        engine = _engine_for(settings, target)
        try:
            with engine.connect() as connection:
                database = connection.execute(text("SELECT current_database()")).scalar_one()
                current_user = connection.execute(text("SELECT current_user")).scalar_one()
                control_exists = connection.execute(
                    text("SELECT to_regnamespace(:name)"), {"name": CONTROL_SCHEMA}
                ).scalar_one_or_none()
                can_create_role = connection.execute(
                    text("SELECT rolcreaterole FROM pg_roles WHERE rolname = current_user")
                ).scalar_one_or_none()
                roles = (
                    connection.execute(
                        text("SELECT rolname FROM pg_roles WHERE rolname IN (:dev, 'admin')"),
                        {"dev": TARGETS[target].username},
                    )
                    .scalars()
                    .all()
                )
                schema_exists = connection.execute(
                    text("SELECT to_regnamespace(:name)"), {"name": TARGETS[target].schema}
                ).scalar_one_or_none()
                print(
                    f"{target}: database={database} user={current_user} "
                    f"control_schema={'ready' if control_exists else 'missing'} "
                    f"createrole={bool(can_create_role)} "
                    f"dev_role={'present' if TARGETS[target].username in roles else 'missing'} "
                    f"dev_schema={'present' if schema_exists else 'missing'}"
                )
        except SQLAlchemyError as exc:
            print(
                f"{target}: check failed ({type(exc).__name__}): "
                f"{_safe_database_error(exc)}",
                file=sys.stderr,
            )
            return 1
        finally:
            engine.dispose()
    return 0


def _account_id(connection: Connection, username: str) -> UUID | None:
    value = connection.execute(
        text(
            f"SELECT user_id FROM "
            f"{quote_identifier(CONTROL_SCHEMA, 'control_schema', 'bootstrap')}.admin_users "
            "WHERE LOWER(username) = LOWER(:username)"
        ),
        {"username": username},
    ).scalar_one_or_none()
    return UUID(str(value)) if value is not None else None


def _provision_target(
    settings: Settings,
    target: str,
    root_password: str,
    root_hash: str,
) -> list[dict[str, str]]:
    spec = TARGETS[target]
    engine = _engine_for(settings, target)
    credentials: list[dict[str, str]] = []
    control = quote_identifier(CONTROL_SCHEMA, "control_schema", "bootstrap")
    role = _role_name(spec.username, "bootstrap")
    schema = quote_identifier(spec.schema, "schema_name", "bootstrap")
    try:
        with engine.begin() as connection:
            for statement in _bootstrap_sql():
                connection.exec_driver_sql(statement)

            root_exists = _account_id(connection, "admin")
            if root_exists is None:
                connection.execute(
                    text(f"""
                    INSERT INTO {control}.admin_users
                        (user_id, username, display_name, password_hash, password_algorithm,
                         is_root, status, must_change_password)
                    VALUES (:user_id, 'admin', 'DB Admin root', :password_hash,
                            'argon2id', TRUE, 'active', TRUE)
                """),
                    {"user_id": ROOT_ID, "password_hash": root_hash},
                )
                connection.execute(
                    text(f"""
                    INSERT INTO {control}.admin_user_roles (user_id, role_id)
                    VALUES (:user_id, :role_id)
                    ON CONFLICT DO NOTHING
                """),
                    {"user_id": ROOT_ID, "role_id": ROOT_ROLE_ID},
                )
            elif root_exists != ROOT_ID:
                raise RuntimeError(f"root account metadata conflict on {target}")
            existing_root_hash = connection.execute(
                text(f"SELECT password_hash FROM {control}.admin_users WHERE user_id = :user_id"),
                {"user_id": ROOT_ID},
            ).scalar_one_or_none()
            if existing_root_hash is not None and not verify_password(
                str(existing_root_hash), root_password
            ):
                raise RuntimeError(f"root password metadata conflict on {target}")
            connection.execute(
                text(f"""
                    INSERT INTO {control}.admin_user_roles (user_id, role_id)
                    VALUES (:user_id, :role_id)
                    ON CONFLICT DO NOTHING
                """),
                {"user_id": ROOT_ID, "role_id": ROOT_ROLE_ID},
            )

            role_exists = connection.execute(
                text("SELECT 1 FROM pg_roles WHERE rolname = :name"), {"name": spec.username}
            ).scalar_one_or_none()
            schema_exists = connection.execute(
                text("SELECT to_regnamespace(:name)"), {"name": spec.schema}
            ).scalar_one_or_none()
            dev_exists = _account_id(connection, spec.username)
            if (role_exists is None) != (schema_exists is None):
                raise RuntimeError(f"partial PostgreSQL dev provision exists on {target}")
            if dev_exists is not None and dev_exists != spec.user_id:
                raise RuntimeError(f"developer account metadata conflict on {target}")
            if role_exists is not None and dev_exists is None:
                raise RuntimeError(f"partial control-plane dev provision exists on {target}")
            if role_exists is None and dev_exists is not None:
                raise RuntimeError(f"partial control-plane dev provision exists on {target}")

            if role_exists is None:
                secret = secrets.token_urlsafe(32)
                password_hash = hash_password(secret)
                connection.execute(
                    text(
                        f"CREATE ROLE {role} LOGIN NOSUPERUSER NOCREATEDB "
                        f"NOCREATEROLE NOINHERIT PASSWORD {_password_literal(secret)}"
                    )
                )
                _allow_schema_ownership(connection, role)
                connection.execute(text(f"CREATE SCHEMA {schema} AUTHORIZATION {role}"))
                connection.execute(text(f"ALTER ROLE {role} SET search_path TO {schema}"))
                connection.execute(
                    text(f"""
                    INSERT INTO {control}.admin_users
                        (user_id, username, display_name, password_hash, password_algorithm,
                         is_root, status, must_change_password)
                    VALUES (:user_id, :username, :display_name, :password_hash,
                            'argon2id', FALSE, 'active', TRUE)
                """),
                    {
                        "user_id": spec.user_id,
                        "username": spec.username,
                        "display_name": spec.username,
                        "password_hash": password_hash,
                    },
                )
                connection.execute(
                    text(f"""
                    INSERT INTO {control}.admin_user_roles (user_id, role_id)
                    VALUES (:user_id, :role_id)
                    ON CONFLICT DO NOTHING
                """),
                    {"user_id": spec.user_id, "role_id": DEVELOPER_ROLE_ID},
                )
                connection.execute(
                    text(f"""
                    INSERT INTO {control}.admin_user_schema_bindings
                        (binding_id, user_id, database_target, schema_name,
                         postgres_role_name, access_level)
                    VALUES (:binding_id, :user_id, :database_target, :schema_name,
                            :role_name, 'owner')
                    ON CONFLICT (user_id, database_target, schema_name) DO NOTHING
                """),
                    {
                        "binding_id": UUID(int=spec.user_id.int + 100),
                        "user_id": spec.user_id,
                        "database_target": target,
                        "schema_name": spec.schema,
                        "role_name": spec.username,
                    },
                )
                credentials.append(
                    {
                        "database": target,
                        "username": spec.username,
                        "schema": spec.schema,
                        "secret": secret,
                    }
                )
            else:
                connection.execute(text(f"ALTER ROLE {role} SET search_path TO {schema}"))
                connection.execute(
                    text(f"""
                        INSERT INTO {control}.admin_user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON CONFLICT DO NOTHING
                    """),
                    {"user_id": spec.user_id, "role_id": DEVELOPER_ROLE_ID},
                )
                connection.execute(
                    text(f"""
                        INSERT INTO {control}.admin_user_schema_bindings
                            (binding_id, user_id, database_target, schema_name,
                             postgres_role_name, access_level)
                        VALUES (:binding_id, :user_id, :database_target, :schema_name,
                                :role_name, 'owner')
                        ON CONFLICT (user_id, database_target, schema_name) DO NOTHING
                    """),
                    {
                        "binding_id": UUID(int=spec.user_id.int + 100),
                        "user_id": spec.user_id,
                        "database_target": target,
                        "schema_name": spec.schema,
                        "role_name": spec.username,
                    },
                )
    finally:
        engine.dispose()
    return credentials


def _write_credentials(path: Path, credentials: list[dict[str, str]]) -> None:
    if not credentials:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"credentials": credentials}, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def _apply(settings: Settings, root_password: str, output: Path) -> int:
    try:
        _validate_password(root_password, "Root password")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    generated: list[dict[str, str]] = []
    root_hash = hash_password(root_password)
    for target in ("study_server", "work_server"):
        try:
            generated.extend(_provision_target(settings, target, root_password, root_hash))
            print(f"{target}: bootstrap applied")
        except (SQLAlchemyError, RuntimeError, ValueError) as exc:
            reason = _safe_database_error(exc) if isinstance(exc, SQLAlchemyError) else str(exc)
            print(
                f"{target}: bootstrap failed ({type(exc).__name__}): {reason}; "
                "remaining targets were not changed",
                file=sys.stderr,
            )
            return 1
    _write_credentials(output, generated)
    if generated:
        print(f"Generated developer credentials were written once to {output} with mode 0600.")
    else:
        print("No new developer secret was generated; existing secrets were not changed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--dry-run", action="store_true", help="Check target readiness without mutation"
    )
    mode.add_argument("--apply", action="store_true", help="Apply the control-plane bootstrap")
    mode.add_argument(
        "--set-developer-password",
        action="store_true",
        help="Set the same temporary password for study_dev and work_dev",
    )
    parser.add_argument(
        "--root-password-stdin",
        action="store_true",
        help="Read the temporary root password from stdin",
    )
    parser.add_argument(
        "--credentials-output", type=Path, default=ROOT / ".local" / "bootstrap-credentials.json"
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.dry_run:
        return _dry_run(settings)
    if args.set_developer_password:
        developer_password = _prompt_confirmed_password()
        if developer_password is None:
            return 2
        return _set_developer_password(settings, developer_password)
    root_password = (
        sys.stdin.readline().rstrip("\n")
        if args.root_password_stdin
        else getpass.getpass("Temporary DB Admin root password: ")
    )
    return _apply(settings, root_password, args.credentials_output)


if __name__ == "__main__":
    raise SystemExit(main())
