import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { CaseService } from '../../services/case';
import { Case, LiveDrop } from '../../interfaces/models';

@Component({
  selector: 'app-case',
  imports: [],
  templateUrl: './case.html',
  styleUrl: './case.css',
})
export class Cases implements OnInit {
  cases: Case[] = [];
  liveDrops: LiveDrop[] = [];
  isLoading = true;
  error: string | null = null;

  constructor(
    private caseService: CaseService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadCases();
    this.loadLiveDrops();
  }

  loadCases() {
    this.caseService.getCases().subscribe({
      next: (data) => {
        this.cases = data.filter(c => c.is_active);
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Failed to load cases';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadLiveDrops() {
    this.caseService.getLiveDrops().subscribe({
      next: (data) => {
        this.liveDrops = data;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Failed to load live drops';
        this.cdr.detectChanges();
      }
    });
  }

  goToCase(c: Case) {
    this.router.navigate(['/cases', c.id]);
  }
}