import secrets

HEADS = False
TAILS = True


async def coinflip():
    """
    Function that returns either
    Heads -> 0
    Tails -> 1
    """
    return secrets.choice([HEADS, TAILS])
