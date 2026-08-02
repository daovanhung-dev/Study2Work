import bcrypt


class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify(
        password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )


def hash_password(password: str) -> str:
    """Hash a plaintext password with the application's password hasher."""

    return PasswordHasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Return whether a plaintext password matches a stored password hash."""

    return PasswordHasher.verify(password, hashed_password)
