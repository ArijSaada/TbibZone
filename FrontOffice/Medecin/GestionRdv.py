from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector.connection import MySQLConnection
from flask_cors import CORS
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)


def recuperer_data():
    success = False
    msg = ''
    data = request.json

    if not data:
        msg = 'Aucune donnée reçue'
        return success, msg, None

    MailDoc = data.get('mail_doc')
    if not MailDoc:
        msg = 'Mail du docteur est requis!'
        return success, msg, None

    Nompatient = data.get('nom_patient')
    if not Nompatient:
        msg = 'Nom du patient est requis!'
        return success, msg, None

    PrenomPatient = data.get('prenom_patient')
    if not PrenomPatient:
        msg = 'Prénom du patient est requis!'
        return success, msg, None

    DateHeure = data.get('DateHeure')
    if not DateHeure:
        msg = 'La date et l\'heure sont requises'
        return success, msg, None

    details = data.get('details') or ""


    success = True
    msg = 'Données récupérées avec succès'
    return success, msg, {
        'mail_doc': MailDoc,
        'nom_patient': Nompatient,
        'prenom_patient': PrenomPatient,
        'DateHeure': DateHeure,
        'details': details
    }
def Patient(conn: MySQLConnection, Nompatient: str, PrenomPatient: str, DateHeure: str):
    success = False
    MailPatient = ''
    msg = ''
    cursor = conn.cursor(buffered=True)

    try:
        cursor.execute("SELECT Mail FROM patient WHERE nom = %s AND prenom = %s", (Nompatient, PrenomPatient))
        result = cursor.fetchone()

        if not result:
            msg = 'Aucun patient trouvé'
            return success, msg, MailPatient

        MailPatient = result[0]


        # Vérification des rendez-vous du patient
        cursorcheck = conn.cursor(buffered=True)
        cursorcheckall = conn.cursor(buffered=True)
        cursorcheck.execute("SELECT * FROM appointment WHERE patient_mail = %s", (MailPatient,))
        rdv = cursorcheck.fetchone()  
        # Utiliser fetchall() pour récupérer toutes les lignes correspondantes
        cursorcheck.close()

        if not rdv:
            success = True
            msg = 'Aucun rendez-vous trouvé pour ce patient'
            return success, msg, MailPatient
        cursorcheckall.execute("SELECT * FROM appointment WHERE patient_mail = %s and appointment_date = %s", (MailPatient, DateHeure))
        rdvPatient = cursorcheckall.fetchall()

        # Si le patient a des rendez-vous
        for r in rdvPatient:
            if r[1] == MailPatient: 
                print(r[1]) # Si l'adresse e-mail du patient correspond à un rendez-vous
                msg = 'Le patient n\'est pas disponible à cette date'
                return success, msg, MailPatient
        
        success = True
        msg = 'Patient trouvé mais n\'a pas de rendez-vous à cette heure de cette date'

    except mysql.connector.Error as err:
        msg = f"Erreur de SELECT dans la table patient : {err}"
        return success, msg, MailPatient

    finally:
        cursor.close()  # S'assurer de fermer le curseur même en cas d'erreur

    return success, msg, MailPatient
def docteur(conn, MailDoc, DateHeure):
    nom_doc, prenom_doc = '', ''
    success = False
    cursorget = conn.cursor(buffered=True)
    cursorget.execute("SELECT name, prenom FROM docteur WHERE Mail = %s", (MailDoc,))
    doctor = cursorget.fetchone()
    cursorget.close()

    if not doctor:
        msg = 'Docteur non trouvé'
        return success, msg, nom_doc, prenom_doc

    nom_doc, prenom_doc = doctor
    cursorcheckdoc = conn.cursor(buffered=True)
    cursorcheckdoc.execute("SELECT nom_doc, prenom_doc FROM appointment WHERE appointment_date = %s", (DateHeure,))
    doc_rdv = cursorcheckdoc.fetchall()
    cursorcheckdoc.close()

    for d in doc_rdv:
        if nom_doc == d[0] and prenom_doc == d[1]:
            msg = 'Le docteur a un rendez-vous à cette heure de cette date'
            return success, msg, nom_doc, prenom_doc

    success = True
    msg = 'Docteur trouvé mais n\'a pas de rendez-vous à cette heure de cette date'
    return success, msg, nom_doc, prenom_doc

@app.route('/add_rdv', methods=['POST'])
def add_rdv():
    conn = None
    try:
        # Connexion à la base
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )

        # Récupération des données JSON via ta fonction helper
        success, msg, data = recuperer_data()
        if not success:
            return jsonify({'success': False, 'msg': msg})

        mail_doc = data['mail_doc']
        nom_patient = data['nom_patient']
        prenom_patient = data['prenom_patient']
        date_heure = data['DateHeure']
        details = data['details']

        # Vérification du patient
        success, msg, mail_patient = Patient(conn, nom_patient, prenom_patient, date_heure)
        if not success:
            return jsonify({'success': False, 'msg': msg})

        # Vérification du docteur
        success, msg, nom_doc, prenom_doc = docteur(conn, mail_doc, date_heure)
        if not success:
            return jsonify({'success': False, 'msg': msg})

        # Insertion du rendez-vous
        cursorAjout = conn.cursor(buffered=True)
        cursorAjout.execute(
            "INSERT INTO appointment (patient_mail, appointment_date, details, nom_doc, prenom_doc) VALUES (%s, %s, %s, %s, %s)",
            (mail_patient, date_heure, details, nom_doc, prenom_doc)
        )
        conn.commit()
        cursorAjout.close()

        return jsonify({'success': True, 'msg': 'Rendez-vous ajouté avec succès!'}), 201

    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

    finally:
        if conn:
            conn.close()



                        

                            
@app.route('/del_rdv', methods=['DELETE'])
def del_rdv():
    conn = None
    try:
        # Connexion base de données
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )

        # Récupération des données et verification patient via helper
        success, msg, data = recuperer_data()
        if not success:
            return jsonify({'success': False, 'msg': msg})

        mail_doc = data['mail_doc']
        nom_patient = data['nom_patient']
        prenom_patient = data['prenom_patient']
        date_heure = data['DateHeure']
        details = data['details']
        MailPatient = ""
        
        success, msg, MailPatient = Patient(conn, nom_patient, prenom_patient, date_heure)
        if ( not success  and msg == 'Aucun patient trouvé' ) :
            return jsonify({'success': False, 'msg': msg})
            
                

        # Si le patient est trouvé et disponible
        success, msg, nom_doc, prenom_doc = docteur(conn, mail_doc, date_heure)
        if (not success and msg =='Docteur non trouvé') or success :
            return jsonify({'success': False, 'msg': msg})

        # Vérification de l'existence du rendez-vous
        cursorCheck = conn.cursor(buffered=True)
        cursorCheck.execute("""
            SELECT * FROM appointment
            WHERE patient_mail = %s AND nom_doc = %s AND prenom_doc = %s AND appointment_date = %s
        """, (MailPatient, nom_doc, prenom_doc, date_heure))
        rdv = cursorCheck.fetchone()
        cursorCheck.close()

        if not rdv:
            return jsonify({'success': False, 'msg': 'Aucun rendez-vous trouvé à supprimer pour ce patient et ce docteur à cette date'})

        # Suppression du rendez-vous
        cursorDel = conn.cursor(buffered=True)
        cursorDel.execute("""
            DELETE FROM appointment
            WHERE patient_mail = %s AND nom_doc = %s AND prenom_doc = %s AND appointment_date = %s
        """, (MailPatient, nom_doc, prenom_doc, date_heure))
        conn.commit()
        cursorDel.close()

        return jsonify({'success': True, 'msg': 'Rendez-vous supprimé avec succès'})

    except Exception as e:
        # En cas d'erreur
        return jsonify({'success': False, 'msg': str(e)})

    finally:
        if conn:
            conn.close()

from datetime import datetime
'''@app.route('/get_rdv', methods=['POST'])


def get_rdv():
    data = request.json or {}

    mail_doc = data.get('Mail', '').strip()
    if not mail_doc:
        return jsonify({"success": False, "msg": "no mail_doc given"})

    # Connect to DB
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )
    except Exception as e:
        return jsonify({"success": False, "msg": f"Database connection failed: {str(e)}"})

    try:
        cursorget = conn.cursor(buffered=True)
        cursorget.execute("SELECT name, prenom FROM docteur WHERE Mail = %s", (mail_doc,))
        doctor = cursorget.fetchone()
        cursorget.close()

        if not doctor:
            return jsonify({"success": False, "msg": "Docteur non trouvé"})

        nom_doc, prenom_doc = doctor

        filters = ["a.nom_doc = %s", "a.prenom_doc = %s"]
        values = [nom_doc, prenom_doc]

        # Optional filters
        nom_patient = data.get('nom_patient', '').strip()
        prenom_patient = data.get('prenom_patient', '').strip()
        dateheure = data.get('dateheure', '').strip()
        start_of_day = f"{dateheure} 00:00:00"
        end_of_day = f"{dateheure} 23:59:59"


        if nom_patient:
            if prenom_patient:
                sqlOnepatient = "Select Mail from patient where nom = %s and prenom = %s"
                cursorOnepatient = conn.cursor(buffered=True)
                
                cursorOnepatient.execute(sqlOnepatient, (nom_patient, prenom_patient))
                one_patient = cursorOnepatient.fetchone()
                cursorOnepatient.close()
                if one_patient:
                    filters.append("p.Mail = %s")
                    values.append(one_patient[0])
                else:
                    return {"success": False, "msg": "Aucun patient n a comme nom = " + nom_patient + " ET prenom = " + prenom_patient}
            sqlPatient = "SELECT Mail FROM patient WHERE nom = %s"
            cursorPatient = conn.cursor(buffered=True)
            cursorPatient.execute(sqlPatient, (nom_patient,))
            patients = cursorPatient.fetchall()
            cursorPatient.close()
            if patients:
                for p in patients:

                    filters.append("p.Mail = %s")
                    values.append(p[0])
        if prenom_patient:
            sqlPatient = "SELECT Mail FROM patient WHERE prenom = %s"
            cursorPrenomPatient = conn.cursor(buffered=True)
            cursorPrenomPatient.execute(sqlPatient, (prenom_patient,))
            prenom_patient_mail = cursorPrenomPatient.fetchone()
            cursorPrenomPatient.close()
            if prenom_patient_mail:
                filters.append("p.Mail = %s")
                values.append(prenom_patient_mail[0])
        if dateheure:
            filters.append("a.appointment_date = %s")
            values.append(dateheure)

        sql = """
        SELECT 
        a.id, 
        a.appointment_date, 
        a.details, 
        a.nom_doc, 
        a.prenom_doc, 
        p.nom AS nom_patient, 
        p.prenom AS prenom_patient
        FROM appointment a
            JOIN patient p ON a.patient_mail = p.Mail
            WHERE a.appointment_date >= %s AND a.appointment_date < %s
"""
        if filters:
            sql +=  + " AND ".join(filters)

        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, start_of_day, end_of_day, values)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "msg": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
        

'''



@app.route('/get_rdv', methods=['POST'])

def get_rdv():
    data = request.json or {}

    mail_doc = data.get('Mail', '').strip()
    if not mail_doc:
        return jsonify({"success": False, "msg": "no mail_doc given"})

    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )
    except Exception as e:
        return jsonify({"success": False, "msg": f"Database connection failed: {str(e)}"})

    try:
        cursorget = conn.cursor(buffered=True)
        cursorget.execute("SELECT name, prenom FROM docteur WHERE Mail = %s", (mail_doc,))
        doctor = cursorget.fetchone()
        cursorget.close()

        if not doctor:
            return jsonify({"success": False, "msg": "Docteur non trouvé"})

        nom_doc, prenom_doc = doctor

        filters = ["a.nom_doc = %s", "a.prenom_doc = %s"]
        values = [nom_doc, prenom_doc]

        # Date filtering
        date_str = data.get('dateheure', '').strip()
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({"success": False, "msg": "Format de date invalide. Utilisez YYYY-MM-DD HH:MM:SS"})

            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            filters.append("a.appointment_date >= %s AND a.appointment_date < %s")
            values.append(start_of_day.strftime('%Y-%m-%d %H:%M:%S'))
            values.append(end_of_day.strftime('%Y-%m-%d %H:%M:%S'))

        # Build final SQL
        sql = """
        SELECT 
            a.id, 
            a.appointment_date, 
            a.details, 
            a.nom_doc, 
            a.prenom_doc, 
            p.nom AS nom_patient, 
            p.prenom AS prenom_patient
        FROM appointment a
            JOIN patient p ON a.patient_mail = p.Mail
        """
        if filters:
            sql += " WHERE " + " AND ".join(filters)

        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, tuple(values))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if date_str:
            for r in results:
               if isinstance(r['appointment_date'], datetime):
                   r['appointment_time'] = r['appointment_date'].strftime('%H:%M:%S')

        return jsonify({"success": True, "msg": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



@app.route('/modif_rdv', methods=['PUT'])
def modif_rdv():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='istic.glsi3',
            database='monpfe'
        )
        data = request.json

        # Récupérer et valider les données
        success, msg, donn = recuperer_data()
        if not success:
            return jsonify({'success': False, 'msg': msg})

        mail_doc = donn['mail_doc']
        nom = donn['nom_patient']
        prenom = donn['prenom_patient']

        new_nom = data.get('newnom_patient') or ''
        new_prenom = data.get('newprenom_patient') or ''
        new_date = data.get('new_dateTime') or ''
       
        ancienne_date = donn.get('DateHeure')


        if ((new_nom != '' and new_prenom == '') or (new_nom == '' and new_prenom != '')):
            return jsonify({'success': False, 'msg': 'Un patient a besoin de nom ET prénom '})
        #chercher l'ancien patient 
        sqlancien = " SELECT MAIL from patient where nom = %s and prenom = %s"
        cursorancien = conn.cursor()
        cursorancien.execute(sqlancien,(nom,prenom,))
        mail_patient = cursorancien.fetchone()
        if not mail_patient:
            return jsonify({"success": False,"msg " : "patient pas trouvé "})
        cursorancien.close()
        mail_patient = mail_patient[0]

        # Vérifier le docteur
        success, msg, nom_doc, prenom_doc = docteur(conn, mail_doc, ancienne_date)
        if not success and msg == 'Docteur non trouvé':
            return jsonify({'success': False, 'msg': msg})
       

        # Vérifier le nouveau patient
        if new_nom != nom and new_prenom != prenom:
            # medecin change le nom et prenom du patient ayant le rendez-vous
           # success, msg, mail_patient = Patient(conn, nom, prenom, ancienne_date)
            if new_date != ancienne_date:
                # envoie aussi une nouvelle date et heure 
                success, msg, new_mail_patient = Patient(conn, new_nom, new_prenom, new_date)
                if not success:
                    if msg == 'Aucun patient trouvé':
                        return jsonify({'success': False, 'msg': msg})
                    elif msg == "Le patient n'est pas disponible à cette date":
                        return jsonify({'success': False, 'msg': msg})
                else:
                    # vérifier si le médecin est libre dans la date et heure saisis 
                    success, msg, nom_doc, prenom_doc = docteur(conn, mail_doc, new_date)
                    if not success:
                        return jsonify({'success': False, 'msg': msg})
                        # if success , le docteur est trouvé et n'a pas de rendez-vous à cette heure 

                    cursorUpdate = conn.cursor(buffered=True)
                    sqlUpdate = "UPDATE appointment SET patient_mail = %s, appointment_date = %s WHERE patient_mail = %s AND appointment_date = %s;"
                    cursorUpdate.execute(sqlUpdate, (new_mail_patient, new_date, mail_patient, ancienne_date))
                    conn.commit()
                    cursorUpdate.close()
            else:
                # si le médecin n’a pas envoyé une nouvelle date 
                success, msg, new_mail_patient = Patient(conn, new_nom, new_prenom, ancienne_date)
                print("patient_mail est " + mail_patient)
                if not success:
                    return jsonify({'success': False, 'msg': msg})
                cursorUpdate = conn.cursor(buffered=True)
                sqlUpdate = "UPDATE appointment SET patient_mail = %s WHERE patient_mail = %s AND appointment_date = %s;"
                cursorUpdate.execute(sqlUpdate, (new_mail_patient, mail_patient, ancienne_date))
                conn.commit()
                cursorUpdate.close()
        else:
            # si le docteur n’a pas saisi un nouveau nom et un nouveau prénom
           
            if not success:
                return jsonify({'success': False, 'msg': msg})
            success, msg, nom_doc, prenom_doc = docteur(conn, mail_doc, new_date)
            if not success:
                return jsonify({'success': False, 'msg': msg})
            # if success, Docteur trouvé mais n'a pas de rendez-vous à cette heure de cette date
            cursorUpdate = conn.cursor(buffered=True)
            sqlUpdate = "UPDATE appointment SET appointment_date = %s WHERE patient_mail = %s AND appointment_date = %s;"
            cursorUpdate.execute(sqlUpdate, (new_date, mail_patient, ancienne_date))
            conn.commit()
            
            cursorUpdate.close()

        return jsonify({'success': True, 'msg': f"Rendez-vous modifié avec succès newdate : {new_date} old_date : {ancienne_date}"})
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

