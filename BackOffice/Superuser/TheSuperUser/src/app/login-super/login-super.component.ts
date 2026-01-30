import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { authservice } from './authservice.service';
import { firstValueFrom } from 'rxjs/internal/firstValueFrom';


@Component({
  selector: 'app-login-super',
  standalone: false,
  templateUrl: './login-super.component.html',
  styleUrl: './login-super.component.css'
})
export class LoginSuperComponent {
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
   

    if(this.tr) {
       
      alert(`Welcome Back ${mail} `);
      
      this.router.navigate(['gestionAdmin']);
    }
    else {
      alert(this.tr);
      alert(mail)
      
      alert(`Login failed: ${response.msg}`);
      console.log(msg);
    }

  }

 
  
}

