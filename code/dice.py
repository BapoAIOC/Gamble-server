import secrets

LOWEST_RANGE = 1
HIGHEST_RANGE = 7


def roll():
    """
    Function that gets a number from 1 through 6 (inclusive)
    """
    return secrets.choice(range(LOWEST_RANGE, HIGHEST_RANGE))

def roll_n(n: int, player_count: int):
    """
    Function that returns 
    [
        [ n elements here ],
        player_count arrays
    ]

    For example:

    roll_n(2, 3)

    Could return
    [
        [1, 2],
        [2, 3],
        [3, 4]
    ]
    """
    res = []
    for i in range(player_count):
        res.append([roll() for each in range(n)])
    return res