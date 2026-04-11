import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class Auth {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post(`${this.apiUrl}/login/`, { username, password});
  }

  logout() {
    return this.http.post(`${this.apiUrl}/logout/`, {});
  }

  saveToken(token:string) {
    localStorage.setItem('token', token);
  }

  register(username: string, password: string) {
    return this.http.post(`${this.apiUrl}/register/`, { username, password });
  }

  getToken() {
    return localStorage.getItem('token');
  }

  isLoggedIn() {
    return localStorage.getItem('token') !== null;
  }
}
