import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginAdminComponent } from './login-admin/login-admin.component';
import { GestionpatientsComponent } from './gestion-patient/gestion-patient.component';
import { GestionMedecinComponent } from './gestion-medecin/gestion-medecin.component';
import { GestionRdvComponent } from './gestion-rdv/gestion-rdv.component';
import { DashboardComponent } from './dashboard/dashboard.component';
//import { DashboardComponent} from './dashboard/dashboard.component';

const routes: Routes = [{'path': '', component : LoginAdminComponent},
  {path: 'gestionPatient', component: GestionpatientsComponent},
  {path: 'gestionMed', component: GestionMedecinComponent},
  {path : 'gestionrdv', component :GestionRdvComponent},
  {path: 'gestion', component: DashboardComponent}
 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
