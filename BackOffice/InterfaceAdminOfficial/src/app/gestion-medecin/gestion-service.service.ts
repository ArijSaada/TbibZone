import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class gesntionService {
  constructor(private http: HttpClient) { }

  private apiUrl = 'http://192.168.43.128:5222';

  // calendar-service.service.ts

  get_docteur(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
     // This is the actual data to send

    return this.http.get<any>(`${this.apiUrl}/Afficherdocteur`, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors du chargement des docteurs'));
      })
    );
  }
 rechercher_docteur(filter?: string): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  const params = new HttpParams().set('v', filter || '');

  return this.http.get<any>(`${this.apiUrl}/chercherdocteur`, { headers, params }).pipe(
    map(response => {
      return response; // full object: { success, msg }
    }),
    catchError((error) => {
      console.error('Error from backend:', error);
      return throwError(() => new Error('Erreur lors du chargement des docteurs'));
    })
  );
}


  del_docteur(docteurData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {
     Mail : docteurData.Mail,
      
      
    };
    return this.http.delete(`${this.apiUrl}/Supprimerdocteur`, {
  headers: headers,
  body: body
});

  };


  add_docteur(docteurData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
  



    const body = {

      name: docteurData.name,
      prenom: docteurData.prenom,
      Mail : docteurData.Mail,
      localisation : docteurData.localisation,
      speciality  : docteurData.specialite ,
     
    };
    return this.http.post<any>(`${this.apiUrl}/AjouterDocteur`, body, { headers }).pipe(
      map(response => {
        return response;  // full object: { success, msg }
      }),
      catchError((error) => {
        console.error('Error from backend:', error);
        return throwError(() => new Error('Erreur lors de l\'ajout de l\'docteur'),error);
      })
    );}


  Modifierdocteur( newdocteur: any): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  const body = {
    // Anciennes infos
    Mail: newdocteur.Mail,
    pwd: newdocteur.pwd,
    name: newdocteur.name,
    prenom: newdocteur.prenom,
    localisation: newdocteur.localisation,   
    specialite: newdocteur.specialite,       

    // Nouvelles infos
    newMail: newdocteur.newMail,
    newpwd: newdocteur.newpwd,
    newname: newdocteur.newname,
    newprenom: newdocteur.newprenom,
    newlocalisation: newdocteur.newlocalisation,  
    newspecialite: newdocteur.newspecialite       
  };

  return this.http.put(`${this.apiUrl}/modifierDocteur`, body, { headers }).pipe(
    map(response => response),
    catchError((error) => {
      console.error('Error from backend:', error);
      return throwError(() => new Error('Erreur lors de la modification du docteur'));
    })
  );
}

  




} 
