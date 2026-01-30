import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';  

import { map } from 'rxjs/operators';
@Injectable({
  providedIn: 'root'
})
export class authservice {
  constructor(private http: HttpClient) {}
  login(Mail: string, pwd: string): Observable<{ success: boolean, msg: string }> {
    
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

 
    return this.http.post<any>(
      'http://192.168.1.19:5006/loginMed',
      { Mail, pwd },{headers}
    ).pipe(
      map(response => ({ success: response.success, msg: response.msg }))
    );
  }
}