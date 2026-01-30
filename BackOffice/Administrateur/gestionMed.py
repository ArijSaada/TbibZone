from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector.connection import MySQLConnection
from flask_cors import CORS
import secrets
import string
from zxcvbn import zxcvbn
from passlib.hash import bcrypt
import uuid

app = Flask(__name__)
CORS(app)

def generate_strong_hashed_token(length=16, min_strength=3):
    alphabet = string.ascii_letters + string.digits + string.punctuation

    while True:
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        result = zxcvbn(token)
        if result['score'] >= min_strength:
            return bcrypt.hash(token)

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'istic.glsi3',
    'database': 'monpfe',
    'port' : 3306
}
@app.route('/AjouterDocteur', methods=['POST'])
def ajouter_Medecin():
    data = request.json
    Mail = data.get('Mail') or ""
    
    name = data.get('name') or ""
    prenom = data.get('prenom') or ""
    localisation = data.get('localisation') or ""
    spec = data.get('speciality') or ""
    Missing = []
    if(Mail == ""):
        Missing.append("Mail")
    if (name == ""):
        Missing.append("name")
    if(prenom == ""):
        Missing.append("prenom")
    if (localisation ==""):
        Missing.append("localisation")
    if (spec ==""):
        Missing.append("speciality")
    if (len(Missing) > 0):
        return jsonify({'success': False, 'msg': Missing})
        
    


    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)
        
        found = True
        while found  == True : 
            pwd = generate_strong_hashed_token()
            sqlpwd = "SELECT * FROM docteur WHERE pwd = %s"
            cursorpwd = connection.cursor()
            cursorpwd.execute(sqlpwd, (pwd,))
            found = cursorpwd.fetchone()
            cursorpwd.close()


       

        # Vérifier si le médecin existe déjà
        Sqldocteur = "SELECT * FROM docteur WHERE (Mail = %s OR pwd = %s)"
        cursordocteur = connection.cursor()
        cursordocteur.execute(Sqldocteur, (Mail,pwd))
        existing_docteur = cursordocteur.fetchone()
        cursordocteur.close()

        if existing_docteur:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur existe déjà en tant que docteur'})

        # Insérer le nouvel docteur
        cursor = connection.cursor()
        cursor.execute("INSERT INTO docteur (Mail, pwd, name, prenom,speciality,location ) VALUES (%s, %s, %s, %s,%s, %s)",
                       (Mail, pwd, name, prenom,spec, localisation))
        connection.commit()
        return jsonify({'success': True, 'msg': 'docteur added successfully' + 'token : ' + pwd}), 201

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/Supprimerdocteur', methods=['DELETE'])
def supprimer_docteur():
    data = request.json
    Mail = data.get('Mail') or ""

    if Mail == "":
        return jsonify({'success': False, 'msg': 'Missing required fields'})

    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)

        # Vérifier si le docteur existe
        Sqldocteur = "SELECT * FROM docteur WHERE Mail = %s"
        cursordocteur = connection.cursor()
        cursordocteur.execute(Sqldocteur, (Mail,))
        existing_docteur = cursordocteur.fetchone()
        cursordocteur.close()

        if not existing_docteur:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur n’existe pas en tant qu’docteur'})

        # Supprimer l’docteur
        cursor = connection.cursor()
        cursor.execute("DELETE FROM docteur WHERE Mail = %s", (Mail,))
        connection.commit()
        return jsonify({'success': True, 'msg': 'docteur deleted successfully'}), 200

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

        # Récupérer tous les docteurs
        cursor.execute("SELECT * FROM docteur")
        docteurs = cursor.fetchall()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

        return jsonify({'success': True, 'msg': docteurs}), 200

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/Afficherdocteur', methods=['GET'])
def mes_docteurs():
    return getAll()

@app.route('/chercherdocteur', methods=['GET'])
def chercher_docteur():
    v = request.args.get('v') or request.args.get('V') or ''
    v = v.lower()
    print("Search term (v):", v)

    fetch = []

    try:
        connection = MySQLConnection(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM docteur")
        listdocteur = cursor.fetchall()
        cursor.close()

        if not v:
            print("No search term provided, returning all doctors.")
            return jsonify({"success": True, "msg": listdocteur})

        for docteur in listdocteur:
            print("Checking docteur:", docteur)
            if (
                v in (docteur.get("Mail") or "").lower() or
                v in (docteur.get("pwd") or "").lower() or
                v in (docteur.get("name") or "").lower() or
                v in (docteur.get("prenom") or "").lower() or 
                v in (docteur.get("location") or "").lower() or
                v in (docteur.get("speciality") or "").lower()
            ):
                fetch.append(docteur)

        if not fetch:
            return jsonify({'success': False, 'msg': 'Aucun docteur trouvé ayant ces paramètres', 'list': listdocteur})

        return jsonify({'success': True, 'msg': fetch})

    finally:
        if connection:
            connection.close()

@app.route('/modifierDocteur', methods=['PUT'])
def Modifier_med():
    connection = None
    cursor = None
    try:
        connection = MySQLConnection(**db_config)
        data = request.json

        # Required old fields
        Mail = data.get('Mail')
        pwd = data.get('pwd')
        name = data.get('name')
        prenom = data.get('prenom')
        localisation = data.get('localisation')
        specialite = data.get('specialite')

        # Track missing fields
        fields = []
        if not Mail: fields.append('Mail')
        if not pwd: fields.append('pwd')
        if not name: fields.append('name')
        if not prenom: fields.append('prenom')
        if not localisation: fields.append('localisation')
        if not specialite: fields.append('specialite')

        # If any required field is missing
        if fields:
            return jsonify({'success': False, 'msg': f'Champs manquants: {fields}'})

        # New values to update
        newMail = data.get('newMail')
        newpwd = data.get('newpwd')
        newname = data.get('newname')
        newprenom = data.get('newprenom')
        newlocalisation = data.get('newlocalisation')
        newspecialite = data.get('newspecialite')

        # If none of the new fields are provided
        if not any([newMail, newpwd, newname, newprenom, newlocalisation, newspecialite]):
            return jsonify({'success': False, 'msg': 'Aucune nouvelle donnée fournie'})

        

        # Check if the current doctor exists
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM docteur WHERE Mail = %s", (Mail,))
        exists = cursor.fetchone()
        if not exists:
            return jsonify({'success': False, 'msg': 'Docteur inexistant'})

        # Check if newMail already exists for another doctor
        if newMail != Mail:  # Allow keeping the same email
            cursor.execute("SELECT * FROM docteur WHERE Mail = %s", (newMail,))
            if cursor.fetchone():
                return jsonify({'success': False, 'msg': 'Ce nouvel email est déjà utilisé'})

        # Update doctor
        sqlModif = """
            UPDATE docteur 
            SET name = %s, prenom = %s, Mail = %s, pwd = %s, location = %s, speciality = %s 
            WHERE Mail = %s
        """
        cursor.execute(sqlModif, (newname, newprenom, newMail, newpwd, newlocalisation, newspecialite, Mail))
        connection.commit()
        return jsonify({'success': True, 'msg': 'Médecin mis à jour avec succès'})
    
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5222, debug=True)
