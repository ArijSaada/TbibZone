import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';  

import { map } from 'rxjs/operators';
@Injectable({
  providedIn: 'root'
})
export class MedecinService {
  constructor(private http: HttpClient) {}

  getAdresseActuelle(mail: string): Observable<string> {
    return this.http.get<any>(`http://192.168.1.19:5005/api/address?mail=${mail}`).pipe(
        map(response => response["msg  "] || response["msg"])
      );
    }
  
  updateAdresse(nouvelleAdresse: string, mail : String): Observable<void> {
    // Simule une mise à jour. Remplace-le avec un vrai PUT
    console.log('Adresse envoyée à la base :', nouvelleAdresse);
   
    return this.http.put<void>(
        'http://192.168.1.19:5005/api/changeAddress',
        {
          change: nouvelleAdresse,
          mail: mail
        }
      )
      
    }
}
