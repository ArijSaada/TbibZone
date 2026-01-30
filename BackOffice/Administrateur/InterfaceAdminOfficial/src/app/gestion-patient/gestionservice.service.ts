import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class gesntionService {
  constructor(private http: HttpClient) { }

  private apiUrl = 'http://192.168.43.128:5210';

  // calendar-service.service.ts

  get_patient(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
     // This is the actual data to send

    return this.http.get<any>(`${this.apiUrl}/Afficherpatient`, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des patients'));
      })
    );
  }
 rechercher_patient(filter?: string): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  const params = new HttpParams().set('v', filter || '');

  return this.http.get<any>(`${this.apiUrl}/chercherpatient`, { headers, params }).pipe(
    map(response => {
      return response; // full object: { success, msg }
    }),
    catchError((error) => {
      console.error('Error from backend:', error);
      return throwError(() => new Error('Erreur lors du chargement des patients'));
    })
  );
}


  del_patient(patientData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {
     Mail : patientData.Mail,
      
      
    };
    return this.http.delete(`${this.apiUrl}/Supprimerpatient`, {
  headers: headers,
  body: body
});

  };


  add_patient(patientData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {

      nom: patientData.nom,
      prenom: patientData.prenom,
      Mail: patientData.Mail,
        pwd: patientData.pwd,
     
    };
    return this.http.post<any>(`${this.apiUrl}/AjouterPatient`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
      console.error('Error from backend:', error);
      return throwError(() => new Error('Erreur lors de l\'ajout du patient'));
})

    );}


  Modifierpatient(patient: any, newpatient: any): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });
  
  const body = {
    nom: patient.nom,
    prenom: patient.prenom,
    Mail: patient.Mail,
    pwd: patient.pwd,

    newname: newpatient.nom,
    newprenom: newpatient.prenom,
    newMail: newpatient.Mail,
    newpwd: newpatient.pwd,
  };

  return this.http.put(`${this.apiUrl}/modifierPatient`, body, { headers }).pipe(
      map(response => {
        
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des patients'));
      })
    );}

  




} 
