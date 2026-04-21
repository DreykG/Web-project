import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Gang, GangMember, GangMessage, GangJoinRequest, GangVaultRental } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class GangService {
  private apiUrl = 'http://localhost:8000/api/gangs';

  constructor(private http: HttpClient) {}

  getGangs() {
    return this.http.get<Gang[]>(`${this.apiUrl}/`);
  }

  createGang(data: { name: string; description: string }) {
    return this.http.post<Gang>(`${this.apiUrl}/`, data);
  }

  getMembers(gangId: number) {
    return this.http.get<GangMember[]>(`${this.apiUrl}/${gangId}/members/`);
  }

  applyToGang(gangId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/apply/`, {});
  }

  getJoinRequests(gangId: number) {
    return this.http.get<GangJoinRequest[]>(`${this.apiUrl}/${gangId}/show_requests/`);
  }

  acceptRequest(gangId: number, requestId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/accept-request/${requestId}/`, {});
  }

  leaveGang(gangId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/leave/`, {});
  }

  promoteMember(gangId: number, userId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/promote/${userId}/`, {});
  }

  demoteMember(gangId: number, userId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/demote/${userId}/`, {});
  }

  kickMember(gangId: number, userId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/kick/${userId}/`, {});
  }

  getVault(gangId: number) {
    return this.http.get<GangVaultRental[]>(`${this.apiUrl}/${gangId}/vault/`);
  }

  depositItem(gangId: number, itemId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/deposit_item/${itemId}/`, {});
  }

  rentItem(gangId: number, itemId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/rent/${itemId}/`, {});
  }

  returnItem(gangId: number, itemId: number) {
    return this.http.post<any>(`${this.apiUrl}/${gangId}/return_item/${itemId}/`, {});
  }

  getChatHistory(gangId: number) {
    return this.http.get<GangMessage[]>(`${this.apiUrl}/${gangId}/chat_history/`);
  }

  sendMessage(gangId: number, text: string) {
    return this.http.post<GangMessage>(`${this.apiUrl}/${gangId}/send_message/`, { text });
  }
}