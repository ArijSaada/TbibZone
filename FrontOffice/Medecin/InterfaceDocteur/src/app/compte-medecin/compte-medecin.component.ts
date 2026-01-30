import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { LocalisationMedComponent } from '../localisation-med/localisation-med.component';
import { CalendarComponent } from '../calendar-component/calendar-component.component';
import { CalendarServiceService } from '../calendar-component/calendar-service.service';
import Fuse from 'fuse.js';
import { CalendarEvent } from 'angular-calendar';

@Component({
  selector: 'app-compte-medecin',
  standalone: false,
  templateUrl: './compte-medecin.component.html',
  styleUrls: ['./compte-medecin.component.css'],
  providers: [LocalisationMedComponent]
})
export class CompteMedecinComponent implements OnInit {
  emailMedecin: string = '';
  rdvs: any[] = [];
  Mail = '';
  fuse!: Fuse<CalendarEvent>;
  now: Date = new Date();
  filters: { [key: string]: string } = {};
  ChosenDay: Date = new Date();
  selectedYear: number = new Date().getFullYear();
  selectedMonth: number = new Date().getMonth(); 
  SelectedDay: number = new Date().getDate();

  viewDate: Date = new Date(); 

  constructor(
    private router: Router,
    private activRoute: ActivatedRoute,
    private service: CalendarServiceService
  ) {}

  ngOnInit() {
    this.activRoute.queryParamMap.subscribe(params => {
      this.Mail = params.get('mail') || '';
      if (this.Mail == '') {
        alert('pas de mail dans ts code');
      } else {
        alert('Mail trouvé: ' + this.Mail);
      }

      this.filters = { 'Mail': this.Mail };
      //alert("filters ")
      //alert(JSON.stringify(this.filters))
      
    });
    
    this.onDateChosen();
    
  }

  onDateChosen() {
    const yyyy = this.ChosenDay.getFullYear();
    const mm = String(this.ChosenDay.getMonth() + 1).padStart(2, '0');
    const dd = String(this.ChosenDay.getDate()).padStart(2, '0');
    const hh = String(this.ChosenDay.getHours()).padStart(2, '0');
    const min = String(this.ChosenDay.getMinutes()).padStart(2, '0');
    const ss = String(this.ChosenDay.getSeconds()).padStart(2, '0');

  
    // Format the date with time (YYYY-MM-DD HH:MM:SS)
    this.filters['dateheure'] = `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
    alert(`Date et heure choisies : ${this.filters['dateheure']}`);
    alert(typeof this.filters['dateheure']);

    // Log to check if the format is correct
    console.log('Formatted date with time:', this.filters['dateheure']);
    
    // Now call the function to get the appointments
    this.get_rdv();
  }

  get_rdv() {
    this.service.get_rdv(this.filters).subscribe({
      next: (response: any) => {
        if (!response.success) {
          console.error('Erreur API:', response.msg);
          alert('Erreur : ' + response.msg);
          return;
        }

        this.rdvs = Array.isArray(response.msg)
          ? response.msg.map((rdv: any) => ({
              start: new Date(rdv.appointment_date),
              title: `${rdv.nom_patient} ${rdv.prenom_patient} ${rdv.appointment_time}`,
              meta: rdv
            }))
          : [];

        console.log(this.rdvs);

        this.fuse = new Fuse(this.rdvs, {
          keys: ['title', 'nom_patient', 'prenom_patient', 'nom_doc', 'prenom_doc'],
          threshold: 0.4
        });
      },
      error: (err) => {
        console.error('Erreur HTTP:', err.message);
        alert('Erreur réseau ou serveur');
      }
    });
  }

  navigateTocalendar() {
    this.activRoute.queryParamMap.subscribe(params => {
      this.emailMedecin = params.get('mail') || '';
      if (this.emailMedecin == '') {
        alert('Email is required');
      } else {
        this.router.navigate(['GestionRdv'], { queryParams: { mail: this.emailMedecin } });
      }
    });
  }

  changelocation() {
    this.router.navigate(['localisation'], { queryParams: { mail: this.Mail } });
  }
}
