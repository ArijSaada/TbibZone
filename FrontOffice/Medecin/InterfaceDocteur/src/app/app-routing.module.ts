import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginMedecinComponent } from './login-medecin/login-medecin.component';
import { CalendarComponent } from './calendar-component/calendar-component.component';
import { ModifierRdvComponent } from './modifier-rdv/modifier-rdv.component';
import { LocalisationMedComponent } from './localisation-med/localisation-med.component';
import { CompteMedecinComponent } from './compte-medecin/compte-medecin.component';

const routes: Routes = [
  {'path' :'', component : LoginMedecinComponent},
  {'path': 'compte-medecin',component: CompteMedecinComponent},
  {'path' : 'GestionRdv', component :CalendarComponent},
  {'path': 'edit-rdv', component : ModifierRdvComponent},
  {'path': 'localisation', component : LocalisationMedComponent},
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
