import { Component } from '@angular/core';
import { RouterLink} from '@angular/router';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }
}
