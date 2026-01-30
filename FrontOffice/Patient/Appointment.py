from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# parametres de la base de données
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'istic.glsi3',
    'database': 'monpfe'
}
#parametres de la routes pour api 
@app.route('/rdv', methods=['POST'])
#fonction pour obtenir les rendez-vous
def get_appointments():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return jsonify({'error': 'Missing username'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch appointments from the database
        query = """
        SELECT appointment_date, details, patient_mail,nom_doc,prenom_doc
        FROM appointment
        WHERE patient_mail = %s
        """
        cursor.execute(query, (username,))
        appointments = cursor.fetchall()

        if appointments:
            response_data = []
            for appointment in appointments:
                try:
                    # Convertir la date de chaine de caractères en objet datetime
                    appointment_dt = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d %H:%M:%S')
                    '''
                    date_str = appointment_dt.strftime('%B %d, %Y')
                    time_str = appointment_dt.strftime('%I:%M %p')
                    '''
                    formatted_datetime = appointment_dt.strftime('%Y-%m-%d %H:%M:%S')

                except ValueError:
                    '''
                    # Fallback in case of unexpected format
                    date_str = appointment['appointment_date']
                    time_str = 'Unknown'
                    '''
                    formatted_datetime = appointment['appointment_date'] 

                appointment_data = {
                    'appointment_date': formatted_datetime,
                    'nom_doc' : appointment['nom_doc'],
                    'prenom_doc' : appointment['prenom_doc'],
                    'details': appointment['details'],
                    'status': 'Upcoming'
                }
                response_data.append(appointment_data)

            return jsonify({'appointments': response_data}), 200
        else:
            return jsonify({'message': 'No appointment found for this user'}), 405

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
