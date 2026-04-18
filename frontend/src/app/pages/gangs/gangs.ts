import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { GangService } from '../../services/gang';
import { Gang } from '../../interfaces/models';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-gangs',
  imports: [FormsModule],
  templateUrl: './gangs.html',
  styleUrl: './gangs.css',
})
export class Gangs implements OnInit {
  gangs: Gang[] = [];
  isLoading = true;
  error: string | null = null;

  showCreateForm = false;
  createName = '';
  createDescription = '';
  createError: string | null = null;
  createLoading = false;

  constructor(
    private gangService: GangService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadGangs();
  }

  loadGangs() {
    this.isLoading = true;
    this.gangService.getGangs().subscribe({
      next: (data) => {
        this.gangs = data;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Failed to load gangs';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  goToGang(gang: Gang) {
    this.router.navigate(['/gangs', gang.id]);
  }

  toggleCreateForm() {
    this.showCreateForm = !this.showCreateForm;
    this.createError = null;
  }

  createGang() {
    if (!this.createName.trim() || !this.createDescription.trim()) {
      this.createError = 'Name and description are required';
      return;
    }
    this.createLoading = true;
    this.gangService.createGang({
      name: this.createName.trim(),
      description: this.createDescription.trim()
    }).subscribe({
      next: (gang) => {
        this.createLoading = false;
        this.showCreateForm = false;
        this.createName = '';
        this.createDescription = '';
        this.router.navigate(['/gangs', gang.id]);
      },
      error: (err) => {
        this.createError = err?.error?.name?.[0] || err?.error?.detail || 'Failed to create gang';
        this.createLoading = false;
        this.cdr.detectChanges();
      }
    });
  }
}