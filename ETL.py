import requests
import psycopg2


class CreateUsersData():
    def __init__(self, name_db):
        self.name_db = name_db

    def connection_db(self):
        con = psycopg2.connect(dbname=self.name_db, user='root', password='root', host='db')
        return con

    def add_user_to_base(self):
        con_into = self.connection_db()
        cur_into = con_into.cursor()
        cur_into.execute("CREATE TABLE users (id serial PRIMARY KEY, name varchar(255));")

        coun = 0
        while True:
            r = requests.get('https://randomuser.me/api')
            if r.json()['results'][0]['gender'] == 'male':
                coun += 1
                print(r.json()['results'][0]['name']['first'], r.json()['results'][0]['name']['last'])
                cur_into.execute(
                    f"insert into users(name) values ('{r.json()['results'][0]['name']['first']} {r.json()['results'][0]['name']['last']}')")
            else:
                pass
            if coun == 100:
                break
        con_into.commit()

        con_into.commit()


    def show_database_users(self):
        con_into_show = self.connection_db()
        cur_into_show = con_into_show.cursor()
        cur_into_show.execute("select * from users")
        rows = cur_into_show.fetchall()
        print(rows)
        cur_into_show.close()


users = CreateUsersData('test_db1')
users.add_user_to_base()
users.show_database_users()
