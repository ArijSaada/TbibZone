import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginSuperComponent } from './login-super/login-super.component';
import { GestionAdminsComponent } from './gestion-admins/gestion-admins.component';

const routes: Routes = [
  {'path':'',component : LoginSuperComponent},
  {'path':'gestionAdmin',component : GestionAdminsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
