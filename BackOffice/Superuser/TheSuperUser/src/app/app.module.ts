import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginSuperComponent } from './login-super/login-super.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { GestionAdminsComponent } from './gestion-admins/gestion-admins.component';
import { EditAdminComponent } from './edit-admin/edit-admin.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginSuperComponent,
    GestionAdminsComponent,
    EditAdminComponent,
    
  ],
 imports: [
    FormsModule,
  
    ReactiveFormsModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule ,
    BrowserAnimationsModule,
       
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
