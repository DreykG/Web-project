import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterLink } from "@angular/router";
import { FormsModule } from '@angular/forms';
import { TradeService } from '../../services/trade';
import { ShopService } from '../../services/shop';
import { InventoryItem, TradeOffer, TradeResponse } from '../../interfaces/models';
import { RouterUpgradeInitializer } from '@angular/router/upgrade';

@Component({
  selector: 'app-trades',
  imports: [RouterLink, FormsModule],
  templateUrl: './trades.html',
  styleUrl: './trades.css',
})
export class Trades implements OnInit{
  offers: TradeOffer[] = [];
  myOffers: TradeOffer[] = [];
  errorMessage: string | null = null;
  showCreateModal = false;
  newOfferTitle = '';
  myInventory: InventoryItem[] = [];
  selectedItems: number[] = [];
  isPrivate = false;
  offerPassword = '';
  isDrawerOpen = false;
  showResponsesModal = false;
  selectedOfferResponses: TradeResponse[] = [];
  selectedOfferId: number | null = null;

  constructor(private tradeService: TradeService, private shopService: ShopService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.tradeService.getTradeOffers().subscribe({
      next: (data: TradeOffer[]) => {
        this.offers = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to load trade offers';
        this.cdr.detectChanges();
      }

    });

    this.tradeService.getMyTradeOffers().subscribe({
      next: (data: TradeOffer[]) => {
        this.myOffers = data;
        this.cdr.detectChanges(); 
      },
      error: (err) => {
        this.errorMessage = 'Failed to load your trade offers';
        this.cdr.detectChanges();

        setTimeout(() => {
          this.errorMessage = null;
          this.cdr.detectChanges();
        }, 3000);
      }
    });
  }

  openCreateModal() {
    this.showCreateModal = true;
    this.shopService.getInventory().subscribe({
      next: (data: InventoryItem[]) => {
        this.myInventory = data;
        this.cdr.detectChanges();
      }
    });
  }

  toggleItem(itemId: number) {
    const idx = this.selectedItems.indexOf(itemId);
    
    if(idx === -1) {
      this.selectedItems.push(itemId);
    }else {
      this.selectedItems.splice(idx, 1);
    }
  }

  openResponsesModal(offer: TradeOffer) {
    this.selectedOfferResponses = offer.responses;
    this.selectedOfferId = offer.id;
    this.showResponsesModal = true;
  }

  acceptResponse(responseId: number) {
    if (!this.selectedOfferId) return;
    this.tradeService.acceptResponse(this.selectedOfferId, responseId).subscribe({
      next: () => {
        this.showResponsesModal = false;
        this.tradeService.getMyTradeOffers().subscribe({
          next: (data: TradeOffer[]) => {
            this.myOffers = data;
            this.cdr.detectChanges(); 
          }
        });
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'Failed to accept response';
        this.cdr.detectChanges();
      }
    });
  }

  createOffer() {
    this.tradeService.createTradeOffer(
      this.newOfferTitle, 
      this.selectedItems, 
      this.isPrivate, 
      this.isPrivate ? this.offerPassword : null
    ).subscribe({
      next: (offer: TradeOffer) => {
        this.myOffers.push(offer);
        
        this.showCreateModal = false;
        this.selectedItems = [];

        this.newOfferTitle = '';
        this.offerPassword = '';
        this.isPrivate = false;

        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to create trade offer';
        this.cdr.detectChanges();

        setTimeout(() => {
          this.errorMessage = null;
          this.cdr.detectChanges();
        }, 3000);
      }
  });
}

  deleteOffer(offerId: number) {
    this.tradeService.deleteTradeOffer(offerId).subscribe({
      next: () => {
        this.myOffers = this.myOffers.filter(offer => offer.id !== offerId);
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to delete trade offer';
        this.cdr.detectChanges();

        setTimeout(() => {
          this.errorMessage = null;
          this.cdr.detectChanges();
        }, 3000);
      }
    });
  }

  toggleDrawer() {
    this.isDrawerOpen = !this.isDrawerOpen;
  }
}


