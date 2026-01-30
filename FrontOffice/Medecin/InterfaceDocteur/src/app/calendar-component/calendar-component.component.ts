import { Component ,  ChangeDetectorRef, NgZone, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import Fuse from 'fuse.js';
import { CalendarServiceService } from './calendar-service.service';
import {
  CalendarEvent,
  CalendarMonthViewDay,
  
  CalendarView,
} from 'angular-calendar';
import { ActivatedRoute, Router } from '@angular/router';
import { delay } from 'rxjs';



@Component({
  selector: 'app-calendar',
  standalone:false,
  templateUrl: './calendar-component.component.html',
  styleUrls: ['./calendar-component.component.css'],

})

export class CalendarComponent implements OnInit{

 
  view: CalendarView = CalendarView.Month; 

  viewDate: Date = new Date(); 
  pressed : boolean = false;
  //selectedDate : Int16Array;
  clickedDate: Date = new Date();
searching : boolean = false;
newEventTime: Date = new Date();
showInlineInput: boolean = false;
newEventDate : String='';
add : boolean = false;
titre : string = "";
modifier : boolean = false;


  fuse!: Fuse<CalendarEvent>;
  
  SelectedDay: number = this.viewDate.getDate();
  
days  = [1 , 2 , 3 , 4 , 5, 6 , 7 ,8 ,9 , 10, 11 , 12, 13, 14 ,15 , 16 , 17 ,18 ,19 ,20 ,21, 22, 23, 24, 25, 26 ,27, 28, 29 ,30 , 31]

  
 
events: any[] = [];
 
  months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ];
  Mail ='';
  chercherPatient: any[] = [];

filters: { [key: string]: string } = {};

constructor(private service: CalendarServiceService, private route: ActivatedRoute,private cd: ChangeDetectorRef,private router: Router) {

}

ngOnInit() {
    this.route.queryParams.subscribe(params => {
    this.Mail = params['mail'] || '';
    if(this.Mail == ''){
        alert('pas de mail dans ts code')
    }
    else {alert('Mail trouvé: ' + this.Mail);}
    this.filters = { 'Mail': this.Mail };
    this.get_rdv();

    // Now call get_rdv only after mail_doc is set
    
  });
  this.fuse = new Fuse(this.events, {
    keys: ['title'],
    threshold: 0.4 
  });
  this.applyFilters();

  
  
  
}
  nom_Patient = '';
  prenom_Patient = '';
  nom_doc ='';
  prenom_doc = '';
  
 

  applyFilters() {
    



    // Add filters to the object only if they are provided
    if (this.nom_Patient) this.filters['nom_patient'] = this.nom_Patient;
    if (this.prenom_Patient) this.filters['prenom_patient'] = this.prenom_Patient;
  

    // Call the method to load the appointments with applied filters
   // this.get_rdv();
  }
  gmtDate  = new Date()

  // Get appointments, either with or without filters
  get_rdv() {
    this.service.get_rdv(this.filters).subscribe({
      next: (response: any) => {
        if (!response.success) {
          console.error('Erreur API:', response.msg);
          alert('Erreur : ' + response.msg); // or show in UI
          return;
        }
        this.events = Array.isArray(response.msg)
          ? response.msg.map((rdv: any) => {
              const gmtDate = new Date(rdv.appointment_date);

      // DEBUG: log the full ISO and the GMT time string
      console.log("Raw date:", rdv.appointment_date);
      console.log("Parsed GMT Date:", gmtDate.toISOString());

      // : Use full ISO string (recommended for most calendars)
     /* const startDate = gmtDate.toISOString();
       const start = new Date(gmtDate.getUTCFullYear(), gmtDate.getUTCMonth(), gmtDate.getUTCDate(),
          gmtDate.getUTCHours(), gmtDate.getUTCMinutes(), gmtDate.getUTCSeconds());
         const end = new Date(start.getTime() + 30 * 60000);
        this.gmtDate = start;
*/
      return {
        ...rdv,
        start: new Date(rdv.appointment_date.replace(" ", "T")), // Convert to Date object
        end: new Date(new Date(rdv.appointment_date.replace(" ", "T")).getTime() + 30 * 60000), // Add 30 minutes
        title: `${rdv.nom_patient}, ${rdv.prenom_patient}`,
        nom_patient: rdv.nom_patient,
        prenom_patient: rdv.prenom_patient,
        nom_doc: rdv.nom_doc,
        prenom_doc: rdv.prenom_doc
      };
    })
  : [];


    
  
  
        //this.events = Array.isArray(response.msg) ? response.msg : [];
        this.chercherPatient = this.events;
  
        this.fuse = new Fuse(this.events, {
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

  onSearchInput(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    const value = inputElement.value;
    this.onSearch(value);
  }
GererEvent(event: { date: Date }): void {
  this.pressed = true;
  

  const clickedDate: Date = event.date;


  this.clickedDate = new Date(clickedDate); // <== this is missing

  const hours = clickedDate.getHours();
  const minutes = clickedDate.getMinutes();
  this.newEventTime = new Date(clickedDate.setHours(hours, minutes));
 
}
  GererEventExisting({ event }: { event: CalendarEvent }): void {
    
    this.datehasevent = true;
    
    this.titre = event.title;
    this.newEventTime = new Date(event.start);
    this.newEventDate = this.formatDateToSQL(this.newEventTime);
    this.pressed = true;
    this.showInlineInput = true;
  }
  datehasevent : boolean = false;



  
  
  
  onSearch(term: string) {
    if (term.trim() === '') {
      this.chercherPatient = [];
      this.viewDate = new Date();
      console.log("Pas de filtre")
    } else {
      this.searching = true;
      console.log(`looking for ${term}`)
      this.chercherPatient = this.events.filter(event =>
        event.title.toLowerCase().includes(term.toLowerCase()));
    }
    if (this.chercherPatient.length > 0) {
      this.viewDate = this.chercherPatient[0].start;
    }
  }

  years: number[] = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - 5 + i);

  selectedMonth = this.viewDate.getMonth();
  selectedYear = this.viewDate.getFullYear();
  ChosenDay = new Date(this.selectedYear, this.selectedMonth, this.SelectedDay);
  
  updateViewDate() {
    this.onDateChosen();
    this.viewDate = new Date(this.selectedYear, this.selectedMonth, 1);
  }


  // Custom function name (for handling the dayClicked event)
  onDatedClicked(event: any) {
  this.clickedDate = event.day.date;
  this.pressed = true;
  this.showInlineInput = false;

  if (this.view === CalendarView.Month) {
    alert('Please click on the "Week" view to see the appointments for this day.');
  }

  const clickedDateStr = this.clickedDate.toDateString();
  const eventsForClickedDate = this.events.filter(ev =>
    ev.start.toDateString() === clickedDateStr
  );

  console.log(`Day selected: ${clickedDateStr}`);
  console.log('Events for the clicked date:', eventsForClickedDate);

  if (this.newEventTime) {
    alert
    const time = new Date(this.newEventTime);
    console.log('Time selected:', time);
    
    const combinedDateTime = new Date(
      this.clickedDate.getFullYear(),
      this.clickedDate.getMonth(),
      this.clickedDate.getDate(),
      time.getHours(),
      time.getMinutes(),
      
    );

    // Use this datetime when creating or sending the event
    this.newEventDate = this.formatDateToSQL(combinedDateTime);
    this.newEventTime = combinedDateTime; // optionally store it for later
    console.log('New combined event time:', this.newEventDate);
  } else {
    console.warn("Time not selected yet. Waiting for user input.");
  }
}

  onDateChosen() {
    
    //const monthIndex  = this.months.indexOf((this.selectedMonth));
     this.ChosenDay = new Date(this.selectedYear, this.selectedMonth, this.SelectedDay);
    
    this.viewDate = this.ChosenDay;
    console.log('Date chosen:', this.ChosenDay);
    
  }
  isChosen(day: Date): boolean {
    
    return this.ChosenDay.getDay() === day.getDay() &&
           this.ChosenDay.getMonth() === day.getMonth() &&
           this.ChosenDay.getFullYear() === day.getFullYear();
  }


  cancel() {
    this.showInlineInput = false;
    this .pressed = false;
    window.location.reload();

    
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


  add_rdv(){
    alert('le clickedday est : ' + this.clickedDate);

    const patient = this.titre?.trim()||'';
    if (!patient){
      alert('Veuillez entrer le nom  et prénom du patient');
      return;
    }
    if (patient.includes(',') === false){
      alert('Veuillez entrer le nom et prénom du patient au format "Nom, Prénom"');
      return;

    }
    const maildoc = this.Mail;
    alert('le mail est : ' + maildoc);
    const nom_patient = patient.split(',')[0].trim();
    const prenom_patient = patient.split(',')[1].trim();
    alert('le nom est : ' + nom_patient);
    alert('le prenom est : ' + prenom_patient);
    const appointmentData = {
      mail_doc: maildoc,
      nom_patient: nom_patient,
      prenom_patient: prenom_patient,
      DateHeure: this.formatDateToSQL(this.clickedDate),
     
    };

    this.service.add_rdv(appointmentData).subscribe({
      next: (response) => {
        if (response.success) {
          alert('Rendez-vous ajouté avec succès');
          window.location.reload();
        } else {
          alert(response.msg);
        }
      },
      error: (error) => {
        console.error('Erreur lors de l\'ajout du rendez-vous:', error);
        alert(error.message);
      }
    });
  }
  del_rdv(){

   const dateheure = new Date((this.newEventDate).replace(" ", "T"));
    alert('le clickedday est : ' + dateheure);
    


    const patient = this.titre?.trim()||'';
    if (!patient){
      alert('Veuillez entrer le nom  et prénom du patient');
      return;
    }
    if (patient.includes(',') === false){
      alert('Veuillez entrer le nom et prénom du patient au format "Nom, Prénom"');
      return;

    }

    const appointmentData = {
      mail_doc: this.Mail,
      nom_patient: patient.split(',')[0].trim(),
      prenom_patient: patient.split(',')[1].trim(),
      DateHeure: this.formatDateToSQL(dateheure),
     
    };
    alert ("date a supprim " + appointmentData['DateHeure'])

    this.service.del_rdv(appointmentData).subscribe({
      next: (response) => {
        if (response.success) {
          alert('Rendez-vous supprimé avec succès');
          window.location.reload();
        } else {
          alert(response.msg);
        }
      },
      error: (error) => {
        console.error('Erreur lors de la suppression du rendez-vous:', error);
        alert(error.message);
      }
    });
  }

  modif : boolean = false;
  
ModifierRdv() {
  const dateheure = new Date(this.newEventDate.replace(" ", "T")); // Input is string → Date
  const gmtDateString = dateheure.toISOString(); 
  this.gmtDate = new Date(gmtDateString);// Correct usage to get GMT format (ISO 8601 string)

  if (!confirm('Are you sure ?')) {
    return;
  }

  const patient = this.titre?.trim() || '';
  if (!patient) {
    alert('Veuillez entrer le nom  et prénom du patient');
    return;
  }

  if (!patient.includes(',')) {
    alert('Veuillez entrer le nom et prénom du patient au format "Nom, Prénom"');
    return;
  }

  const nom_Patient = patient.split(',')[0].trim();
  const prenom_Patient = patient.split(',')[1].trim();

  alert('Le clicked day est : ' + this.newEventDate);
  alert('GMT ISO string : ' + gmtDateString);

  // Optional: if backend requires a specific SQL format, e.g. "YYYY-MM-DD HH:mm:ss"
  const formattedDate = this.formatDateToSQL(dateheure); 
  alert('Date formatée pour SQL : ' + formattedDate);

  // Send the correctly formatted GMT time in query params
  this.router.navigate(['edit-rdv'], {
    queryParams: {
      mail_doc: this.Mail,
      nom_patient: nom_Patient,
      prenom_patient: prenom_Patient,
      DateHeure: this.formatDateToSQL(this.gmtDate)
    }
  });
}


  CalendarView = CalendarView; 

}

  

  