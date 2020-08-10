import os
import psycopg2


class call_database(object):
    """docstring for call_database."""

    def __init__(self, arg):
        super(call_database, self).__init__()
        self.arg = arg

    def web_select_overall():
        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        postgres_select_query = f"""SELECT * FROM user_account
        ORDER BY last_login;"""

        cursor.execute(postgres_select_query)

        message = []
        while True:
            temp = cursor.fetchmany(10)

            if temp:
                message.extend(temp)
            else:
                break

        cursor.close()
        conn.close()

        return message
