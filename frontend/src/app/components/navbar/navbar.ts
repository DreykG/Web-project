import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { RouterLink, RouterModule} from '@angular/router';
import { ProfileService } from '../../services/profile';
import { UserProfile } from '../../interfaces/models';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  profile: UserProfile | null = null;
  errorMessage = '';

  constructor(private profileService: ProfileService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    if(this.isLoggedIn()) {
      this.profileService.profile$.subscribe(
        data => {
          this.profile = data;
          this.cdr.detectChanges();
        });
      this.profileService.loadProfile();
    }
  }

  isLoggedIn() {
    return !!localStorage.getItem('token');
  }
}