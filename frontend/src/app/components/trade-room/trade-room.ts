import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { TradeService } from '../../services/trade';
import { ShopService } from '../../services/shop';
import { TradeOffer, InventoryItem } from '../../interfaces/models';
import { CdkDragDrop, moveItemInArray, transferArrayItem, DragDropModule } from '@angular/cdk/drag-drop';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-trade-room',
  imports: [DragDropModule, FormsModule],
  templateUrl: './trade-room.html',
  styleUrl: './trade-room.css',
})
export class TradeRoom implements OnInit {
  offer: TradeOffer | null = null;
  myInventory: InventoryItem[] = [];
  selectedItems: InventoryItem[] = [];
  errorMessage = '';
  passwordInput = '';
  passwordVerified = false;

  constructor(private route: ActivatedRoute, private tradeService: TradeService, private shopService: ShopService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    const offerId = Number(this.route.snapshot.paramMap.get('id'));

    this.tradeService.getTradeOffers().subscribe({
      next: (data: TradeOffer[]) => {
        this.offer = data.find(o => o.id === offerId) || null;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to load trade offer';
        this.cdr.detectChanges();
      }
    });

    this.shopService.getInventory().subscribe({
      next: (data: InventoryItem[]) => {
        this.myInventory = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to load your inventory';
        this.cdr.detectChanges();
      }
    });
  }

  toggleItem(item: InventoryItem) {
    const idx = this.selectedItems.findIndex(i => i.id === item.id);

    if(idx === -1) {
      this.selectedItems.push(item);
    } else {
      this.selectedItems.splice(idx, 1);
    }
  }

  isSelected(item: InventoryItem): boolean {
    return this.selectedItems.some(i => i.id === item.id);
  }

  respondToOffer() {
    if (!this.offer) return;

    const itemIds = this.selectedItems.map(i => i.id);

    this.tradeService.respondToOffer(this.offer.id, itemIds).subscribe({
        next: () => {
            this.errorMessage = '';
            this.cdr.detectChanges();
        },
        error: () => {
            this.errorMessage = 'Failed to respond to offer';
            this.cdr.detectChanges();
        }
    });
  }

  drop(event: CdkDragDrop<InventoryItem[]>) {
    if (event.previousContainer === event.container) {
        moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
        transferArrayItem(
            event.previousContainer.data,
            event.container.data,
            event.previousIndex,
            event.currentIndex
        );
    }
    this.cdr.detectChanges();
  }

  verifyPassword() {
    if (!this.offer) return;

    this.tradeService.verify_password(this.offer.id, this.passwordInput).subscribe({
      next: () => {
        this.passwordVerified = true;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Incorrect password';
        this.cdr.detectChanges();
      }
    });
  }
}
