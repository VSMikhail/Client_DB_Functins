import psycopg2

with psycopg2.connect(dbname='client_db', user='postgres', password='n41xc76') as conn:
    with conn.cursor() as cur:
        def delete_tables():
            cur.execute("""
            DROP TABLE phone_number;
            """)

            cur.execute("""
            DROP TABLE client;
            """)

            conn.commit()

        def create_tables():
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
                client_id INTEGER REFERENCES client(client_id),
                phone_number VARCHAR(30)
            );
            """)

            conn.commit()

        def add_client(name: str, last_name: str, email: str):
            cur.execute("""
            INSERT INTO client(name, last_name, email)
            VALUES(%s, %s, %s)
            """, (name, last_name, email))
            conn.commit()

        def add_phone_number(client_id: int, phone_number: str):
            cur.execute("""
            INSERT INTO phone_number(client_id, phone_number)
            VALUES(%s, %s)
            """, (client_id, phone_number))
            conn.commit()

        def update_client_info(client_id: int, name: str, last_name: str, email: str):
            cur.execute("""
            UPDATE client
            SET name = %s,
            last_name = %s,
            email = %s
            WHERE client_id = %s
            """, (name, last_name, email, client_id))
            conn.commit()

        def delete_phone_numbers(client_id: int):
            cur.execute("""
            DELETE FROM phone_number
            WHERE client_id = %s
            """, (client_id,))
            conn.commit()

        def delete_client(client_id: int):
            delete_phone_numbers(client_id)
            cur.execute("""
            DELETE FROM client
            WHERE client_id = %s
            """, (client_id,))
            conn.commit()

        def select_by_input_data():
            choise = int(input("""Input number 1-4:
             1-search by name
             2-search by last name
             3-search by email
             4-search by phone number: """))
            if 0 < choise < 5:
                searched_data = input('Input search request: ')
                if choise == 1:
                    cur.execute("""
                    SELECT name, last_name FROM client c
                    JOIN phone_number pn ON c.client_id = pn.client_id 
                    WHERE name = %s;
                    """, (searched_data,))
                elif choise == 2:
                    cur.execute("""
                    SELECT name, last_name FROM client c
                    JOIN phone_number pn ON c.client_id = pn.client_id 
                    WHERE last_name = %s;
                    """, (searched_data,))
                elif choise == 3:
                    cur.execute("""
                    SELECT name, last_name FROM client c
                    JOIN phone_number pn ON c.client_id = pn.client_id 
                    WHERE email = %s;
                    """, (searched_data,))
                if choise == 4:
                    cur.execute("""
                    SELECT name, last_name FROM client c
                    JOIN phone_number pn ON c.client_id = pn.client_id 
                    WHERE phone_number = %s;
                    """, (searched_data,))
                req = cur.fetchall()
                if req:
                    print(req)
                else:
                    print('Nothing found')
            else:
                print('Wrong input number')


        delete_tables()
        create_tables()
        add_client('Vasya', 'Ginsburg', '654@mail.kz')
        add_client('Katya', 'Ginsburg', '123@mail.kz')
        add_client('Ulya', 'Ginsburg', '456@mail.kz')
        add_client('Phil', 'Ginsburg', '789@mail.kz')
        add_client('Julia', 'Ginsburg', '987@mail.kz')
        add_phone_number(1, '+7-904-997-77-00')
        add_phone_number(2, '+7-904-997-77-01')
        add_phone_number(3, '+7-904-997-77-02')
        add_phone_number(5, '+7-904-997-77-03')
        update_client_info(1, 'Peter', 'Ginsburg', '654@mail.kz')
        delete_phone_numbers(1)
        delete_client(2)
        select_by_input_data()
        
conn.close
