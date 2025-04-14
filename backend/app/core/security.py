from passlib.context import CryptContext

from app.core.config import settings


class Security:
    """Security for password hashing and verification."""

    def __init__(self, algorithm: str, rounds: int):
        """Initialize the security."""
        crypt_context_config = {
            "schemes": [algorithm],
            "deprecated": "auto",
        }
        algorithm = str(algorithm).lower()
        if algorithm in ["bcrypt", "argon2", "pbkdf2_sha256"]:
            crypt_context_config[f"{algorithm}__rounds"] = rounds

        self.crypt_context = CryptContext(**crypt_context_config)

    def verify(self, secret: str, hashed: str) -> bool:
        """Verify a secret against a hashed value."""
        return self.crypt_context.verify(secret, hashed)

    def hash(self, secret: str) -> str:
        """Hash a secret value."""
        return self.crypt_context.hash(secret)


security = Security(
    algorithm=settings.PASSWORD_CRYPT_ALGORITHM, rounds=settings.PASSWORD_HASHING_ROUNDS
)
