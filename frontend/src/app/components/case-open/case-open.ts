import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectorRef,
  ViewChild,
  ElementRef,
  NgZone,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CaseService } from '../../services/case';
import { ProfileService } from '../../services/profile';
import { Case, CaseItem, CaseOpening } from '../../interfaces/models';

type OpenState = 'idle' | 'spinning' | 'result';

const CELL_WIDTH = 130;
const WINNER_INDEX = 50;
const SPIN_DURATION_MS = 4000;

@Component({
  selector: 'app-case-open',
  standalone: true,
  imports: [CommonModule],
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
  resultItem: CaseItem | null = null;
  winnerIndex = WINNER_INDEX;
  actionMessage: string | null = null;
  actionLoading = false;

  result: CaseOpening | null = null;
  private spinTimeout: any;

  @ViewChild('rouletteStrip') rouletteStripRef!: ElementRef<HTMLElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private caseService: CaseService,
    private cdr: ChangeDetectorRef,
    private ngZone: NgZone,
    private profileService: ProfileService
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
        this.case_ = cases.find((c) => c.id === id) || null;
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
      },
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
      },
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
    this.resetStripPosition();

    this.caseService.openCase(this.case_.id).subscribe({
      next: (opening) => {
        this.result = opening;
        this.profileService.refreshProfile();

        // Ищем скин в caseItems по item_id
        let winner = this.caseItems.find((ci) => ci.id === opening.item_id) || null;

        // Fallback: строим из drop если не нашли в списке
        if (!winner && opening.drop) {
          winner = {
            id: opening.item_id,
            skin_name: opening.drop.skin_name,
            wear_name: opening.drop.wear_name,
            img_url: opening.drop.url,
            drop_chance: 0,
          } as any;
        }

        this.resultItem = winner;

        if (this.resultItem) {
          this.rouletteItems[WINNER_INDEX] = this.resultItem;
          this.rouletteItems = [...this.rouletteItems];
        }

        this.cdr.detectChanges();

        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            this.startSpin();
          });
        });
      },
      error: (err) => {
        this.openState = 'idle';
        this.error = err?.error?.detail || 'Failed to open case. Check your balance.';
        this.cdr.detectChanges();
      },
    });
  }

  private resetStripPosition() {
    const el = this.rouletteStripRef?.nativeElement;
    if (!el) return;
    el.style.transition = 'none';
    el.style.transform = 'translateX(0)';
  }

  private startSpin() {
    const el = this.rouletteStripRef?.nativeElement;
    if (!el) return;

    const containerHalfWidth = (el.parentElement?.offsetWidth ?? 600) / 2;
    const winnerCellCenter = WINNER_INDEX * CELL_WIDTH + CELL_WIDTH / 2;
    const translateX = winnerCellCenter - containerHalfWidth;

    el.style.transition = `transform ${SPIN_DURATION_MS}ms cubic-bezier(0.12, 0.8, 0.22, 1)`;
    el.style.transform = `translateX(-${translateX}px)`;

    this.ngZone.runOutsideAngular(() => {
      this.spinTimeout = setTimeout(() => {
        this.ngZone.run(() => {
          this.openState = 'result';
          this.cdr.detectChanges();
        });
      }, SPIN_DURATION_MS + 200);
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
    if (!this.result?.drop?.id) return;
    this.actionLoading = true;
    this.caseService.accessDroppedItem(this.result.drop.id).subscribe({
      next: () => {
        this.actionMessage = '✓ Item added to your inventory!';
        this.actionLoading = false;
        this.profileService.refreshProfile();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Error accepting item.';
        this.actionLoading = false;
        this.cdr.detectChanges();
      },
    });
  }

  sellItem() {
    if (!this.result?.drop?.id) return;
    this.actionLoading = true;
    this.caseService.sellDroppedItem(this.result.drop.id).subscribe({
      next: () => {
        this.actionMessage = `✓ Sold for $${this.result!.sell_price}! Balance updated.`;
        this.actionLoading = false;
        this.profileService.refreshProfile();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Error selling item.';
        this.actionLoading = false;
        this.cdr.detectChanges();
      },
    });
  }

  openAgain() {
    const el = this.rouletteStripRef?.nativeElement;
    if (el) {
      el.style.transition = 'none';
      el.style.transform = 'translateX(0)';
    }
    this.openState = 'idle';
    this.result = null;
    this.resultItem = null;
    this.actionMessage = null;
    this.rouletteItems = [];
    this.cdr.detectChanges();
  }

  goBack() {
    this.router.navigate(['/cases']);
  }
}