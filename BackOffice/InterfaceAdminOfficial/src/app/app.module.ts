import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginAdminComponent } from './login-admin/login-admin.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { GestionpatientsComponent } from './gestion-patient/gestion-patient.component';
import { GestionMedecinComponent } from './gestion-medecin/gestion-medecin.component';
import { GestionRdvComponent } from './gestion-rdv/gestion-rdv.component';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DashboardComponent } from './dashboard/dashboard.component';
//import { AppointmentStatsComponent } from './dashboard/appointment-stats/appointment-stats.component';
import { NgApexchartsModule } from 'ng-apexcharts';


@NgModule({
  declarations: [
    AppComponent,
    
    LoginAdminComponent,
    GestionpatientsComponent,
    GestionMedecinComponent,
    GestionRdvComponent,
    DashboardComponent,
   // AppointmentStatsComponent,


    
  ],
    imports: [
     BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    
    RouterModule,
    BrowserAnimationsModule,
    CalendarModule.forRoot({ provide: DateAdapter, useFactory: adapterFactory }),

    NgApexchartsModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
