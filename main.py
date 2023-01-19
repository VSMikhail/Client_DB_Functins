import psycopg2


def delete_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_number;
        """)

        cur.execute("""
        DROP TABLE client;
        """)

        conn.commit()


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            last_name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(client_id) ON DELETE CASCADE,
            phone_number VARCHAR(30)
        );
        """)

        conn.commit()


def add_phone_number(conn, client_id: int, phone_number: str):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_number(client_id, phone_number)
        VALUES(%s, %s);
        """, (client_id, phone_number))
        conn.commit()


def add_client(conn, name: str, last_name: str, email: str, phones: list = None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, last_name, email)
        VALUES(%s, %s, %s)
        RETURNING client_id;
        """, (name, last_name, email))
        returning_client_id = cur.fetchall()
    if phones:
        for phone in phones:
            add_phone_number(conn, returning_client_id[0][0], phone)


def delete_all_phone_numbers_by_id(conn, client_id: int):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s;
        """, (client_id,))
        conn.commit()


def update_client_info(conn, client_id: int, name: str = None, last_name: str = None, email: str = None, phones: list = None):
    with conn.cursor() as cur:
        if name:
            cur.execute("""
            UPDATE client
            SET name = %s
            WHERE client_id = %s;
            """, (name, client_id))
            conn.commit()
        if last_name:
            cur.execute("""
            UPDATE client
            SET last_name = %s
            WHERE client_id = %s;
            """, (last_name, client_id))
            conn.commit()
        if email:
            cur.execute("""
            UPDATE client
            SET email = %s
            WHERE client_id = %s;
            """, (email, client_id))
            conn.commit()
        if phones:
            delete_all_phone_numbers_by_id(conn, client_id)
            for phone in phones:
                add_phone_number(conn, client_id, phone)


def delete_phone_number(conn, client_id: int, phone_number: str):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s AND phone_number = %s;
        """, (client_id, phone_number))
        conn.commit()


def delete_client(conn, client_id: int):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client
        WHERE client_id = %s;
        """, (client_id,))
        conn.commit()


with psycopg2.connect(dbname='client_db', user='postgres', password='n41xc76') as conn:

    delete_tables(conn)
    create_tables(conn)
    add_client(conn, 'Vasya', 'Ginsburg', '123455@mail.kz', ['+15','+1563'])
    add_client(conn, 'Ulya', 'Ginsburg', '123@mail.kz', ['+15','+1563'])
    add_client(conn, 'Phil', 'Ginsburg', '455@mail.kz', ['+15','+1563'])
    add_client(conn, 'Sam', 'Ginsburg', '456@mail.kz', ['+15','+1563'])
    add_client(conn, 'Ivan', 'Ginsburg', '789@mail.kz', ['+15','+156300'])
    add_phone_number(conn, 1, '+7-904-997-77-00')
    add_phone_number(conn, 2, '+7-904-997-77-01')
    add_phone_number(conn, 3, '+7-904-997-77-02')
    add_phone_number(conn, 5, '+7-904-997-77-03')
    update_client_info(conn, 3, None, 'Fisieva', "oleg5429@mail.by", ['new3','new4'])
    delete_phone_number(conn, 3, 'n')
    delete_client(conn, 2)
    # search_client(conn, 'Vasya', None)