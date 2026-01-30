from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'istic.glsi3',
    'database': 'monpfe',
    'port': 3306
}

@app.route('/login', methods=['POST'])
def login_Super():
    cursor = None
    conn = None
    try:
        data = request.get_json()
        Mail = data.get('Mail')
        pwd = data.get('pwd')

        if not Mail or not pwd:
            return jsonify({'success': False, 'msg': 'Missing Mail or password'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query_all = "SELECT * FROM superuser WHERE Mail = %s AND pwd = %s"
        cursor.execute(query_all, (Mail, pwd))
        user = cursor.fetchone()

        if user:
            return jsonify({'success': True, 'msg': 'Let him in'}), 200
        else:
            query_mail = "SELECT * FROM superuser WHERE Mail = %s"
            cursor.execute(query_mail, (Mail,))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({'success': False, 'msg': 'Wrong password'}), 401
            else:
                return jsonify({'success': False, 'msg': 'Super-user not found'}), 401

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'msg': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
