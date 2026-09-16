"""DB Admin control-plane accounts, bindings and local authentication."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import jwt
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.core.contracts import (
    USERNAME_PATTERN,
    ChangeSchemaRequest,
    CreateAccessAccountRequest,
    UpdateAccessAccountRequest,
)
from app.core.passwords import hash_password, verify_password
from app.core.responses import ApiError
from app.core.security import Principal
from app.services.audit import AuditStore
from app.services.identifiers import quote_identifier, validate_identifier

LOCK_THRESHOLD = 5
LOCK_MINUTES = 15
_ROLE_NAME_PATTERN = USERNAME_PATTERN


def _password_literal(password: str) -> str:
    """Build a PostgreSQL literal for utility statements that reject binds."""

    if "\x00" in password:
        raise ValueError("Password contains an invalid character")
    escaped = password.replace("\\", "\\\\").replace("'", "\\'")
    return "E'" + escaped + "'"


@dataclass(frozen=True)
class AccountRecord:
    user_id: str
    username: str
    display_name: str
    password_hash: str
    is_root: bool
    status: str
    must_change_password: bool
    failed_login_attempts: int
    locked_until: datetime | None
    last_login_at: datetime | None
    password_changed_at: datetime | None
    target: str


class AccessService:
    """Repository for the isolated ``db_admin`` schema on each target."""

    def __init__(
        self,
        engines: dict[str, Engine],
        settings: Settings,
        audit: AuditStore,
    ) -> None:
        self.engines = engines
        self.settings = settings
        self.audit = audit
        trace_id = "access-startup"
        self._control = quote_identifier(settings.control_schema, "control_schema", trace_id)

    def _engine(self, database: str, trace_id: str) -> Engine:
        engine = self.engines.get(database)
        if engine is None:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_DATABASE_NOT_FOUND",
                message="The selected database is not configured.",
                trace_id=trace_id,
            )
        return engine

    def _control_error(self, trace_id: str) -> ApiError:
        return ApiError(
            status_code=503,
            business_code="DB_ADMIN_CONTROL_PLANE_UNAVAILABLE",
            message="The DB Admin control plane is not ready on the selected database.",
            trace_id=trace_id,
        )

    def _account_query(self, by_id: bool = False) -> str:
        condition = "user_id = :user_id" if by_id else "LOWER(username) = LOWER(:username)"
        return f"""
            SELECT user_id, username, display_name, password_hash, is_root, status,
                   must_change_password, failed_login_attempts, locked_until,
                   last_login_at, password_changed_at
            FROM {self._control}.admin_users
            WHERE {condition}
        """

    def _accounts_by_username(self, username: str, trace_id: str) -> list[AccountRecord]:
        return self._accounts(username=username, trace_id=trace_id)

    def _accounts_by_id(self, user_id: str, trace_id: str) -> list[AccountRecord]:
        return self._accounts(user_id=user_id, trace_id=trace_id)

    def _accounts(
        self,
        *,
        trace_id: str,
        username: str | None = None,
        user_id: str | None = None,
    ) -> list[AccountRecord]:
        if (username is None) == (user_id is None):
            raise ValueError("Exactly one account lookup key is required")
        params = {"username": username} if username is not None else {"user_id": user_id}
        statement = text(self._account_query(by_id=user_id is not None))
        records: list[AccountRecord] = []
        for target, engine in self.engines.items():
            try:
                with engine.connect() as connection:
                    row = connection.execute(statement, params).mappings().first()
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
            if row is None:
                continue
            records.append(
                AccountRecord(
                    user_id=str(row["user_id"]),
                    username=str(row["username"]),
                    display_name=str(row["display_name"]),
                    password_hash=str(row["password_hash"]),
                    is_root=bool(row["is_root"]),
                    status=str(row["status"]),
                    must_change_password=bool(row["must_change_password"]),
                    failed_login_attempts=int(row["failed_login_attempts"]),
                    locked_until=row["locked_until"],
                    last_login_at=row["last_login_at"],
                    password_changed_at=row["password_changed_at"],
                    target=target,
                )
            )
        return records

    def _metadata_is_consistent(self, records: list[AccountRecord]) -> bool:
        if not records:
            return True
        first = records[0]
        return all(
            (
                item.user_id,
                item.username,
                item.display_name,
                item.password_hash,
                item.is_root,
            )
            == (
                first.user_id,
                first.username,
                first.display_name,
                first.password_hash,
                first.is_root,
            )
            for item in records[1:]
        )

    def _generic_login_error(self, trace_id: str) -> ApiError:
        return ApiError(
            status_code=401,
            business_code="DB_ADMIN_INVALID_CREDENTIALS",
            message="Username or password is incorrect.",
            trace_id=trace_id,
        )

    def _now(self) -> datetime:
        return datetime.now(UTC)

    def _is_locked(self, value: datetime | None) -> bool:
        if value is None:
            return False
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value > self._now()

    def _record_auth_failure(self, record: AccountRecord, trace_id: str) -> None:
        attempts = record.failed_login_attempts + 1
        locked_until = (
            self._now() + timedelta(minutes=LOCK_MINUTES) if attempts >= LOCK_THRESHOLD else None
        )
        try:
            with self._engine(record.target, trace_id).begin() as connection:
                connection.execute(
                    text(f"""
                        UPDATE {self._control}.admin_users
                        SET failed_login_attempts = :attempts,
                            locked_until = :locked_until,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = :user_id
                    """),
                    {"attempts": attempts, "locked_until": locked_until, "user_id": record.user_id},
                )
        except SQLAlchemyError as exc:
            raise self._control_error(trace_id) from exc

    def _record_auth_success(self, records: list[AccountRecord], trace_id: str) -> None:
        for record in records:
            try:
                with self._engine(record.target, trace_id).begin() as connection:
                    connection.execute(
                        text(f"""
                            UPDATE {self._control}.admin_users
                            SET failed_login_attempts = 0,
                                locked_until = NULL,
                                last_login_at = CURRENT_TIMESTAMP,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE user_id = :user_id
                        """),
                        {"user_id": record.user_id},
                    )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc

    def _roles_and_bindings(
        self, records: list[AccountRecord], trace_id: str
    ) -> tuple[set[str], list[dict[str, str]]]:
        roles: set[str] = set()
        bindings: dict[tuple[str, str], dict[str, str]] = {}
        role_sql = text(f"""
            SELECT r.role_key, p.permission_key
            FROM {self._control}.admin_user_roles AS ur
            JOIN {self._control}.admin_roles AS r ON r.role_id = ur.role_id
            JOIN {self._control}.admin_role_permissions AS rp ON rp.role_id = r.role_id
            JOIN {self._control}.admin_permissions AS p ON p.permission_id = rp.permission_id
            WHERE ur.user_id = :user_id
        """)
        binding_sql = text(f"""
            SELECT database_target, schema_name, postgres_role_name, access_level
            FROM {self._control}.admin_user_schema_bindings
            WHERE user_id = :user_id AND is_active = TRUE
        """)
        permissions: set[str] = set()
        for record in records:
            try:
                with self._engine(record.target, trace_id).connect() as connection:
                    for row in connection.execute(role_sql, {"user_id": record.user_id}).mappings():
                        roles.add(str(row["role_key"]))
                        permissions.add(str(row["permission_key"]))
                    for row in connection.execute(
                        binding_sql, {"user_id": record.user_id}
                    ).mappings():
                        key = (str(row["database_target"]), str(row["schema_name"]))
                        bindings[key] = {
                            "database": key[0],
                            "schema": key[1],
                            "postgresRole": str(row["postgres_role_name"]),
                            "accessLevel": str(row["access_level"]),
                        }
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        return permissions | (
            {"db_admin:manage"} if any(r.is_root for r in records) else set()
        ), list(bindings.values())

    def _token(
        self,
        record: AccountRecord,
        permissions: set[str],
        roles: set[str],
        bindings: list[dict[str, str]],
    ) -> str:
        secret = self.settings.local_jwt_secret
        if not self.settings.local_auth_enabled or secret is None:
            raise ApiError(
                status_code=503,
                business_code="DB_ADMIN_LOCAL_AUTH_DISABLED",
                message="Local DB Admin password authentication is not enabled.",
                trace_id="auth-config",
            )
        targets = (
            sorted(self.engines)
            if record.is_root
            else sorted({item["database"] for item in bindings})
        )
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": record.user_id,
            "userId": record.user_id,
            "username": record.username,
            "isRoot": record.is_root,
            "mustChangePassword": record.must_change_password,
            "permissions": sorted(permissions),
            "roles": sorted(roles),
            "targets": targets,
            "schemaBindings": bindings,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self.settings.local_jwt_ttl_minutes)).timestamp()),
            "jti": secrets.token_urlsafe(18),
            "iss": self.settings.jwt_issuer,
            "aud": self.settings.jwt_audience,
        }
        return jwt.encode(payload, secret.get_secret_value(), algorithm="HS256")

    def _session_data(
        self,
        record: AccountRecord,
        permissions: set[str],
        roles: set[str],
        bindings: list[dict[str, str]],
        trace_id: str,
    ) -> dict[str, Any]:
        return {
            "accessToken": self._token(record, permissions, roles, bindings),
            "user": {
                "id": record.user_id,
                "username": record.username,
                "displayName": record.display_name,
                "isRoot": record.is_root,
                "status": record.status,
            },
            "permissions": sorted(permissions),
            "roles": sorted(roles),
            "targets": sorted(self.engines)
            if record.is_root
            else sorted({item["database"] for item in bindings}),
            "schemaBindings": bindings,
            "mustChangePassword": record.must_change_password,
            "traceId": trace_id,
        }

    def login(self, username: str, password: str, trace_id: str) -> dict[str, Any]:
        if not self.settings.local_auth_enabled:
            raise ApiError(
                status_code=503,
                business_code="DB_ADMIN_LOCAL_AUTH_DISABLED",
                message="Local DB Admin password authentication is not enabled.",
                trace_id=trace_id,
            )
        records = self._accounts_by_username(username, trace_id)
        if not records or not self._metadata_is_consistent(records):
            self.audit.record(
                actor="anonymous",
                action="auth.login",
                target="local",
                outcome="failed",
                trace_id=trace_id,
            )
            raise self._generic_login_error(trace_id)
        record = records[0]
        if record.status != "active" or any(self._is_locked(item.locked_until) for item in records):
            self.audit.record(
                actor="anonymous",
                action="auth.login",
                target="local",
                outcome="failed",
                trace_id=trace_id,
            )
            raise self._generic_login_error(trace_id)
        if not verify_password(record.password_hash, password):
            self._record_auth_failure(record, trace_id)
            self.audit.record(
                actor="anonymous",
                action="auth.login",
                target="local",
                outcome="failed",
                trace_id=trace_id,
            )
            raise self._generic_login_error(trace_id)
        self._record_auth_success(records, trace_id)
        permissions, bindings = self._roles_and_bindings(records, trace_id)
        roles = {"root"} if record.is_root else {"developer"}
        data = self._session_data(record, permissions, roles, bindings, trace_id)
        self.audit.record(
            actor=record.user_id,
            actor_user_id=record.user_id,
            actor_username=record.username,
            action="auth.login",
            target="local",
            outcome="success",
            trace_id=trace_id,
        )
        return data

    def me(self, principal: Principal, trace_id: str) -> dict[str, Any]:
        if principal.user_id is None:
            return {
                "user": {
                    "id": principal.subject,
                    "username": principal.username,
                    "isRoot": principal.is_root,
                },
                "permissions": sorted(principal.permissions),
                "roles": sorted(principal.roles),
                "targets": sorted(principal.targets),
                "schemaBindings": list(principal.schema_bindings),
                "mustChangePassword": principal.must_change_password,
                "traceId": trace_id,
            }
        records = self._accounts_by_id(principal.user_id, trace_id)
        if not records:
            raise self._generic_login_error(trace_id)
        permissions, bindings = self._roles_and_bindings(records, trace_id)
        roles = {"root"} if records[0].is_root else {"developer"}
        return self._session_data(records[0], permissions, roles, bindings, trace_id)

    def is_active(self, principal: Principal, trace_id: str) -> bool:
        """Check revocation state for a local token before it reaches a route."""

        if principal.user_id is None:
            return True
        records = self._accounts_by_id(principal.user_id, trace_id)
        return bool(records) and all(record.status == "active" for record in records)

    def change_password(
        self, principal: Principal, current: str, new: str, trace_id: str
    ) -> dict[str, Any]:
        if principal.user_id is None:
            raise ApiError(
                status_code=401,
                business_code="DB_ADMIN_LOCAL_AUTH_REQUIRED",
                message="Local account authentication is required.",
                trace_id=trace_id,
            )
        records = self._accounts_by_id(principal.user_id, trace_id)
        if (
            not records
            or not self._metadata_is_consistent(records)
            or not verify_password(records[0].password_hash, current)
        ):
            raise ApiError(
                status_code=401,
                business_code="DB_ADMIN_INVALID_CREDENTIALS",
                message="Current password is incorrect.",
                trace_id=trace_id,
            )
        if verify_password(records[0].password_hash, new):
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_PASSWORD_REUSED",
                message="Choose a new password.",
                trace_id=trace_id,
            )
        password_hash = hash_password(new)
        binding_sql = text(
            f"SELECT postgres_role_name FROM {self._control}.admin_user_schema_bindings "
            "WHERE user_id = :user_id AND is_active = TRUE"
        )
        for record in records:
            try:
                with self._engine(record.target, trace_id).begin() as connection:
                    connection.execute(
                        text(f"""
                        UPDATE {self._control}.admin_users
                        SET password_hash = :password_hash, password_algorithm = 'argon2id',
                            must_change_password = FALSE, failed_login_attempts = 0,
                            locked_until = NULL, password_changed_at = CURRENT_TIMESTAMP,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = :user_id
                    """),
                        {"password_hash": password_hash, "user_id": record.user_id},
                    )
                    for row in connection.execute(
                        binding_sql, {"user_id": record.user_id}
                    ).mappings():
                        role_sql = self._role_sql_name(str(row["postgres_role_name"]), trace_id)
                        connection.execute(
                            text(f"ALTER ROLE {role_sql} PASSWORD {_password_literal(new)}")
                        )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        updated = AccountRecord(
            **{**records[0].__dict__, "password_hash": password_hash, "must_change_password": False}
        )
        permissions, bindings = self._roles_and_bindings(records, trace_id)
        roles = {"root"} if updated.is_root else {"developer"}
        self.audit.record(
            actor=updated.user_id,
            actor_user_id=updated.user_id,
            actor_username=updated.username,
            action="auth.change_password",
            target="local",
            outcome="success",
            trace_id=trace_id,
        )
        return self._session_data(updated, permissions, roles, bindings, trace_id)

    def allowed_targets(self, principal: Principal) -> set[str]:
        return (
            set(self.engines) if principal.is_root else set(principal.targets) & set(self.engines)
        )

    def allowed_schema_names(self, principal: Principal, database: str) -> set[str] | None:
        if principal.is_root:
            return None
        return {
            str(item["schema"])
            for item in principal.schema_bindings
            if item.get("database") == database
        }

    def current_schema_names(
        self, principal: Principal, database: str, trace_id: str
    ) -> set[str] | None:
        """Read live bindings so reassigning a schema revokes old tokens."""

        allowed = self.allowed_schema_names(principal, database)
        if principal.is_root or principal.user_id is None:
            return allowed
        engine = self.require_target(principal, database, trace_id)
        try:
            with engine.connect() as connection:
                rows = connection.execute(
                    text(
                        f"SELECT schema_name FROM {self._control}.admin_user_schema_bindings "
                        "WHERE user_id = :user_id AND database_target = :database "
                        "AND is_active = TRUE"
                    ),
                    {"user_id": principal.user_id, "database": database},
                ).scalars()
                return {str(schema) for schema in rows}
        except SQLAlchemyError as exc:
            raise self._control_error(trace_id) from exc

    def require_target(self, principal: Principal, database: str, trace_id: str) -> Engine:
        engine = self._engine(database, trace_id)
        if not principal.is_root and database not in self.allowed_targets(principal):
            raise ApiError(
                status_code=403,
                business_code="DB_ADMIN_TARGET_FORBIDDEN",
                message="The account is not assigned to this database.",
                trace_id=trace_id,
            )
        return engine

    def require_schema(
        self, principal: Principal, database: str, schema: str, trace_id: str
    ) -> Engine:
        engine = self.require_target(principal, database, trace_id)
        if principal.is_root:
            return engine
        assigned = any(
            item.get("database") == database and item.get("schema") == schema
            for item in principal.schema_bindings
        )
        if principal.user_id is not None:
            try:
                with engine.connect() as connection:
                    assigned = (
                        connection.execute(
                            text(
                                f"SELECT 1 FROM {self._control}.admin_user_schema_bindings "
                                "WHERE user_id = :user_id AND database_target = :database "
                                "AND schema_name = :schema AND is_active = TRUE"
                            ),
                            {
                                "user_id": principal.user_id,
                                "database": database,
                                "schema": schema,
                            },
                        ).scalar_one_or_none()
                        is not None
                    )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        if not assigned:
            raise ApiError(
                status_code=403,
                business_code="DB_ADMIN_SCHEMA_FORBIDDEN",
                message="The account is not assigned to this schema.",
                trace_id=trace_id,
            )
        return engine

    def _public_account(
        self, row: dict[str, Any], bindings: list[dict[str, Any]]
    ) -> dict[str, Any]:
        def iso(value: Any) -> str | None:
            if value is None or isinstance(value, str):
                return value
            return value.isoformat() if hasattr(value, "isoformat") else str(value)

        return {
            "id": str(row["user_id"]),
            "username": row["username"],
            "displayName": row["display_name"],
            "status": row["status"],
            "isRoot": bool(row["is_root"]),
            "mustChangePassword": bool(row["must_change_password"]),
            "failedLoginAttempts": int(row["failed_login_attempts"]),
            "lockedUntil": iso(row["locked_until"]),
            "lastLoginAt": iso(row["last_login_at"]),
            "createdAt": iso(row["created_at"]),
            "bindings": bindings,
        }

    def list_accounts(self, database: str | None, trace_id: str) -> list[dict[str, Any]]:
        targets = [database] if database else list(self.engines)
        merged: dict[str, dict[str, Any]] = {}
        account_sql = text(f"""
            SELECT user_id, username, display_name, is_root, status, must_change_password,
                   failed_login_attempts, locked_until, last_login_at, created_at
            FROM {self._control}.admin_users
            ORDER BY username
        """)
        binding_sql = text(f"""
            SELECT database_target, schema_name, postgres_role_name, access_level, is_active
            FROM {self._control}.admin_user_schema_bindings
            WHERE user_id = :user_id AND is_active = TRUE
            ORDER BY database_target, schema_name
        """)
        for target in targets:
            self._engine(target, trace_id)
            try:
                with self._engine(target, trace_id).connect() as connection:
                    rows = list(connection.execute(account_sql).mappings())
                    for row in rows:
                        bindings = [
                            dict(item)
                            for item in connection.execute(
                                binding_sql, {"user_id": row["user_id"]}
                            ).mappings()
                        ]
                        item = self._public_account(dict(row), bindings)
                        if item["id"] not in merged:
                            merged[item["id"]] = item
                        else:
                            merged[item["id"]]["bindings"] = (
                                list(merged[item["id"]]["bindings"]) + bindings
                            )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        for item in merged.values():
            unique: dict[tuple[str, str], dict[str, Any]] = {}
            for binding in item["bindings"]:
                unique[(str(binding["database_target"]), str(binding["schema_name"]))] = {
                    "database": binding["database_target"],
                    "schema": binding["schema_name"],
                    "postgresRole": binding["postgres_role_name"],
                    "accessLevel": binding["access_level"],
                    "active": bool(binding["is_active"]),
                }
            item["bindings"] = list(unique.values())
        return sorted(merged.values(), key=lambda item: str(item["username"]))

    def _role_sql_name(self, username: str, trace_id: str) -> str:
        if not _ROLE_NAME_PATTERN.fullmatch(username) or len(username) > 63:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_IDENTIFIER",
                message="The username cannot be used as a PostgreSQL role.",
                trace_id=trace_id,
            )
        return '"' + username.replace('"', '""') + '"'

    def _allow_schema_ownership(self, connection: Any, role_sql: str) -> None:
        """Enable SET ROLE for the creating session during schema ownership DDL."""

        connection.execute(text(f"GRANT {role_sql} TO CURRENT_USER WITH SET TRUE"))

    def _validate_schema(self, schema: str, trace_id: str) -> str:
        validate_identifier(schema, "schema_name", trace_id)
        if (
            schema == self.settings.control_schema
            or schema.startswith("pg_")
            or schema == "information_schema"
        ):
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_SCHEMA_RESERVED",
                message="This schema name is reserved.",
                trace_id=trace_id,
            )
        return quote_identifier(schema, "schema_name", trace_id)

    def create_account(self, request: CreateAccessAccountRequest, trace_id: str) -> dict[str, Any]:
        self._engine(request.database, trace_id)
        if len(request.username) > 63:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_IDENTIFIER",
                message="Username is too long for a PostgreSQL role.",
                trace_id=trace_id,
            )
        schema_sql = self._validate_schema(request.schema_name, trace_id)
        role_sql = self._role_sql_name(request.username, trace_id)
        if self._accounts_by_username(request.username, trace_id):
            raise ApiError(
                status_code=409,
                business_code="DB_ADMIN_ACCOUNT_EXISTS",
                message="An account with this username already exists.",
                trace_id=trace_id,
            )
        secret = secrets.token_urlsafe(32)
        user_id = uuid4()
        binding_id = uuid4()
        try:
            with self._engine(request.database, trace_id).begin() as connection:
                if (
                    connection.execute(
                        text("SELECT 1 FROM pg_roles WHERE rolname = :name"),
                        {"name": request.username},
                    ).scalar_one_or_none()
                    is not None
                ):
                    raise ApiError(
                        status_code=409,
                        business_code="DB_ADMIN_POSTGRES_ROLE_EXISTS",
                        message="The PostgreSQL role already exists.",
                        trace_id=trace_id,
                    )
                if (
                    connection.execute(
                        text("SELECT to_regnamespace(:name)"), {"name": request.schema_name}
                    ).scalar_one_or_none()
                    is not None
                ):
                    raise ApiError(
                        status_code=409,
                        business_code="DB_ADMIN_SCHEMA_EXISTS",
                        message="The schema already exists.",
                        trace_id=trace_id,
                    )
                connection.execute(
                    text(
                        f"CREATE ROLE {role_sql} LOGIN NOSUPERUSER NOCREATEDB "
                        f"NOCREATEROLE NOINHERIT PASSWORD {_password_literal(secret)}"
                    )
                )
                self._allow_schema_ownership(connection, role_sql)
                connection.execute(text(f"CREATE SCHEMA {schema_sql} AUTHORIZATION {role_sql}"))
                connection.execute(text(f"ALTER ROLE {role_sql} SET search_path TO {schema_sql}"))
                role_id = connection.execute(
                    text(
                        f"SELECT role_id FROM {self._control}.admin_roles "
                        "WHERE role_key = 'developer'"
                    )
                ).scalar_one()
                connection.execute(
                    text(f"""
                    INSERT INTO {self._control}.admin_users
                        (user_id, username, display_name, password_hash,
                         password_algorithm, is_root, status, must_change_password)
                    VALUES (:user_id, :username, :display_name, :password_hash,
                            'argon2id', FALSE, 'active', TRUE)
                """),
                    {
                        "user_id": user_id,
                        "username": request.username,
                        "display_name": request.display_name,
                        "password_hash": hash_password(secret),
                    },
                )
                connection.execute(
                    text(
                        f"INSERT INTO {self._control}.admin_user_roles "
                        "(user_id, role_id) VALUES (:user_id, :role_id)"
                    ),
                    {"user_id": user_id, "role_id": role_id},
                )
                connection.execute(
                    text(f"""
                    INSERT INTO {self._control}.admin_user_schema_bindings
                        (binding_id, user_id, database_target, schema_name,
                         postgres_role_name, access_level)
                    VALUES (:binding_id, :user_id, :database_target, :schema_name,
                            :role_name, 'owner')
                """),
                    {
                        "binding_id": binding_id,
                        "user_id": user_id,
                        "database_target": request.database,
                        "schema_name": request.schema_name,
                        "role_name": request.username,
                    },
                )
        except ApiError:
            raise
        except SQLAlchemyError as exc:
            raise ApiError(
                status_code=400,
                business_code="DB_ADMIN_ACCESS_OPERATION_FAILED",
                message="Unable to create the account and its schema.",
                trace_id=trace_id,
            ) from exc
        account = {
            "id": str(user_id),
            "username": request.username,
            "displayName": request.display_name,
            "status": "active",
            "isRoot": False,
            "mustChangePassword": True,
            "bindings": [
                {
                    "database": request.database,
                    "schema": request.schema_name,
                    "postgresRole": request.username,
                    "accessLevel": "owner",
                    "active": True,
                }
            ],
        }
        account["secret"] = secret
        return account

    def update_account(
        self, user_id: str, request: UpdateAccessAccountRequest, principal: Principal, trace_id: str
    ) -> dict[str, Any]:
        try:
            UUID(user_id)
        except ValueError as exc:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_ACCOUNT_ID",
                message="The account identifier is invalid.",
                trace_id=trace_id,
            ) from exc
        records = self._accounts_by_id(user_id, trace_id)
        if not records:
            raise ApiError(
                status_code=404,
                business_code="DB_ADMIN_ACCOUNT_NOT_FOUND",
                message="The account was not found.",
                trace_id=trace_id,
            )
        if records[0].is_root and request.status == "disabled":
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_ROOT_CANNOT_DISABLE",
                message="The root account cannot be disabled.",
                trace_id=trace_id,
            )
        for record in records:
            try:
                with self._engine(record.target, trace_id).begin() as connection:
                    connection.execute(
                        text(f"""
                        UPDATE {self._control}.admin_users
                        SET display_name = COALESCE(:display_name, display_name),
                            status = COALESCE(:status, status), updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = :user_id
                    """),
                        {
                            "display_name": request.display_name,
                            "status": request.status,
                            "user_id": user_id,
                        },
                    )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        self.audit.record(
            actor=principal.subject,
            actor_user_id=principal.user_id,
            actor_username=principal.username,
            action="access.account.update",
            target=user_id,
            database_target=records[0].target,
            outcome="success",
            trace_id=trace_id,
            details={"status": request.status},
        )
        return self.list_accounts(None, trace_id)[
            next(
                i
                for i, item in enumerate(self.list_accounts(None, trace_id))
                if item["id"] == user_id
            )
        ]

    def rotate_password(self, user_id: str, principal: Principal, trace_id: str) -> dict[str, Any]:
        records = self._accounts_by_id(user_id, trace_id)
        if not records:
            raise ApiError(
                status_code=404,
                business_code="DB_ADMIN_ACCOUNT_NOT_FOUND",
                message="The account was not found.",
                trace_id=trace_id,
            )
        secret = secrets.token_urlsafe(32)
        password_hash = hash_password(secret)
        binding_sql = text(
            f"SELECT postgres_role_name FROM {self._control}.admin_user_schema_bindings "
            "WHERE user_id = :user_id AND is_active = TRUE"
        )
        for record in records:
            try:
                with self._engine(record.target, trace_id).begin() as connection:
                    connection.execute(
                        text(f"""
                        UPDATE {self._control}.admin_users
                        SET password_hash = :password_hash, password_algorithm = 'argon2id',
                            must_change_password = TRUE, password_changed_at = NULL,
                            failed_login_attempts = 0, locked_until = NULL,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = :user_id
                    """),
                        {"password_hash": password_hash, "user_id": user_id},
                    )
                    for row in connection.execute(binding_sql, {"user_id": user_id}).mappings():
                        role_sql = self._role_sql_name(str(row["postgres_role_name"]), trace_id)
                        connection.execute(
                            text(f"ALTER ROLE {role_sql} PASSWORD {_password_literal(secret)}")
                        )
            except SQLAlchemyError as exc:
                raise self._control_error(trace_id) from exc
        self.audit.record(
            actor=principal.subject,
            actor_user_id=principal.user_id,
            actor_username=principal.username,
            action="access.account.rotate_password",
            target=user_id,
            database_target=records[0].target,
            outcome="success",
            trace_id=trace_id,
        )
        account = next(item for item in self.list_accounts(None, trace_id) if item["id"] == user_id)
        account["secret"] = secret
        return account

    def change_schema(
        self, user_id: str, request: ChangeSchemaRequest, principal: Principal, trace_id: str
    ) -> dict[str, Any]:
        records = [
            item
            for item in self._accounts_by_id(user_id, trace_id)
            if item.target == request.database
        ]
        if not records:
            raise ApiError(
                status_code=404,
                business_code="DB_ADMIN_ACCOUNT_BINDING_NOT_FOUND",
                message="The account is not assigned to this database.",
                trace_id=trace_id,
            )
        record = records[0]
        if record.is_root:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_ROOT_SCHEMA_UNSUPPORTED",
                message="The root account does not use a developer schema.",
                trace_id=trace_id,
            )
        new_schema_sql = self._validate_schema(request.schema_name, trace_id)
        binding_sql = text(
            f"SELECT binding_id, schema_name, postgres_role_name "
            f"FROM {self._control}.admin_user_schema_bindings "
            "WHERE user_id = :user_id AND database_target = :database_target "
            "AND is_active = TRUE FOR UPDATE"
        )
        same_schema = False
        try:
            with self._engine(request.database, trace_id).begin() as connection:
                binding = (
                    connection.execute(
                        binding_sql, {"user_id": user_id, "database_target": request.database}
                    )
                    .mappings()
                    .first()
                )
                if binding is None:
                    raise ApiError(
                        status_code=404,
                        business_code="DB_ADMIN_ACCOUNT_BINDING_NOT_FOUND",
                        message="The account is not assigned to this database.",
                        trace_id=trace_id,
                    )
                if binding["schema_name"] == request.schema_name:
                    same_schema = True
                elif (
                    connection.execute(
                        text(
                            f"SELECT 1 FROM {self._control}.admin_user_schema_bindings "
                            "WHERE database_target = :database_target "
                            "AND schema_name = :schema_name AND is_active = TRUE"
                        ),
                        {"database_target": request.database, "schema_name": request.schema_name},
                    ).scalar_one_or_none()
                    is not None
                ):
                    raise ApiError(
                        status_code=409,
                        business_code="DB_ADMIN_SCHEMA_ALREADY_ASSIGNED",
                        message="The schema is already assigned to another account.",
                        trace_id=trace_id,
                    )
                else:
                    role_sql = self._role_sql_name(str(binding["postgres_role_name"]), trace_id)
                    if (
                        connection.execute(
                            text("SELECT to_regnamespace(:name)"), {"name": request.schema_name}
                        ).scalar_one_or_none()
                        is None
                    ):
                        self._allow_schema_ownership(connection, role_sql)
                        connection.execute(
                            text(f"CREATE SCHEMA {new_schema_sql} AUTHORIZATION {role_sql}")
                        )
                    else:
                        self._allow_schema_ownership(connection, role_sql)
                        connection.execute(
                            text(f"ALTER SCHEMA {new_schema_sql} OWNER TO {role_sql}")
                        )
                    connection.execute(
                        text(f"ALTER ROLE {role_sql} SET search_path TO {new_schema_sql}")
                    )
                    connection.execute(
                        text(
                            f"UPDATE {self._control}.admin_user_schema_bindings "
                            "SET schema_name = :schema_name, updated_at = CURRENT_TIMESTAMP "
                            "WHERE binding_id = :binding_id"
                        ),
                        {"schema_name": request.schema_name, "binding_id": binding["binding_id"]},
                    )
        except ApiError:
            raise
        except SQLAlchemyError as exc:
            raise ApiError(
                status_code=400,
                business_code="DB_ADMIN_ACCESS_OPERATION_FAILED",
                message="Unable to change the account schema.",
                trace_id=trace_id,
            ) from exc
        if same_schema:
            return next(
                item
                for item in self.list_accounts(request.database, trace_id)
                if item["id"] == user_id
            )
        self.audit.record(
            actor=principal.subject,
            actor_user_id=principal.user_id,
            actor_username=principal.username,
            action="access.account.change_schema",
            target=f"{request.database}:{request.schema_name}",
            database_target=request.database,
            outcome="success",
            trace_id=trace_id,
            details={"userId": user_id},
        )
        return next(
            item for item in self.list_accounts(request.database, trace_id) if item["id"] == user_id
        )

    def list_audit(
        self, database: str | None, actor: str | None, action: str | None, limit: int, trace_id: str
    ) -> list[dict[str, Any]]:
        return self.audit.list_persistent(
            database=database, actor=actor, action=action, limit=limit, trace_id=trace_id
        )
