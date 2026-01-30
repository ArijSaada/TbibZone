import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { gesntionService } from './gestioAdmin.service';

@Component({
  selector: 'app-gestion-admins',
  standalone: false,
  templateUrl: './gestion-admins.component.html',
  styleUrl: './gestion-admins.component.css'
})
export class GestionAdminsComponent {
  admin : any = {
    nom:'',
    prenom : '',
    mail : '',
    pwd : ''
  }
  nom: string = '';
  prenom: string = '';
  mail: string = '';
  pwd: string = '';
  

  admins: any[] = [];
 
   searchTerm: string = '';
   ToAdjustAdmin: boolean = false;
  

  constructor(private router: Router, private adminService: gesntionService) {
    this.ToAdjustAdmin = false;
   }

   ngOnInit() {
      this.Get_Admin();
   }

   Get_Admin() {
    console.log('Fetching admins...');
     this.adminService.get_admin().subscribe({
       next: (response) => {
         this.admins = response.msg;
       },
       error: (error) => {
         console.error('Error fetching admins:', error);
       }
     });
   }
   //fonction modifier
   
   AdjustAdmin(admin: any) {
    this.ToAdjustAdmin = true;
    this.admin = admin ;
    this.nom = admin.nom;
    this.prenom = admin.prenom;
    this.mail = admin.Mail;
    this.pwd = admin.pwd;
    console.log('Admin to adjust:', admin);
    console.log('Admin details:', this.nom, this.prenom, this.mail, this.pwd);
    

   }
   modifier: boolean = false;
   newnom: string = '';
   newprenom: string = '';
   newMail : string = '';
   newpwd : string = '';
 

   UpdateAdmin() {
    this.modifier = true;
    
  
  }
  //envoie de requete modifier au service
  SubmitModifier() {
    const newAdmin = {
    nom: this.newnom,
    prenom: this.newprenom,
    Mail: this.newMail,
    pwd: this.newpwd
  };
    return this.adminService.ModifierAdmin(this.admin, newAdmin).subscribe({
      next: (response) => {
        if (response.success) {
          alert(response.success + response.msg);
        }
        else {
          alert('Error updating admin:' + response.msg);
        }
        this.Get_Admin(); // Refresh the list after update
      },
      error: (error) => {
        console.error('Error updating admin:', error);
      }
    });


 
   }

   DeleteAdmin() {
    const mail = this.admin.Mail;
    alert('Deleting admin with mail:' + mail);
    this.adminService.del_admin(this.admin).subscribe({
      next: (response) => {
        if (response.success) {
          alert('Admin deleted successfully:' + response.msg);
        }
        else {
          alert('Error deleting admin:' + response.msg);
        }
        this.Get_Admin(); // Refresh the list after deletion
      },
      error: (error) => {
          alert('Error deleting admin:' + error);
      }
    });

   }
   AddAdmin() {


    alert('Adding new admin:' + this.admin.nom + ' ' + this.admin.prenom + ' ' + this.admin.Mail);
    this.admin = {
      nom: this.nom,
      prenom: this.prenom,
      Mail: this.mail,
      pwd: this.pwd
    };

    this.adminService.add_admin(this.admin).subscribe({
      next: (response) => { 
        if (response.success) {
          alert('Admin added successfully:' + response.msg);
        }
        else {
          alert('Error adding admin:' + response.msg);
        }
        this.Get_Admin(); // Refresh the list after adding
      },
      error: (error) => {   
        console.error('Error adding admin:', error);
      }
    });
    
    }
  
  onSearchInput(searchTerm: string): void {
    if (searchTerm) {
      
      this.adminService.rechercher_admin(searchTerm).subscribe({
        next: (response) => {
          this.admins = response.msg;
          console.log('Filtered admins:', this.admins);
        },
        error: (error) => {
          console.error('Error searching admins:', error);
        }
      });
    } else {
      
      this.Get_Admin();
    }
  }
}
