import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { InventoryItem, TradeOffer, TradeOfferItem, TradeResponse, TradeResponseItem } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class TradeService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getTradeOffers() {
    return this.http.get<TradeOffer[]>(`${this.apiUrl}/api/trades/`);
  }

  getMyTradeOffers() {
    return this.http.get<TradeOffer[]>(`${this.apiUrl}/api/trades/my_offers/`);
  }

  createTradeOffer(title: string, items: number[]) {
    return this.http.post<TradeOffer>(`${this.apiUrl}/api/trades/`, { title, items });
  }

  respondToOffer(offerId: number, items: number[]) {
    return this.http.post<TradeResponse>(`${this.apiUrl}/trades/${offerId}/respond/`, { items });
  }

  acceptResponse(offerId: number, responseId: number) {
    return this.http.post(`${this.apiUrl}/trades/${offerId}/accept-response/${responseId}/`, {});
  }
}
