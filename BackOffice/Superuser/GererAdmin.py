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
@app.route('/AjouterAdmin', methods=['POST'])
def ajouter_admin():
    data = request.json
    Mail = data.get('Mail') or ""
    pwd = data.get('pwd') or ""
    nom_admin = data.get('nom_admin') or ""
    prenom_admin = data.get('prenom_admin') or ""

    if Mail == "" or pwd == "" or nom_admin == "" or prenom_admin == "":
        return jsonify({'success': False, 'msg': 'Missing required fields'})

    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)

        # Vérifier si c'est le mail d’un superuser
        sqlSuperUser = "SELECT * FROM superuser WHERE Mail = %s"
        cursorSuperUser = connection.cursor()
        cursorSuperUser.execute(sqlSuperUser, (Mail,))
        existing_SuperUser = cursorSuperUser.fetchone()
        cursorSuperUser.close()

        # Vérifier si c'est le mail d’un docteur
        sqlDocteur = "SELECT * FROM docteur WHERE Mail = %s"
        cursorDocteur = connection.cursor()
        cursorDocteur.execute(sqlDocteur, (Mail,))
        existing_Docteur = cursorDocteur.fetchone()
        cursorDocteur.close()

        if existing_SuperUser or existing_Docteur:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur ne peut pas être un administrateur'})

        # Vérifier si l’admin existe déjà
        SqlAdmin = "SELECT * FROM admin WHERE Mail = %s"
        cursorAdmin = connection.cursor()
        cursorAdmin.execute(SqlAdmin, (Mail,))
        existing_Admin = cursorAdmin.fetchone()
        cursorAdmin.close()

        if existing_Admin:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur existe déjà en tant qu’administrateur'})

        # Insérer le nouvel admin
        cursor = connection.cursor()
        cursor.execute("INSERT INTO admin (Mail, pwd, nom, prenom) VALUES (%s, %s, %s, %s)",
                       (Mail, pwd, nom_admin, prenom_admin))
        connection.commit()
        return jsonify({'success': True, 'msg': 'Admin added successfully'}), 201

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/SupprimerAdmin', methods=['DELETE'])
def supprimer_admin():
    data = request.json
    Mail = data.get('Mail') or ""

    if Mail == "":
        return jsonify({'success': False, 'msg': 'Missing required fields'})

    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)

        # Vérifier si l’admin existe
        SqlAdmin = "SELECT * FROM admin WHERE Mail = %s"
        cursorAdmin = connection.cursor()
        cursorAdmin.execute(SqlAdmin, (Mail,))
        existing_Admin = cursorAdmin.fetchone()
        cursorAdmin.close()

        if not existing_Admin:
            return jsonify({'success': False, 'msg': 'Cet Utilisateur n’existe pas en tant qu’administrateur'})

        # Supprimer l’admin
        cursor = connection.cursor()
        cursor.execute("DELETE FROM admin WHERE Mail = %s", (Mail,))
        connection.commit()
        return jsonify({'success': True, 'msg': 'Admin deleted successfully'}), 200

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

        # Récupérer tous les admins
        cursor.execute("SELECT * FROM admin")
        admins = cursor.fetchall()

        return jsonify({'success': True, 'msg': admins}), 200

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/AfficherAdmin', methods=['GET'])
def mes_admins():
    return getAll()

@app.route('/chercherAdmin', methods=['GET'])


def chercher_admin():
    data = request.json
    v = request.args.get('v', '').lower()
    fetch = []
    listAdmin = []
    if ((not v ) or v == ""):
        print("v est vide")
        return getAll()
        
    


    connection = None
    cursor = None

    try:
        connection = MySQLConnection(**db_config)
        cursorAll = connection.cursor(dictionary=True)
        cursorAll.execute("SELECT * FROM admin")
        listAdmin = cursorAll.fetchall()
        cursorAll.close()
        for admin in listAdmin:
            print(admin)
           
            if (
                v in (admin["Mail"] or "").lower() or
                v in (admin["pwd"] or "").lower() or
                v in (admin["nom"] or "").lower() or
                v in (admin["prenom"] or "").lower()
            ):
                fetch.append(admin)

        if len(fetch) == 0:
            return jsonify({'success': False, 'msg': 'Aucun admin trouvé ayant ces parametres', 'list': listAdmin})
        return jsonify({'success': True, 'msg': fetch}), 200

     

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@app.route('/modif_admin', methods=['PUT'])
def Modifier_Admin():
    connection = None
    cursor = None
    try:
        connection = MySQLConnection(**db_config)
        data = request.json

        # Required old fields
        Mail = data.get('Mail')
        pwd = data.get('pwd')
        nom = data.get('nom_admin')
        prenom = data.get('prenom_admin')
        

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
        newname = data.get('newnom_admin')
        newprenom= data.get('newprenom_admin')
       

        # If none of the new fields are provided
        if not any([newMail, newpwd, newname, newprenom]):
            return jsonify({'success': False, 'msg': 'Aucune nouvelle donnée fournie'})

        

        # Check if the current doctor exists
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE Mail = %s", (Mail,))
        exists = cursor.fetchone()
        if not exists:
            return jsonify({'success': False, 'msg': 'admin inexistant'})

        # Check if newMail already exists for another doctor
        if newMail != Mail:  # Allow keeping the same email
            cursor.execute("SELECT * FROM admin WHERE Mail = %s", (newMail,))
            if cursor.fetchone():
                return jsonify({'success': False, 'msg': 'Ce nouvel email est déjà utilisé'})

        # Update doctor
        sqlModif = """
            UPDATE admin 
            SET nom = %s, prenom = %s, Mail = %s, pwd = %s 
            WHERE Mail = %s
        """
        cursor.execute(sqlModif, (newname, newprenom, newMail, newpwd, Mail))
        connection.commit()
        return jsonify({'success': True, 'msg': 'Admin mis à jour avec succès'})
    
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5201, debug=True)
