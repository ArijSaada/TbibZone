import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class gesntionService {
  constructor(private http: HttpClient) { }

  private apiUrl = 'http://192.168.1.19:5201';

  // calendar-service.service.ts

  get_admin(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
     // This is the actual data to send

    return this.http.get<any>(`${this.apiUrl}/AfficherAdmin`, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des admins'));
      })
    );
  }
 rechercher_admin(filter?: string): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  const params = new HttpParams().set('v', filter || '');

  return this.http.post<any>(`${this.apiUrl}/chercherAdmin`, {}, { headers, params }).pipe(
    map(response => {
      return response; // full object: { success, msg }
    }),
    catchError((error) => {
      console.error('Error from backend:', error);
      return throwError(() => new Error('Erreur lors du chargement des admins'));
    })
  );
}

  del_admin(adminData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {
     Mail : adminData.Mail,
      
      
    };
    return this.http.delete(`${this.apiUrl}/SupprimerAdmin`, {
  headers: headers,
  body: body
});

  };


  add_admin(adminData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {

      nom_admin: adminData.nom,
      prenom_admin: adminData.prenom,
      Mail : adminData.Mail,
        pwd: adminData.pwd,
     
    };
    return this.http.post<any>(`${this.apiUrl}/AjouterAdmin`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors de l\'ajout de l\'admin'),error);
      })
    );}


  ModifierAdmin(admin: any, newAdmin: any): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });
  
  const body = {
    nom_admin: admin.nom,
    prenom_admin: admin.prenom,
    Mail: admin.Mail,
    pwd: admin.pwd,

    newnom_admin: newAdmin.nom,
    newprenom_admin: newAdmin.prenom,
    newMail: newAdmin.Mail,
    newpwd: newAdmin.pwd,
  };

  return this.http.put(`${this.apiUrl}/modif_admin `, body, { headers }).pipe(
      map(response => {
        
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des admins'));
      })
    );} 


} 
