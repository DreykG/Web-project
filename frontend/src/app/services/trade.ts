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
    return this.http.get<TradeOffer[]>(`${this.apiUrl}/trades/`);
  }

  getMyTradeOffers() {
    return this.http.get<TradeOffer[]>(`${this.apiUrl}/trades/my_offers/`);
  }

  getMyRequests() {
    return this.http.get<TradeResponse[]>(`${this.apiUrl}/trades/my_requests/`);
  }

  cancelResponse(responseId: number) {
    return this.http.post(`${this.apiUrl}/trades/${responseId}/cancel_response/`, {});
  }

  createTradeOffer(title: string, items: number[], isPrivate: boolean = false, password: string | null = null) {
    return this.http.post<TradeOffer>(`${this.apiUrl}/trades/`, { title, items, is_private: isPrivate, password });
  }

  respondToOffer(offerId: number, items: number[]) {
    return this.http.post<TradeResponse>(`${this.apiUrl}/trades/${offerId}/respond/`, { items });
  }

  acceptResponse(offerId: number, responseId: number) {
    return this.http.post(`${this.apiUrl}/trades/${offerId}/accept-response/${responseId}/`, {});
  }

  rejectResponse(offerId: number, responseId: number) {
    return this.http.post(`${this.apiUrl}/trades/${offerId}/reject-response/${responseId}/`, {});
  }

  deleteTradeOffer(offerId: number) {
    return this.http.post(`${this.apiUrl}/trades/${offerId}/cancel_offer/`, {});
  }

  verify_password(offerId: number, password: string) {
    return this.http.post(`${this.apiUrl}/trades/${offerId}/verify_password/`, { password });
  }
}
