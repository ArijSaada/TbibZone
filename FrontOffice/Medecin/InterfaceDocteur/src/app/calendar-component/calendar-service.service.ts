import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CalendarServiceService {
  constructor(private http: HttpClient) { }

  private apiUrl = 'http://192.168.1.19:5001';

  // calendar-service.service.ts

  get_rdv(filters?: { [key: string]: string }): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
    const body = filters || {};  // This is the actual data to send
  
    return this.http.post<any>(`${this.apiUrl}/get_rdv`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des rendez-vous'));
      })
    );
  }
del_rdv(appointmentData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {
      mail_doc: appointmentData.mail_doc,
      nom_patient: appointmentData.nom_patient,
      prenom_patient: appointmentData.prenom_patient,
      DateHeure: appointmentData.DateHeure,
      details: appointmentData.details
    };
    return this.http.delete(`${this.apiUrl}/del_rdv`, {
  headers: headers,
  body: body
});

  };


  add_rdv(appointmentData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {
      mail_doc: appointmentData.mail_doc,
      nom_patient: appointmentData.nom_patient,
      prenom_patient: appointmentData.prenom_patient,
      DateHeure: appointmentData.DateHeure,
      details: appointmentData.details
    };
    return this.http.post<any>(`${this.apiUrl}/add_rdv`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des rendez-vous'),error);
      })
    );}


  ModifierRdv(eventToModify: any): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });
  
  const body = {
    mail_doc: eventToModify.mail_doc,
    nom_patient: eventToModify.nom_patient,
    prenom_patient: eventToModify.prenom_patient,
    
    newnom_patient: eventToModify.newnom_patient,
    newprenom_patient: eventToModify.newprenom_patient,
    new_dateTime: eventToModify.new_dateTime, 
    newdetails: eventToModify.details || '',
    DateHeure: eventToModify.DateHeure
  };

  return this.http.put(`${this.apiUrl}/modif_rdv`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des rendez-vous'));
      })
    );}


} 
