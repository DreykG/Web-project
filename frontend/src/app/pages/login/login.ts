import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private authService: Auth, private router: Router) {}

  onLogin() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response: any) => {
        this.authService.saveToken(response.token);
        window.location.href = '/shop'
      },
      error: () => {
        this.errorMessage = 'Invalid username or password';
      }
    });
  }
}
