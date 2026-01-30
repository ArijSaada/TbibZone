import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';
import { gesntionService  } from './gestion-service.service';

@Component({
  selector: 'app-gestion-medecin',
  standalone: false,
  templateUrl: './gestion-medecin.component.html',
  styleUrl: './gestion-medecin.component.css'
})
export class GestionMedecinComponent {
  docteur : any = {
   
    name:'',
    prenom : '',
    mail : '',
    pwd : '',
    localisation : '',
    specialite  : '',

    
    

  }
  name: string = '';
  prenom: string = '';
  mail: string = '';
  pwd: string = '';
  localisation : string = '';
  specialite  : string = '';
  newlocalisation : string = '';
  newspec : string = '';
  supprimer: boolean = false;


  

  docteurs: any[] = [];
 
   searchTerm: string = '';
   ToAdjustdocteur: boolean = false;
  

  constructor(private router: Router, private DoctorService: gesntionService , private cdr : ChangeDetectorRef) {
    this.ToAdjustdocteur = false;
   }

   ngOnInit() {
      this.Get_docteur();
   }

   Get_docteur() {
    console.log('Fetching docteurs...');
     this.DoctorService .get_docteur().subscribe({
       next: (response) => {
         this.docteurs = response.msg;
       },
       error: (error) => {
         console.error('Error fetching docteurs:', error);
       }
     });
   }
   
   Adjustdocteur(docteur: any) {
    this.supprimer = true;
    this.ToAdjustdocteur = true;
    this.docteur = docteur ;
    this.name = docteur.name;
    this.prenom = docteur.prenom;
    this.mail = docteur.Mail;
    this.pwd = docteur.pwd;
    this.specialite  = docteur.speciality ;
    this.localisation = docteur.location;
   alert(this.docteur.name);
    console.log('docteur details:', this.name, this.prenom, this.mail);
    

   }
   modifier: boolean = false;
   newname: string = '';
   newprenom: string = '';
   newMail : string = '';
   newpwd : string = '';
 

   Updatedocteur() {
    this.modifier = true;
    
  
  }
  SubmitModifier() {
    alert(this.docteur.name)
    alert (this.docteur.prenom)
    alert (this.docteur.Mail)
    alert(this.docteur.pwd)
    alert(this.docteur.location)
    alert(this.specialite)
    const newdocteur = {
  name: this.docteur.name,
  prenom: this.docteur.prenom,
  Mail: this.docteur.Mail,
  pwd: this.docteur.pwd, //
  specialite: this.docteur.speciality,
  localisation: this.docteur.location,

  newname: this.newname,
  newprenom: this.newprenom,
  newMail: this.newMail,
  newpwd: this.newpwd,
  newspeciality: this.newspec,
  newlocation: this.newlocalisation
};
    return this.DoctorService.Modifierdocteur(newdocteur).subscribe({
      next: (response) => {
        if (response.success) {
          alert(response.success + response.msg);
        }
        else {
          alert('Error updating docteur:' + response.msg);
        }
        this.Get_docteur(); // Refresh the list after update
      },
      error: (error) => {
        console.error('Error updating docteur:', error);
      }
    });


   // this.router.navigate(['/edit-docteur']);
     // Logic to edit docteur details
   }

   Deletedocteur() {
    const mail = this.docteur.Mail;
    alert('Deleting docteur with mail:' + mail);
    this.DoctorService.del_docteur(this.docteur).subscribe({
      next: (response) => {
        if (response.success) {
          alert('docteur deleted successfully:' + response.msg);
        }
        else {
          alert('Error deleting docteur:' + response.msg);
        }
        this.Get_docteur(); // Refresh the list after deletion
      },
      error: (error) => {
          alert('Error deleting docteur:' + error);
      }
    });

   }
   AjoutForm(){
    this.ToAdjustdocteur = true;

   }
   AjouterMed() {


    this.docteur = {
      name: this.name,
      prenom: this.prenom,
      Mail: this.mail,
      specialite  : this.specialite ,
      localisation : this.localisation
    };
    alert (this.specialite)
    alert (this.docteur.specialite)

    this.DoctorService.add_docteur(this.docteur).subscribe({
      next: (response) => { 
        if (response.success) {
          alert('docteur added successfully:' + response.msg);
        }
        else {
          alert('Error adding docteur:' + response.msg);
        }
        this.Get_docteur(); // Refresh the list after adding
      },
      error: (error) => {   
        console.error('Error adding docteur:', error);
      }
    });
     // Logic to add a new docteur
    
    }
  // Logic to handle form submission
  
  // Logic to handle docteur search
  onSearchInput(searchTerm: string): void {
    if (searchTerm) {
      alert(searchTerm)
      this.DoctorService.rechercher_docteur(searchTerm).subscribe({
        next: (response) => {
          this.docteurs = response.msg;
          
          this.cdr.detectChanges();

          console.log('Filtered docteurs:', this.docteurs);
        },
        error: (error) => {
          console.error('Error searching docteurs:', error);
        }
      });
    } else {
      // Reset the list if search term is empty
      this.Get_docteur();
    }
  }

}
