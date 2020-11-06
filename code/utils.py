import os
import typing
import psycopg2

postgres_user = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_db = os.environ["POSTGRES_DB"]
postgres_url = os.environ["POSTGRES_URL"]
postgres_port = os.environ["POSTGRES_PORT"]
server_num = int(os.environ["SERVER_NUM"])

connection = None


def establish_connection():
    global connection
    connection = psycopg2.connect(user=postgres_user,
                                  password=postgres_password,
                                  host=postgres_url,
                                  port=postgres_port,
                                  database=postgres_db)


async def get_invalid_input_return(key: str, value: str):
    return {
        "error": f"Invalid input for key {key}, had value {value}"
    }, 400


def execute_query(query: str, *args):
    if connection is None:
        establish_connection()

    with connection.cursor() as cursor:
        cursor.execute(query, args)
    connection.commit()


def log_game(game_num: int, amount: float, players: typing.List[typing.Tuple[int, bool]]):
    if connection is None:
        establish_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM start_game(%s, %s)", (game_num, amount))
        res = cursor.fetchone()
        game_id = res[0]
        for p, win in players:
            cursor.execute("CALL add_player_game(%s, %s, %s)",
                           (game_id, p, win,))
    connection.commit()

    return {}, 200


def log_endpoint_access(endpoint: str, ip: str, user_agent: str):
    if connection is None:
        establish_connection()

    execute_query("CALL insert_endpoint_visit(%s, %s, %s, %s);",
                  user_agent, ip, endpoint, server_num, )
