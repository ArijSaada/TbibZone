import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { authservice } from './authservice.service';

@Component({
  selector: 'app-login-admin',
  standalone: false,
  templateUrl: './login-admin.component.html',
  styleUrl: './login-admin.component.css',
})
export class LoginAdminComponent {
  tr :boolean = false;
  adresseForm: FormGroup;


  constructor(private router: Router, private fb : FormBuilder,private authService: authservice) {
    this.adresseForm = this.fb.group({
      mail: ['', [Validators.required, Validators.email]],
      pwd :['', [Validators.required]]
    });
  } 

  async login(){
    var msg ="";
    
    
   
    const mail = this.adresseForm.get('mail')?.value;
    const pwd = this.adresseForm.get('pwd')?.value;
    const response = await firstValueFrom(this.authService.login(mail ,pwd));
    this.tr = response.success;
   

    /*this.authService.login(mail, pwd).subscribe(response => {
      this.tr = response.success;
       msg = response.msg;
    })
       */
    if(this.tr) {
       
      alert(`Welcome Back ${mail} `);
      alert(`Your password is ${pwd}`);
      this.router.navigate(['gestion']);
    }
    else {
      alert(this.tr);
      alert(`Login failed: ${response.msg}`);
      console.log(msg);
    }

  }// Inject Router
;
  
}
  
