import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CalendarServiceService } from '../calendar-component/calendar-service.service';

@Component({
  selector: 'app-modifier-rdv',
  standalone: false,
  templateUrl: './modifier-rdv.component.html',
  styleUrl: './modifier-rdv.component.css'
})
export class ModifierRdvComponent implements OnInit{
  mail_doc: string = '';
  nom_patient: string = '';
  prenom_patient: string = '';
  DateHeure: string = '';
  details: string = '';
  constructor(private activ: ActivatedRoute, private service : CalendarServiceService) {
    this.activ.queryParams.subscribe(params => {
      this.mail_doc = params['mail_doc'];
      this.nom_patient = params['nom_patient'];
      this.prenom_patient = params['prenom_patient'];
      this.DateHeure = params['DateHeure'];
      
    });
if(!this.mail_doc || !this.nom_patient || !this.prenom_patient || !this.DateHeure ) {
      alert('Erreur: Paramètres manquants dans l\'URL');
      if (!this.mail_doc) {
        alert('le ts code de modifier n a pas recu le mail_doc')
      }
      if(! this.nom_patient) {
        alert('le ts code de modifier n a pas recu le nom_patient')
      }
      if(! this.prenom_patient) {
        alert('le ts code de modifier n a pas recu le prenom_patient')
      }
      if(! this.DateHeure) {
        alert('le ts code de modifier n a pas recu le DateHeure')
      }
      
    }

  }

  ngOnInit(): void {
    // You can perform additional initialization here
  }
  formatDateToSQL(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // month is 0-indexed
  const day = String(date.getDate()).padStart(2, '0');

  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
Inputnom : string = '';
Inputprenom : string = '';
inputDateTime : string ='';

  ModifierRdv() {
    const newnom_patient = this.Inputnom;
    const newprenom_patient = this.Inputprenom;
  
    const newdetails = this.details;
    const new_dateTime = new  Date(this.inputDateTime);
  const formattedDate = this.formatDateToSQL(new_dateTime);
  alert("ancien nom_patient" + this.nom_patient)
  alert('DateHeure recu ' + this.formatDateToSQL(new Date(this.DateHeure)))
  alert('new_dateTime: ' + new_dateTime);
  alert('newnom' + newnom_patient)
  
  const appointmentData = {
      mail_doc: this.mail_doc,
      nom_patient: this.nom_patient,
      prenom_patient: this.prenom_patient,
      DateHeure: this.formatDateToSQL(new Date(this.DateHeure)),

    

      newnom_patient: newnom_patient,
      newprenom_patient: newprenom_patient,
      new_dateTime : this.formatDateToSQL(new Date(this.inputDateTime)),
      newDetails: newdetails
    };
    console.log(appointmentData);
    this.service.ModifierRdv(appointmentData).subscribe({
      next: (response) => {
        if (response.success) {
          alert('Rendez-vous modifié avec succès');
          window.location.reload();
        } else {
          alert(response.msg);
        }
      },
      error: (error) => {
        console.error('Erreur lors de la modification du rendez-vous:', error);
        alert(error.message);
      }
    });
  }
  
  


}
