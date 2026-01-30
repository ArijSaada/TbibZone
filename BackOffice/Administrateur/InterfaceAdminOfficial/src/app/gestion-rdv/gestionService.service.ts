import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class gestionRdvService {
  private baseUrl = 'http://192.168.43.128:5500/admin';

  constructor(private http: HttpClient) {}

  // Get all appointments
  get_rdv(): Observable<any> {
    return this.http.get(`${this.baseUrl}/getAllrdv`);
  }

  // Search appointments
  searchRdvs(v: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/search_rdvs`, { v });
  }

  // Add an appointment
  add_rdv(rdvData: {
    nom_doc: string,
    prenom_doc: string,
    nom_patient: string,
    prenom_patient: string,
    appointment_date: string
  }): Observable<any> {
    return this.http.post(`${this.baseUrl}/add_rdv`, rdvData);
  }
  

  // Delete an appointment
  del_rdv(rdvData: {
    nom_doc: string,
    prenom_doc: string,
    nom_patient: string,
    prenom_patient: string,
    appointment_date: string
  }): Observable<any> {
    return this.http.request('delete', `${this.baseUrl}/delete_rdv`, {
      body: rdvData
    });
  }

  // Modify an appointment
  Modifier_rdv(updateData: {
  nom_patient: string;
  prenom_patient: string;
  nom_doc: string;
  prenom_doc: string;
  appointment_date: string;
  new_nom_patient?: string;
  new_prenom_patient?: string;
  new_nom_doc?: string;
  new_prenom_doc?: string;
  new_datetime?: string;
},
 newAppointment: { nom_doc: string; prenom_doc: string; nom_patient: string; prenom_patient: string; appointment_date: string; }): Observable<any> {
    return this.http.put(`${this.baseUrl}/modify_rdv`, updateData);
  }
  
}
