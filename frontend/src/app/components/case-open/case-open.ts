import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CaseService } from '../../services/case';
import { Case, CaseItem, CaseOpening } from '../../interfaces/models';

type OpenState = 'idle' | 'spinning' | 'result';

@Component({
  selector: 'app-case-open',
  imports: [],
  templateUrl: './case-open.html',
  styleUrl: './case-open.css',
})
export class CaseOpen implements OnInit, OnDestroy {
  case_: Case | null = null;
  caseItems: CaseItem[] = [];
  isLoading = true;
  error: string | null = null;

  openState: OpenState = 'idle';
  rouletteItems: CaseItem[] = [];
  result: CaseOpening | null = null;
  resultItem: CaseItem | null = null;
  actionMessage: string | null = null;
  actionLoading = false;

  private spinTimeout: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private caseService: CaseService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadCase(id);
  }

  ngOnDestroy() {
    clearTimeout(this.spinTimeout);
  }

  loadCase(id: number) {
    this.caseService.getCases().subscribe({
      next: (cases) => {
        this.case_ = cases.find(c => c.id === id) || null;
        if (!this.case_) {
          this.error = 'Case not found';
          this.isLoading = false;
          this.cdr.detectChanges();
          return;
        }
        this.loadItems(id);
      },
      error: () => {
        this.error = 'Failed to load case';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadItems(id: number) {
    this.caseService.getCaseItems(id).subscribe({
      next: (items) => {
        this.caseItems = items;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Failed to load case items';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  open() {
    if (!this.case_ || this.openState === 'spinning') return;

    this.rouletteItems = this.buildRouletteStrip();
    this.openState = 'spinning';
    this.result = null;
    this.resultItem = null;
    this.actionMessage = null;
    this.cdr.detectChanges();

    this.caseService.openCase(this.case_.id).subscribe({
      next: (opening) => {
        this.result = opening;
        this.resultItem = this.caseItems.find(ci => ci.id === opening.case_item) || null;

        if (this.resultItem) {
          this.rouletteItems[50] = this.resultItem;
        }

        this.cdr.detectChanges();

        this.spinTimeout = setTimeout(() => {
          this.openState = 'result';
          this.cdr.detectChanges();
        }, 4200);
      },
      error: (err) => {
        this.openState = 'idle';
        this.error = err?.error?.detail || 'Failed to open case. Check your balance.';
        this.cdr.detectChanges();
      }
    });
  }

  buildRouletteStrip(): CaseItem[] {
    if (!this.caseItems.length) return [];
    const strip: CaseItem[] = [];
    for (let i = 0; i < 60; i++) {
      strip.push(this.caseItems[Math.floor(Math.random() * this.caseItems.length)]);
    }
    return strip;
  }

  acceptItem() {
    if (!this.result?.inventory_item) return;
    this.actionLoading = true;
    this.caseService.accessDroppedItem(this.result.inventory_item).subscribe({
      next: () => {
        this.actionMessage = '✓ Item added to your inventory!';
        this.actionLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Error accepting item.';
        this.actionLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  sellItem() {
    if (!this.result?.inventory_item) return;
    this.actionLoading = true;
    this.caseService.sellDroppedItem(this.result.inventory_item).subscribe({
      next: () => {
        this.actionMessage = '✓ Item sold! Balance updated.';
        this.actionLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Error selling item.';
        this.actionLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  openAgain() {
    this.openState = 'idle';
    this.result = null;
    this.resultItem = null;
    this.actionMessage = null;
    this.cdr.detectChanges();
  }

  goBack() {
    this.router.navigate(['/cases']);
  }
}