import secrets

def random_number_between(lower: int, upper: int):
    # inclusive of upper
    return secrets.choice(range(lower, upper))