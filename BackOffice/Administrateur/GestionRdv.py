from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='istic.glsi3',
        database='monpfe'
    )

@app.route('/admin/getAllrdv', methods=['GET'])
def get_all_rdvs():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                a.id,
                a.appointment_date,
                a.details,
                a.nom_doc,
                a.prenom_doc,
                p.nom AS nom_patient,
                p.prenom AS prenom_patient
            FROM 
                appointment a
            JOIN 
                patient p ON a.patient_mail = p.Mail
        """
        cursor.execute(query)
        results = cursor.fetchall()

        return jsonify({"success": True, "msg": results})
    except Error as e:
        return jsonify({"success": False, "msg": str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/admin/search_rdvs', methods=['POST'])
def search_rdvs():
    try:
        data = request.json or {}
        v = data.get("v", "").strip().lower()

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        results = []

        if not v:
            return jsonify({"success": False, "msg": "Empty search"})
      

        # Step 1: Check if v is in appointment table
        cursor.execute("SELECT * FROM appointment WHERE LOWER(patient_mail) =  %s or LOWER(nom_doc) = %s  or LOWER(prenom_doc) = %s or LOWER(appointment_date) = %s  ", (v,v,v,v))
        results = cursor.fetchall()
        if results:
            return jsonify({"success": True, "msg": results})

        # Step 2: Check if it's a doctor mail
        cursor.execute("SELECT name, prenom FROM docteur WHERE LOWER(Mail) = %s", (v,))
        doctor = cursor.fetchone()
        if doctor:
            nom_doctor = doctor["name"]
            prenom_doctor = doctor["prenom"]
            cursor.execute("SELECT * FROM appointment WHERE nom_doc = %s and prenom_doc = %s ) ", (nom_doctor,prenom_doctor))
            msg = cursor.fetchall()
            return jsonify({"success": True, "msg": msg})
        # Step 3: Check if it's a patient nom or prenom
        cursor.execute("SELECT Mail FROM patient WHERE LOWER(nom)= %s or LOWER(prenom) = %s", (v,v))
        patient = cursor.fetchone()
        if patient:
            patient_mail = patient["Mail"]
            
            cursor.execute("SELECT * FROM appointment WHERE patient_mail = %s", (patient_mail,))
            msg = cursor.fetchall()
            return jsonify({"success": True, "msg": msg})
        return jsonify({"success": False, "msg": "Aucun rendez-vous trouvé"})
            


  
        

    except Error as e:
        return jsonify({"success": False, "msg": str(e)})
    finally:
        cursor.close()
        conn.close()


        

@app.route('/admin/add_rdv', methods=['POST'])
def add_rdv ():
    cursorAjouterRdv = None
    conn = None
    try:
        conn = mysql.connector.connect(
           host= '127.0.0.1',
            user='root',
            password='istic.glsi3',
            database = 'monpfe',
            port = 3306
        
        )
        #Récupérer les données du formulaire
        data = request.get_json()
        nom_doc = data.get('nom_doc')
        prenom_doc = data.get('prenom_doc')
        nom_patient = data.get('nom_patient')
        prenom_patient = data.get('prenom_patient')
        appointment_date = data.get('appointment_date')
        if not data :
            return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a ajouter manquantes'})
        if not nom_doc or not prenom_doc or not nom_patient or not prenom_patient or not appointment_date:
            return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a ajouter manquantes'})
        #Vérifier l'existence du patient
        cursorCheckPatient = conn.cursor()
        print ("checking patient exists .... ")
        cursorCheckPatient.execute("SELECT Mail FROM patient WHERE nom = %s AND prenom = %s", (nom_patient, prenom_patient))
        existing_patient = cursorCheckPatient.fetchone()
        if not existing_patient:
            return jsonify({'success' : False,'msg': 'Patient non trouvé'})
        patient_mail = existing_patient[0]
        cursorCheckPatient.close()
        #Verifier l'existence du rendez-vous 
        cursorCheckRdv = conn.cursor()
        print("checkign apt existing .... ")
        cursorCheckRdv.execute("SELECT * FROM appointment WHERE appointment_date = %s AND nom_doc = %s AND  prenom_doc = %s  AND patient_mail = %s", (appointment_date,nom_doc, prenom_doc, patient_mail))
        existing_rdv = cursorCheckRdv.fetchone()

        if existing_rdv:
            return jsonify({'success' :True,'msg': 'Rendez-vous déjà existant'})
        cursorCheckRdv.close()
        #Vérifier l existence du docteur 
        cursorCheckMedecin = conn.cursor()
        print ("checking docteur exists .... ")
        cursorCheckMedecin.execute("SELECT * FROM docteur WHERE name = %s AND prenom = %s", (nom_doc, prenom_doc,))
        existing_medecin = cursorCheckMedecin.fetchone()
        if not existing_medecin:
            return jsonify({'success':False,'msg': 'Médecin non trouvé'})
        cursorCheckMedecin.close()
        #Vérifier  la disponibilité du docteur
        cursorCheckDispo = conn.cursor()
        print ("checking docteur available .... ")
        cursorCheckDispo.execute("SELECT * FROM appointment WHERE nom_doc = %s AND prenom_doc = %s AND appointment_date = %s", (nom_doc, prenom_doc, appointment_date))
        existing_dispo = cursorCheckDispo.fetchone()
        if existing_dispo:
            return jsonify({'success': False,'msg': 'Médecin non disponible'})
        cursorCheckDispo.close()
        #Vérifier la disponibilité du patient 
        cursorCheckPatient = conn.cursor()
        print ("checking patient available .... ")
        cursorCheckPatient.execute("SELECT * FROM appointment WHERE patient_mail = %s AND appointment_date = %s", (patient_mail, appointment_date))
        existing_patient = cursorCheckPatient.fetchone()
        if existing_patient:
            return jsonify({'success' :False,'msg': 'Patient non disponible'})
        cursorCheckPatient.close()
        #Ajouter le rendez-vous
        cursorAjouterRdv = conn.cursor()
        print ("adding appointment .... ")
        cursorAjouterRdv.execute("INSERT INTO appointment (nom_doc, prenom_doc, appointment_date, patient_mail) VALUES (%s,%s,%s,%s)", (nom_doc, prenom_doc, appointment_date, patient_mail))
        conn.commit()
        return jsonify({'success' : True,'msg': 'Rendez-vous ajouté avec succès'})
    except mysql.connector.Error as err:
        return jsonify({'success' : False,'msg': str(err)})
    finally:
        if cursorAjouterRdv:
            cursorAjouterRdv.close()
        if conn:
            conn.close()
        
@app.route('/admin/delete_rdv', methods=['DELETE'])
def supprimer_rdv():
    cursor_del = None
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user = 'root',
        password = 'istic.glsi3',
        database = 'monpfe',
        port = 3306
    )
    data = request.get_json()
    nom_doc = data.get('nom_doc')
    prenom_doc = data.get('prenom_doc')
    nom_patient = data.get('nom_patient')
    prenom_patient = data.get('prenom_patient')
    appointment_date = data.get('appointment_date')
    if not nom_doc or not prenom_doc or not nom_patient or not prenom_patient or not appointment_date:
        return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a supprimer manquantes'})
    try:
        #recuperer l'email du patient
        cursor_patient = conn.cursor()
        cursor_patient.execute("SELECT Mail FROM patient WHERE nom = %s AND prenom = %s", (nom_patient, prenom_patient))
        existing_patient = cursor_patient.fetchone()
        if not existing_patient:    
            return jsonify({'success' : False, 'msg' : 'Patient non trouvé'})
        patient_mail = existing_patient[0]
        cursor_patient.close()
        cursor_check = conn.cursor()
        cursor_check.execute("SELECT * FROM appointment WHERE nom_doc = %s AND prenom_doc = %s AND patient_mail = %s AND appointment_date = %s", (nom_doc, prenom_doc, patient_mail, appointment_date))
        existing_rdv = cursor_check.fetchone()
        if not existing_rdv:
            return jsonify({'success' : False, 'msg' : 'Rendez-vous non trouvé'})
        cursor_check.close()
        cursor_del = conn.cursor()
        cursor_del.execute("DELETE FROM appointment WHERE nom_doc = %s AND prenom_doc = %s AND patient_mail = %s AND appointment_date = %s", (nom_doc, prenom_doc, patient_mail, appointment_date))
        conn.commit()
        return jsonify({'success' : True, 'msg' : 'Rendez-vous supprimé avec succès'})
    except mysql.connector.Error as err:
        return jsonify({'success' : False, 'msg' : str(err)})
    finally:
        if cursor_del:
            cursor_del.close()
        if conn:
            conn.close()

@app.route('/admin/modify_rdv', methods=['PUT'])
def modif_rdv():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )
        cursor = conn.cursor(dictionary=True)
        data = request.json

        # Validate required fields
        required_fields = ['nom_patient', 'prenom_patient', 'nom_doc', 'prenom_doc', 'appointment_date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'success': False, 'msg': 'Missing required fields: ' + ', '.join(missing_fields)})

        # Original appointment details
        nom_patient = data['nom_patient']
        prenom_patient = data['prenom_patient']
        nom_doc = data['nom_doc']
        prenom_doc = data['prenom_doc']
        appointment_date = data['appointment_date']

        # New appointment details (optional)
        new_nom_patient = data.get('newnom_patient')
        new_prenom_patient = data.get('newprenom_patient')
        new_nom_doc = data.get('newnom_doc')
        new_prenom_doc = data.get('newprenom_doc')
        new_appointment_date = data.get('newappointment_date', appointment_date)

        # Get original patient mail
        cursor.execute("SELECT Mail FROM patient WHERE nom = %s AND prenom = %s", 
                       (nom_patient, prenom_patient))
        patient = cursor.fetchall()
        if not patient:
            return jsonify({'success': False, 'msg': 'Original patient not found'})
        original_patient_mail = patient[0]['Mail']

        # Get original doctor mail
        cursor.execute("SELECT Mail FROM docteur WHERE name = %s AND prenom = %s",
                       (nom_doc, prenom_doc))
        doctor = cursor.fetchall()
        if not doctor:
            return jsonify({'success': False, 'msg': 'Original doctor not found'})

        # Default to original patient mail unless changed
        new_patient_mail = original_patient_mail

        # Handle patient change if provided
        if new_nom_patient and new_prenom_patient:
            cursor.execute("SELECT Mail FROM patient WHERE nom = %s AND prenom = %s",
                           (new_nom_patient, new_prenom_patient))
            new_patient = cursor.fetchall()
            if not new_patient:
                return jsonify({'success': False, 'msg': 'New patient not found'})
            new_patient_mail = new_patient[0]['Mail']

            # Check if new patient already has appointment at new time
            cursor.execute("""
                SELECT * FROM appointment 
                WHERE patient_mail = %s 
                AND appointment_date = %s
                AND NOT (nom_doc = %s AND prenom_doc = %s AND appointment_date = %s)
            """, (new_patient_mail, new_appointment_date, nom_doc, prenom_doc, appointment_date))
            hasrdv  = cursor.fetchone()

            if hasrdv:
                return jsonify({'success': False, 'msg': 'New patient already has an appointment at this time'})

        # Handle doctor change if provided
        new_nom_doc_final = new_nom_doc if new_nom_doc else nom_doc
        new_prenom_doc_final = new_prenom_doc if new_prenom_doc else prenom_doc

        if new_nom_doc or new_prenom_doc:
            cursor.execute("SELECT Mail FROM docteur WHERE name = %s AND prenom = %s",
                           (new_nom_doc_final, new_prenom_doc_final))
            new_doctor = cursor.fetchall()
            if not new_doctor:
                return jsonify({'success': False, 'msg': 'New doctor not found'})

            # Check if new doctor already has appointment at new time
            cursor.execute("""
                SELECT * FROM appointment 
                WHERE nom_doc = %s 
                AND prenom_doc = %s
                AND appointment_date = %s
                AND NOT (patient_mail = %s AND appointment_date = %s)
            """, (new_nom_doc_final, new_prenom_doc_final, new_appointment_date,
                  original_patient_mail, appointment_date))
            hasrdv = cursor.fetchone()

            if hasrdv:
                return jsonify({'success': False, 'msg': 'New doctor already has an appointment at this time'})

        # Update the appointment
        update_sql = """
            UPDATE appointment
            SET nom_doc = %s,
                prenom_doc = %s,
                patient_mail = %s,
                appointment_date = %s
            WHERE nom_doc = %s
            AND prenom_doc = %s
            AND patient_mail = %s
            AND appointment_date = %s
        """
        cursor.execute(update_sql, (
            new_nom_doc_final,
            new_prenom_doc_final,
            new_patient_mail,
            new_appointment_date,
            nom_doc,
            prenom_doc,
            original_patient_mail,
            appointment_date
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'msg': 'No appointment was modified - check your criteria'})

        return jsonify({'success': True, 'msg': 'Appointment successfully modified'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'msg': f"Database error: {str(err)}"})
    except Exception as e:
        return jsonify({'success': False, 'msg': f"Unexpected error: {str(e)}"})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5500, host='0.0.0.0')
