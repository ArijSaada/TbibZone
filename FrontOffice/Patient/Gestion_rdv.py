from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector.connection import MySQLConnection
from flask_cors import CORS
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)


@app.route('/rdvPatient', methods=['POST'])
#fonction pour ajouter un rendez-vous
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
        patient_mail = data.get('Mail')
        appointment_date = data.get('appointment_date')
        if not data :
            return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a ajouter manquantes'})
        if not nom_doc or not prenom_doc or not patient_mail or not appointment_date:
            return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a ajouter manquantes'})
        #Verifier l'existence du rendez-vous 
        cursorCheckRdv = conn.cursor()
        print("checking apt existing .... ")
        cursorCheckRdv.execute("SELECT * FROM appointment WHERE appointment_date = %s AND nom_doc = %s AND  prenom_doc = %s  AND patient_mail = %s", (appointment_date,nom_doc, prenom_doc, patient_mail))
        existing_rdv = cursorCheckRdv.fetchall()

        if existing_rdv:
            return jsonify({'success' :True,'msg': 'Rendez-vous déjà existant'})
        cursorCheckRdv.close()
        #Vérifier l existence du medecin 
        cursorCheckMedecin = conn.cursor()
        print ("checking medecin exists .... ")
        cursorCheckMedecin.execute("SELECT * FROM docteur WHERE name = %s AND prenom = %s", (nom_doc, prenom_doc,))
        existing_medecin = cursorCheckMedecin.fetchall()
        if not existing_medecin:
            return jsonify({'success':False,'msg': 'Médecin non trouvé'})
        cursorCheckMedecin.close()
        #Vérifier  la disponibilité du medecin
        cursorCheckDispo = conn.cursor()
        print ("checking medecin available .... ")
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

@app.route('/delrdvPatient', methods=['DELETE'])

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
    patient_mail = data.get('Mail')
    appointment_date = data.get('appointment_date')
    if not nom_doc or not prenom_doc or not patient_mail or not appointment_date:
        return jsonify({'success' : False, 'msg' : 'Donnees du rendez-vous a supprimer manquantes'})
    try:
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
#fonction helper pour générer des créneaux horaires

def generate_time_slots(start_date, days_ahead, start_hour=8, end_hour=17, slot_duration_minutes=60, workdays=[0, 1, 2, 3, 4]):
    slots = []
    current_date = start_date
    for _ in range(days_ahead):
        if current_date.weekday() in workdays:
            slot_time = datetime.combine(current_date, datetime.min.time()).replace(hour=start_hour)
            while slot_time.hour < end_hour:
                slots.append(slot_time.strftime('%Y-%m-%d %H:%M'))
                slot_time += timedelta(minutes=slot_duration_minutes)
        current_date += timedelta(days=1)
    return slots

@app.route('/disponibilite', methods=[ 'POST'])  
#fonction pour obtenir les disponibilités d'un médecin
def disponibilite():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='istic.glsi3',
        database='monpfe'
    )

    data = request.get_json()
    nom_doc = data.get('nom_doc')
    prenom_doc = data.get('prenom')
#donner les variables manquantes
    missing = []
    if not nom_doc or nom_doc.strip() == '':
        missing.append('nom_doc')
    if not prenom_doc or prenom_doc.strip() == '':
        missing.append('prenom')

    if missing:
        return jsonify({'success': False, 'msg': f"{', '.join(missing)} valeur(s) manquante(s)"}), 400

    cursor = conn.cursor()
    sql = "SELECT appointment_date FROM appointment WHERE nom_doc = %s AND prenom_doc = %s"
    cursor.execute(sql, (nom_doc, prenom_doc))
    # liste des dates des rendez-vous du medecin spécifié²
    busy = [row[0] for row in cursor.fetchall()]  
#produire pour les prochains 60 jours les crenaux horaires de lundi au vendredi de 8h à 17h
   
    today = datetime.today().date()
    all_slots = generate_time_slots(start_date=today, days_ahead=60)

    # Remove busy ones
    available_slots = [slot for slot in all_slots if slot not in busy]

    return jsonify({
        'success': True,
        'available_slots': available_slots
    })


@app.route('/patient/modify_rdv', methods=['PUT'])
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

        # Recoit les parametres du rendez-vous . 
        required_fields = ['Mail', 'nom_doc', 'prenom_doc', 'appointment_date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'success': False, 'msg': 'Missing fields: ' + ', '.join(missing_fields)})

        # les details du rendez-vous à modifier
        patient_mail = data['Mail']
        nom_doc = data['nom_doc']
        prenom_doc = data['prenom_doc']
        appointment_date = data['appointment_date']

        # les nouvelles du rendez-vous
        newnom_doc = data.get('newnom_doc')
        new_prenomDoc = data.get('newprenom_doc')
        new_appointment_date = data.get('newappointment_date')

        # docteur exitse ?
        cursor.execute("SELECT Mail FROM docteur WHERE name = %s AND prenom = %s", (nom_doc, prenom_doc))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({'success': False, 'msg': 'Original doctor not found'})

        # le nouveau docteur existe ?
        if newnom_doc != nom_doc or new_prenomDoc != prenom_doc:
            cursor.execute("SELECT Mail FROM docteur WHERE name = %s AND prenom = %s", (newnom_doc, new_prenomDoc))
            new_doctor = cursor.fetchone()
            if not new_doctor:
                return jsonify({'success': False, 'msg': 'New doctor not found'})

        # disponobilité du patient dans la nouvelle date
        cursor.execute("""
            SELECT * FROM appointment 
            WHERE patient_mail = %s 
              AND appointment_date = %s
              AND NOT (nom_doc = %s AND prenom_doc = %s AND appointment_date = %s)
        """, (patient_mail, new_appointment_date, nom_doc, prenom_doc, appointment_date))
        existing_patient_appt = cursor.fetchone()
        if existing_patient_appt:
            return jsonify({'success': False, 'msg': 'You already have another appointment at this time'})

        # disponobilité du nouveeau docteur dans la nouvelle date
        cursor.execute("""
            SELECT * FROM appointment 
            WHERE nom_doc = %s 
              AND prenom_doc = %s 
              AND appointment_date = %s
              AND NOT (nom_doc = %s AND prenom_doc = %s AND patient_mail = %s AND appointment_date = %s)
        """, (newnom_doc, new_prenomDoc, new_appointment_date,
              nom_doc, prenom_doc, patient_mail, appointment_date))
        conflicting_doc_appt = cursor.fetchone()
        if conflicting_doc_appt:
            return jsonify({'success': False, 'msg': 'New doctor already has an appointment at this time'})

        # faire la modification du rendez-vous
        cursor.execute("""
            UPDATE appointment
            SET nom_doc = %s,
                prenom_doc = %s,
                appointment_date = %s
            WHERE patient_mail = %s
              AND nom_doc = %s
              AND prenom_doc = %s
              AND appointment_date = %s
        """, (
            newnom_doc,
            new_prenomDoc,
            new_appointment_date,
            patient_mail,
            nom_doc,
            prenom_doc,
            appointment_date
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'msg': 'No appointment was modified - check your data'})

        return jsonify({'success': True, 'msg': 'Appointment successfully modified'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'msg': f'Database error: {str(err)}'})
    except Exception as e:
        return jsonify({'success': False, 'msg': f'Unexpected error: {str(e)}'})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5400, debug=True)

