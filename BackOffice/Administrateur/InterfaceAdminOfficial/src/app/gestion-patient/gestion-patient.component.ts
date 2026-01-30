import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';
import { gesntionService } from './gestionservice.service';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-gestion-patients',
  standalone: false,
  templateUrl: './gestion-patient.component.html',
  styleUrl: './gestion-patient.component.css'
})
export class GestionpatientsComponent {
  patient : any = {
    id : '',
    nom:'',
    prenom : '',
    mail : '',
    pwd : '',
    Appointments :'',
    saved_locations : '',
    History : ''

  }
  nom: string = '';
  prenom: string = '';
  mail: string = '';
  pwd: string = '';
  supprimer: boolean = false;
  

  patients: any[] = [];
 
   searchTerm: string = '';
   ToAdjustpatient: boolean = false;
  

  constructor(private router: Router, private patientService: gesntionService, private cdr : ChangeDetectorRef) {
    this.ToAdjustpatient = false;
   }

   ngOnInit() {
      this.Get_patient();
   }

   Get_patient() {
    console.log('Fetching patients...');
     this.patientService.get_patient().subscribe({
       next: (response) => {
         this.patients = response.msg;
       },
       error: (error) => {
         console.error('Error fetching patients:', error);
       }
     });
   }
   
   Adjustpatient(patient: any) {
    this.supprimer = true;
    this.ToAdjustpatient = true;
    this.patient = patient ;
    this.nom = patient.nom;
    this.prenom = patient.prenom;
    this.mail = patient.Mail;
    this.pwd = patient.pwd;
    console.log('patient to adjust:', patient);
    console.log('patient details:', this.nom, this.prenom, this.mail, this.pwd);
    

   }
   modifier: boolean = false;
   newnom: string = '';
   newprenom: string = '';
   newMail : string = '';
   newpwd : string = '';
 

   Updatepatient() {
    this.modifier = true;
    
  
  }
  SubmitModifier() {
    const newpatient = {
    nom: this.newnom,
    prenom: this.newprenom,
    Mail: this.newMail,
    pwd: this.newpwd
  };
    return this.patientService.Modifierpatient(this.patient, newpatient).subscribe({
      next: (response) => {
        if (response.success) {
          alert(response.success + response.msg);
        }
        else {
          alert('Error updating patient:' + response.msg);
        }
        this.Get_patient(); // Refresh the list after update
      },
      error: (error) => {
        console.error('Error updating patient:', error);
      }
    });


   // this.router.navigate(['/edit-patient']);
     // Logic to edit patient details
   }

   Deletepatient() {
    const mail = this.patient.Mail;
    alert('Deleting patient with mail:' + mail);
    this.patientService.del_patient(this.patient).subscribe({
      next: (response) => {
        if (response.success) {
          alert('patient deleted successfully:' + response.msg);
        }
        else {
          alert('Error deleting patient:' + response.msg);
        }
        this.Get_patient(); // Refresh the list after deletion
      },
      error: (error) => {
          alert('Error deleting patient:' + error);
      }
    });

   }
   Ajouter_Patient(){
    this.ToAdjustpatient = true;
   }
   Addpatient() {


    alert('Adding new patient:' + this.patient.nom + ' ' + this.patient.prenom + ' ' + this.patient.Mail);
    this.patient = {
      nom: this.nom,
      prenom: this.prenom,
      Mail: this.mail,
      pwd: this.pwd
    };

    this.patientService.add_patient(this.patient).subscribe({
      next: (response) => { 
        if (response.success) {
          alert('patient added successfully:' + response.msg);
        }
        else {
          alert('Error adding patient:' + response.msg);
        }
        this.Get_patient(); // Refresh the list after adding
      },
      error: (error) => {   
        console.error('Error adding patient:', error);
      }
    });
     // Logic to add a new patient
    
    }
  // Logic to handle form submission
  
  // Logic to handle patient search
  onSearchInput(searchTerm: string): void {
    if (searchTerm) {
      alert(searchTerm)
      this.patientService.rechercher_patient(searchTerm).subscribe({
        next: (response) => {
          this.patients = response.msg;
          
          this.cdr.detectChanges();

          console.log('Filtered patients:', this.patients);
        },
        error: (error) => {
          console.error('Error searching patients:', error);
        }
      });
    } else {
      // Reset the list if search term is empty
      this.Get_patient();
    }
  }
}
