import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { RouterLink} from '@angular/router';
import { ProfileService } from '../../services/profile';
import { UserProfile } from '../../interfaces/models';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  profile: UserProfile | null = null;
  errorMessage = '';

  constructor(private profileService: ProfileService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
          console.log('isLoggedIn:', this.isLoggedIn());
    if(this.isLoggedIn()) {
      this.profileService.getProfile().subscribe({
        next: (data: UserProfile) => {
          this.profile = data;
          this.cdr.detectChanges();
        },
        error: () => {
          this.errorMessage = 'Profile loading error';
          this.cdr.detectChanges();
        }
      });
    }
  }

  isLoggedIn() {
    return !!localStorage.getItem('token');
  }
}