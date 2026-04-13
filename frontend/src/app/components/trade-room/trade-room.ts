import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterLink, ActivatedRoute } from "@angular/router";
import { TradeService } from '../../services/trade';
import { ShopService } from '../../services/shop';
import { TradeOffer, InventoryItem } from '../../interfaces/models';

@Component({
  selector: 'app-trade-room',
  imports: [RouterLink],
  templateUrl: './trade-room.html',
  styleUrl: './trade-room.css',
})
export class TradeRoom implements OnInit {
  offer: TradeOffer | null = null;
  myInventory: InventoryItem[] = [];
  selectedItems: InventoryItem[] = [];
  errorMessage = '';

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
}
