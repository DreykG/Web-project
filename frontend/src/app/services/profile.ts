import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserProfile } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {
  
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}
    
  getProfile() {
    return this.http.get<UserProfile>(`${this.apiUrl}/users/profile/`);
  }

}
