import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Case, CaseItem, CaseOpening, LiveDrop, ItemActionRequest, InventoryItem } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class CaseService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getCases() {
    return this.http.get<Case[]>(`${this.apiUrl}/cases/list`);
  }

  getCaseItems(caseId: number) {
    return this.http.get<CaseItem[]>(`${this.apiUrl}/cases/list/${caseId}/case_items/`);
  }

  openCase(caseId: number) {
    return this.http.post<CaseOpening>(`${this.apiUrl}/cases/list/${caseId}/open_case/`, {});
  }

  accessDroppedItem(itemId: number) {
    return this.http.post<any>(`${this.apiUrl}/cases/list/access_dropped_item/`, { item_id: itemId });
  }

  sellDroppedItem(itemId: number) {
    return this.http.post<any>(`${this.apiUrl}/cases/list/sell_dropped_item/`, { item_id: itemId });
  }

  getPendingItems() {
    return this.http.get<InventoryItem[]>(`${this.apiUrl}/cases/list/pending_items/`);
  }

  sellAllPending() {
    return this.http.post<any>(`${this.apiUrl}/cases/list/sell_all_pending/`, {});
  }

  getLiveDrops() {
    return this.http.get<LiveDrop[]>(`${this.apiUrl}/cases/list/live_drops/`);
  }
}