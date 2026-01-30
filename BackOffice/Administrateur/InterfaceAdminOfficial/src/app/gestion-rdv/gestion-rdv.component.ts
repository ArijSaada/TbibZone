import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import Fuse from 'fuse.js';
import { CalendarView } from 'angular-calendar';
import { CalendarModule, CalendarDateFormatter } from 'angular-calendar';

import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';

import { Router } from '@angular/router';
import {gestionRdvService} from './gestionService.service';
import { CalendarEvent } from 'angular-calendar';

@Component({
  selector: 'app-gestion-rdv',
  standalone: false,
  templateUrl: './gestion-rdv.component.html',
  styleUrl: './gestion-rdv.component.css'
})
export class GestionRdvComponent implements OnInit {
   CalendarView = CalendarView;
   events: CalendarEvent[] = [];


  appointment : any = {
    id : '',
    nom_doc:'',
    prenom_doc : '',
    nom_patient : '',
    prenom_patient : '',
    appointment_date : '',


  }

  
  nom_doc: string = '';
  prenom_doc: string = '';
  nom_patient: string = '';
  prenom_patient: string = '';
  appointment_date: string = '';
  viewDate: Date = new Date();
  selectedDay: number = this.viewDate.getDate();
  clickedDate: Date = new Date();
  pressed: boolean = false;
  showInlineInput: boolean = false;
  newEventDate: string = this.formatDateToSQL(new Date());
  newEventTime: string | null = null;
  datehasevent : boolean = false;
 
  rdvs: any[] = [];
 
   searchTerm: string = '';
   ToAdjustrdv: boolean = false;
   
years: number[] = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - 5 + i);

  selectedMonth = this.viewDate.getMonth();
  selectedYear = this.viewDate.getFullYear();
  ChosenDay = new Date(this.selectedYear, this.selectedMonth, this.selectedDay);
  view: CalendarView = CalendarView.Month; 

 
  months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ];
 days  = [1 , 2 , 3 , 4 , 5, 6 , 7 ,8 ,9 , 10, 11 , 12, 13, 14 ,15 , 16 , 17 ,18 ,19 ,20 ,21, 22, 23, 24, 25, 26 ,27, 28, 29 ,30 , 31];

  
  
  updateViewDate() {
    this.onDateChosen();
    this.viewDate = new Date(this.selectedYear, this.selectedMonth, 1);
  }


  // Custom function name (for handling the dayClicked event)
  onDatedClicked(event: any) {
  this.clickedDate = event.day.date;
  this.pressed = true;
  this.showInlineInput = false;

  // Replace CalendarView.Month with the string 'month' or your actual month view identifier
  if (this.view === 'month') {
    alert('Please click on the "Week" view to see the appointments for this day.');
  }
  const clickedDateStr = this.clickedDate.toDateString();
  const eventsForClickedDate = this.events.filter((ev: { start: { toDateString: () => string; }; }) =>
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
    this.newEventDate = this.formatDateToSQL(combinedDateTime);
    //this.newEventTime = combinedDateTime; // optionally store it for later
    console.log('New combined event time:', this.newEventDate);
  } else {
    console.warn("Time not selected yet. Waiting for user input.");
  }
  
  }
  onDateChosen() {
    
    //const monthIndex  = this.months.indexOf((this.selectedMonth));
     this.ChosenDay = new Date(this.selectedYear, this.selectedMonth, this.selectedDay);
    
    this.viewDate = this.ChosenDay;
    console.log('Date chosen:', this.ChosenDay);
    
  }
  isChosen(day: Date): boolean {
    
    return this.ChosenDay.getDay() === day.getDay() &&
           this.ChosenDay.getMonth() === day.getMonth() &&
           this.ChosenDay.getFullYear() === day.getFullYear();
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

  constructor(private router: Router, private service: gestionRdvService , private cdr : ChangeDetectorRef) {
    this.ToAdjustrdv = false;
   }

   ngOnInit() {
      this.Get_rdv();
   }

  Get_rdv() {
  console.log('Fetching rdvs...');
  this.service.get_rdv().subscribe({
    next: (response) => {
      this.rdvs = response.msg;
      this.events = this.rdvs.map((rdv: any) => ({
        start: new Date(rdv.appointment_date),
        title: `Dr. ${rdv.nom_doc} ${rdv.prenom_doc} - Patient: ${rdv.nom_patient} ${rdv.prenom_patient}`,
        allDay: false,
        color: {
          primary: '#ad2121',
          secondary: '#FAE3E3'
        },
        meta: rdv
      }))
      console.log('Events:', this.events); // Check if events are properly formatted
    },
    error: (error) => {
      console.error('Error fetching rdvs:', error);
    }
  });
}
   
   Adjustrdv(appointment: any) {
    this.ToAdjustrdv = true;
    this.appointment = appointment ;
    this.nom_doc = appointment.nom_doc;
    this.prenom_doc = appointment.prenom_doc;
    this.nom_patient = appointment.nom_patient;
    this.prenom_patient = appointment.prenom_patient;
    this.appointment_date = appointment.appointment_date;
   
   
    console.log('appointment to adjust:', appointment);
    console.log('appointment details:', this.nom_doc, this.prenom_doc, this.nom_doc, this.prenom_doc, this.appointment_date);
    

   }
   modifier: boolean = false;
   newnom_doc: string = '';
   newprenom_doc: string = '';
   newnom_patient : string = '';
   newprenom_patient : string = '';
 

   Update_rdv() {
    this.appointment = {
      nom_doc : this.appointment.nom_doc,
      prenom_doc : this.appointment.prenom_doc,
      nom_patient : this.appointment.nom_patient,
      prenom_patient : this.appointment.prenom_patient,
      appointment_date : this.appointment.appointment_date,

    }
    this.modifier = true;
    
  
  }
  SubmitModifier() {
  const updateData = {
    nom_doc: this.appointment.nom_doc,
    prenom_doc: this.appointment.prenom_doc,
    nom_patient: this.appointment.nom_patient,
    prenom_patient: this.appointment.prenom_patient,
    appointment_date: this.appointment.appointment_date,

    new_nom_doc: this.newnom_doc,
    new_prenom_doc: this.newprenom_doc,
    new_nom_patient: this.newnom_patient,
    new_prenom_patient: this.newprenom_patient,
    new_datetime: this.appointment_date,
  };
  alert(updateData.prenom_patient)

  const newAppointment = {
    nom_doc: this.newnom_doc,
    prenom_doc: this.newprenom_doc,
    nom_patient: this.newnom_patient,
    prenom_patient: this.newprenom_patient,
    appointment_date: this.appointment_date,
  };

  this.service.Modifier_rdv(updateData, newAppointment).subscribe({
    next: (response) => {
      if (response.success) {
        alert('Appointment updated successfully: ' + response.msg);
        this.modifier = false;
      } else {
        alert('Error updating appointment: ' + response.msg);
      }
      this.Get_rdv(); // Refresh the list after update
    },
    error: (error) => {
      console.error('Error updating appointment:', error);
    }
  });
}

   Delete_rdv() {
    
    alert('Deleting appointment');
    this.service.del_rdv(this.appointment).subscribe({
      next: (response) => {
        if (response.success) {
          alert('appointment deleted successfully:' + response.msg);
        }
        else {
          alert('Error deleting appointment:' + response.msg);
        }
        this.Get_rdv(); // Refresh the list after deletion
      },
      error: (error) => {
          alert('Error deleting appointment:' + error);
      }
    });

   }
   add_rdv() {
    
    if (this.newEventTime) {
     const [hours, minutes] = this.newEventTime.split(':').map(Number);

      const date = new Date(this.clickedDate);


      
      
      
      
      const combinedDateTime = new Date(
        this.clickedDate.getFullYear(),
        this.clickedDate.getMonth(),
        this.clickedDate.getDate(),
        hours,
        minutes,
      );
       alert(this.formatDateToSQL(combinedDateTime))
      // Use combinedDateTime as needed
    


    alert('Adding new appointment:' + this.appointment.nom_doc + ' ' + this.appointment.prenom_doc + ' ' + this.appointment.nom_patient + ' ' + this.appointment.prenom_patient + ' ' + this.appointment.appointment_date);
    this.appointment = {
      nom_doc: this.nom_doc,
      prenom_doc: this.prenom_doc,
      nom_patient: this.nom_patient,
      prenom_patient: this.prenom_patient,  
      appointment_date: this.formatDateToSQL(combinedDateTime)
     
    };

    this.service.add_rdv(this.appointment).subscribe({
      next: (response) => { 
        if (response.success) {
          alert('appointment added successfully:' + response.msg);
        }
        else {
          alert('Error adding appointment:' + response.msg);
        }
        this.Get_rdv(); // Refresh the list after adding
      },
      error: (error) => {   
        console.error('Error adding appointment:', error);
      }
    });
     // Logic to add a new appointment
    } else {
      console.error('newEventTime is null');
      return;
    }
   
    }
  
  onSearchInput(searchTerm: string): void {
    if (searchTerm) {
      alert(searchTerm)
      this.service.searchRdvs(searchTerm).subscribe({
        next: (response) => {
          this.rdvs = response.msg;
          
          this.cdr.detectChanges();

          console.log('Filtered rdvs:', this.rdvs);
        },
        error: (error) => {
          console.error('Error searching rdvs:', error);
        }
      });
    } else {
      // Reset the list if search term is empty
      this.Get_rdv();
    }
  }
  GererEvent(event: any): void {
  this.pressed = true;
  

  const clickedDate: Date = event.date;


  this.clickedDate = new Date(clickedDate); // <== this is missing

  const hours = clickedDate.getHours();
  const minutes = clickedDate.getMinutes();
 // this.newEventTime = new Date(clickedDate.setHours(hours, minutes));
 
}
  

GererEventExisting({ event }: { event: CalendarEvent }): void {
  this.datehasevent = true;
  this.clickedDate = event.start;
  this.appointment = event.meta;

  this.nom_doc = event.meta.nom_doc;
  this.prenom_doc = event.meta.prenom_doc;
  this.nom_patient = event.meta.nom_patient;
  this.prenom_patient = event.meta.prenom_patient;
  this.appointment_date = this.formatDateToSQL(new Date(event.start));

  this.ToAdjustrdv = true;
  this.pressed = true;

  console.log('Existing event selected:', event);
  console.log('Appointment details loaded:', this.appointment);
}
}
