from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector.connection import MySQLConnection
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'istic.glsi3',
    'database': 'monpfe',
    'port' : 3306
}
@app.route('/AjouterPatient', methods=['POST'])
def ajouter_patient():
    data = request.json
    Mail = data.get('Mail') or ""
    pwd = data.get('pwd') or ""
    nom = data.get('nom') or ""
    prenom = data.get('prenom') or ""

    if Mail == "" or pwd == "" or nom == "" or prenom == "":
        return jsonify({'success': False, 'msg': 'Missing required fields'})

    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)

       

        # Vérifier si le patient existe déjà
        Sqlpatient = "SELECT * FROM patient WHERE Mail = %s"
        cursorpatient = connection.cursor()
        cursorpatient.execute(Sqlpatient, (Mail,))
        existing_patient = cursorpatient.fetchone()
        cursorpatient.close()

        if existing_patient:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur existe déjà en tant que patient'})

        # Insérer le nouvel patient
        cursor = connection.cursor()
        cursor.execute("INSERT INTO patient (Mail, pwd, nom, prenom) VALUES (%s, %s, %s, %s)",
                       (Mail, pwd, nom, prenom))
        connection.commit()
        return jsonify({'success': True, 'msg': 'patient added successfully'}), 201

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/Supprimerpatient', methods=['DELETE'])
def supprimer_patient():
    data = request.json
    Mail = data.get('Mail') or ""

    if Mail == "":
        return jsonify({'success': False, 'msg': 'Missing required fields'})

    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)

        # Vérifier si le patient existe
        Sqlpatient = "SELECT * FROM patient WHERE Mail = %s"
        cursorpatient = connection.cursor()
        cursorpatient.execute(Sqlpatient, (Mail,))
        existing_patient = cursorpatient.fetchone()
        cursorpatient.close()

        if not existing_patient:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur n’existe pas en tant qu’patient'})

        # Supprimer l’patient
        cursor = connection.cursor()
        cursor.execute("DELETE FROM patient WHERE Mail = %s", (Mail,))
        connection.commit()
        return jsonify({'success': True, 'msg': 'patient deleted successfully'}), 200

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def getAll():
    connection = None
    cursor = None
    try:
        connection = MySQLConnection(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Récupérer tous les patients
        cursor.execute("SELECT * FROM patient")
        patients = cursor.fetchall()

        return jsonify({'success': True, 'msg': patients}), 200

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/Afficherpatient', methods=['GET'])


def mes_patients():
    print(app.url_map)


    return getAll()

@app.route('/chercherpatient', methods=['GET'])


def chercher_patient():
    #data = request.json
    v = request.args.get('v', '').lower()
    fetch = []
    listpatient = []
    if ((not v ) or v == ""):
        print("v est vide")
        return getAll()
        
    


    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)
        cursorAll = connection.cursor(dictionary=True)
        cursorAll.execute("SELECT * FROM patient")
        listpatient = cursorAll.fetchall()
        cursorAll.close()
        for patient in listpatient:
            print(patient)
           
            if (
                v in (patient["Mail"] or "").lower() or
                v in (patient["pwd"] or "").lower() or
                v in (patient["nom"] or "").lower() or
                v in (patient["prenom"] or "").lower()
            ):
                fetch.append(patient)

        if len(fetch) == 0:
            return jsonify({'success': False, 'msg': 'Aucun patient trouvé ayant ces parametres', 'list': listpatient})
        return jsonify({'success': True, 'msg': fetch}), 200

     

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@app.route('/modifierPatient', methods=['PUT'])
def Modifier_med():
    connection = None
    cursor = None
    try:
        connection = MySQLConnection(**db_config)
        data = request.json

        # Required old fields
        Mail = data.get('Mail')
        pwd = data.get('pwd')
        nom = data.get('nom')
        prenom = data.get('prenom')
        

        # Track missing fields
        fields = []
        if not Mail: fields.append('Mail')
        if not pwd: fields.append('pwd')
        if not nom: fields.append('nom')
        if not prenom: fields.append('prenom')
      

        # If any required field is missing
        if fields:
            return jsonify({'success': False, 'msg': f'Champs manquants: {fields}'})

        # New values to update
        newMail = data.get('newMail')
        newpwd = data.get('newpwd')
        newname = data.get('newname')
        newprenom = data.get('newprenom')
       

        # If none of the new fields are provided
        if not any([newMail, newpwd, newname, newprenom]):
            return jsonify({'success': False, 'msg': 'Aucune nouvelle donnée fournie'})

        

        # Check if the current doctor exists
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patient WHERE Mail = %s", (Mail,))
        exists = cursor.fetchone()
        if not exists:
            return jsonify({'success': False, 'msg': 'patient inexistant'})

        # Check if newMail already exists for another doctor
        if newMail != Mail:  # Allow keeping the same email
            cursor.execute("SELECT * FROM patient WHERE Mail = %s", (newMail,))
            if cursor.fetchone():
                return jsonify({'success': False, 'msg': 'Ce nouvel email est déjà utilisé'})

        # Update doctor
        sqlModif = """
            UPDATE patient 
            SET nom = %s, prenom = %s, Mail = %s, pwd = %s 
            WHERE Mail = %s
        """
        cursor.execute(sqlModif, (newname, newprenom, newMail, newpwd, Mail))
        connection.commit()
        return jsonify({'success': True, 'msg': 'Patient mis à jour avec succès'})
    
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5210, debug=True)
