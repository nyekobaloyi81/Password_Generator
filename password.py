import secrets
from typing import Iterable


CHARACTER_SETS = {
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "numbers": "0123456789",
    "symbols": "!@#$%^&*()-_=+[]{};:,.?/|~",
}


def generate_password(
    length: int,
    categories: Iterable[str] = ("lowercase", "uppercase", "numbers", "symbols"),
) -> str:
    """Generate a cryptographically secure password containing every selected category."""
    selected = tuple(category for category in categories if category in CHARACTER_SETS)
    if not selected:
        raise ValueError("Select at least one character category.")
    if length < len(selected):
        raise ValueError("Password length must accommodate every selected character category.")

    characters = "".join(CHARACTER_SETS[category] for category in selected)
    password = [secrets.choice(CHARACTER_SETS[category]) for category in selected]
    password.extend(secrets.choice(characters) for _ in range(length - len(selected)))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def estimate_entropy(length: int, categories: Iterable[str]) -> float:
    """Estimate entropy using the assumption that each character is sampled uniformly."""
    selected = tuple(category for category in categories if category in CHARACTER_SETS)
    if length <= 0 or not selected:
        return 0.0

    pool_size = sum(len(CHARACTER_SETS[category]) for category in selected)
    import math

    return length * math.log2(pool_size)
