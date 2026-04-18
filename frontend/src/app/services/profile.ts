import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserProfile } from '../interfaces/models';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {
  private apiUrl = 'http://localhost:8000/api';
  private profileSubject = new BehaviorSubject<UserProfile | null>(null);
  profile$ = this.profileSubject.asObservable();

  constructor(private http: HttpClient) {}
    
  getProfile() {
    return this.http.get<UserProfile>(`${this.apiUrl}/users/profile/`);
  }

  loadProfile() {
    this.getProfile().subscribe({
      next: (profile) => {
        this.profileSubject.next(profile);
      },
      error: () => {
        this.profileSubject.next(null);
      }
    });
  }

  refreshProfile() {
    this.loadProfile();
  }

}
