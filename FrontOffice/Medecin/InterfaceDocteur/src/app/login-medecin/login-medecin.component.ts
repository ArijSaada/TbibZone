import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { authservice } from './authservice.service';
import { firstValueFrom } from 'rxjs/internal/firstValueFrom';


@Component({
  selector: 'app-login-medecin',
  standalone: false,
  templateUrl: './login-medecin.component.html',
  styleUrls: ['./login-medecin.component.css']
})
export class LoginMedecinComponent {
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
     msg = response.msg;
    

    /*this.authService.login(mail, pwd).subscribe(response => {
      this.tr = response.success;
       msg = response.msg;
    })
       */
    if(this.tr) {
       
      alert(`Welcome Back ${mail} `);
      
      this.router.navigate(['compte-medecin'], { queryParams: { mail } });
    }
    else {
      alert(this.tr);
      console.log(msg);
    }

  }// Inject Router

}
