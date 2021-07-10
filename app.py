from flask import Flask, jsonify
import psycopg2

con = psycopg2.connect(dbname='test_db1', user='root', password='root', host='db')


app = Flask(__name__)


@app.route('/')
def main_page():
    return 'Welcome to API service!'


@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_users():
    cur = con.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    global user_list
    user_list = {}
    for r in rows:
        users_dict = {}
        users_dict['name'] = r[1]
        users_id_dict = {r[0]: {'id': r[0],
                                'name': r[1]}}
        user_list.update(users_id_dict)
    return jsonify({'users_info': user_list})


@app.route('/todo/api/v1.0/users/<int:users_id>', methods=['GET'])
def get_user_id(users_id):
    get_user = user_list[users_id]
    return f'{get_user}'


@app.route('/todo/api/v1.0/del/<int:del_id>', methods=['GET'])
def del_user_id(del_id):
    cur = con.cursor()
    cur.execute(f"delete from users where id={del_id}")
    con.commit()
    return f'id {del_id} delete success'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')