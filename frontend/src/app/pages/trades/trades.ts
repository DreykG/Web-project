import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { TradeService } from '../../services/trade';
import { TradeOffer } from '../../interfaces/models';

@Component({
  selector: 'app-trades',
  imports: [],
  templateUrl: './trades.html',
  styleUrl: './trades.css',
})
export class Trades implements OnInit{
  offers: TradeOffer[] = [];
  myOffers: TradeOffer[] = [];
  errorMessage = '';

  constructor(private tradeService: TradeService, private cdr: ChangeDetectorRef) {}

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
      }
    });
  }

}
