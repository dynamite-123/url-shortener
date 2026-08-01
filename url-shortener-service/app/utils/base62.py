ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode_base62(number: int) -> str:
    if number < 0:
        raise ValueError("Number must be non-negative")

    if number == 0:
        return ALPHABET[0]

    encoded = []

    while number > 0:
        number, remainder = divmod(number, BASE)
        encoded.append(ALPHABET[remainder])

    return "".join(reversed(encoded))


def decode_base62(code: str) -> int:
    if not code:
        raise ValueError("Code cannot be empty")

    decoded = 0

    for char in code:
        try:
            value = ALPHABET.index(char)
        except ValueError:
            raise ValueError(f"Invalid Base62 character: {char}")

        decoded = decoded * BASE + value

    return decoded