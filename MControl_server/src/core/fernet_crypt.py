import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
default_iterations = 100_000


def _derive_key(
    passwd: bytes, salt: bytes, iterations: int = default_iterations
) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend,
    )
    return b64e(kdf.derive(passwd))


def password_encrypt(
    msg: bytes, secret_key: str, iterations: int = default_iterations
) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(secret_key.encode(), salt, iterations)
    return b64e(
        b"%b%b%b"
        % (
            salt,
            iterations.to_bytes(4, "big"),
            b64d(Fernet(key).encrypt(msg)),
        )
    )


def password_decrypt(token: bytes, secret_key: str) -> bytes:
    decoded = b64d(token)
    salt, _iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(_iter, "big")
    key = _derive_key(secret_key.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


# example of usage
if __name__ == "__main__":
    encoding = "utf-8"
    # store generated password in secure location
    message, password = "John Doe", "password"
    encrypted = password_encrypt(message.encode(encoding), password)
    print("Encrypted:", encrypted.decode(encoding))
    print("with password:", password)
    print("Decrypted:", password_decrypt(encrypted, password).decode(encoding))
