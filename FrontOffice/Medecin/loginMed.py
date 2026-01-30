from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# MySQL database configuration


@app.route('/loginMed', methods=['POST'])
def loginMed():
    conn =None
    cursor = None
    try:
        data = request.get_json()
        Mail = data.get('Mail')
        pwd = data.get('pwd')
   
        
        # Corrected the variable names to match with 'Mail' and 'pwd'
        if not Mail or not pwd:
            if not Mail and  pwd :
                return jsonify({'success':False,'msg': 'Missing email '})
            if  Mail and not pwd :

                return jsonify({'success':False,'msg': 'Missing  password'})
            if (not Mail and not pwd):
                return jsonify({'success':False,'msg': 'Missing email and password'})


                
            
        
        # Establish MySQL connection
        conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='istic.glsi3',
    database='monpfe',
    port=3306
)

        cursor = conn.cursor()
        
        # Query to check if user exists and password matches
        query_all = "SELECT * FROM docteur WHERE Mail = %s AND pwd = %s;"

        cursor.execute(query_all, (Mail, pwd))
        user = cursor.fetchone()
        
        if user:
            return jsonify({'success': True ,'msg': 'Let him in'}), 200
        else:
            # Check if the email exists for wrong password case
            query_mail = "SELECT * FROM docteur WHERE Mail = %s"
            cursor.execute(query_mail, (Mail,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(user);
                return jsonify({'success':False ,'msg': 'Wrong password'})
            else:
                return jsonify({'success':False ,'msg': 'User not found'})
    except mysql.connector.Error as err:
        return jsonify({'success':False ,'msg': str(err)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True, port=5006)
