from __future__ import annotations

import hashlib
import hmac
import os


class PasswordService:
    ALGORITHM = "pbkdf2_sha256"
    ITERATIONS = 600_000

    def hash_password(self, password: str) -> str:
        password = password.strip()
        if not password:
            raise ValueError("La contraseña no puede estar vacía.")

        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self.ITERATIONS,
        )
        return f"{self.ALGORITHM}${self.ITERATIONS}${salt.hex()}${digest.hex()}"

    def verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            algorithm, iterations_str, salt_hex, digest_hex = stored_hash.split("$", 3)
            if algorithm != self.ALGORITHM:
                return False

            iterations = int(iterations_str)
            salt = bytes.fromhex(salt_hex)
            expected_digest = bytes.fromhex(digest_hex)

            candidate_digest = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations,
            )
            return hmac.compare_digest(candidate_digest, expected_digest)
        except Exception:
            return False