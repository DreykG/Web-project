import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ShopService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getSkins() {
    return this.http.get(`${this.apiUrl}/skins/`);
  }

  getCartItems() {
    return this.http.get(`${this.apiUrl}/cart-items/`);
  }

  getInventory(){
    return this.http.get(`${this.apiUrl}/inventory/`);
  }

  addToCart(skinId: number){
    return this.http.post(`${this.apiUrl}/cart/`, {skin_id: skinId});
  }

  buyCart(){
    return this.http.post(`${this.apiUrl}/cart/buy/`, {});
  }

  removeFromCart(itemId: number){
    return this.http.delete(`${this.apiUrl}/cart-items/${itemId}/`);
  }
}
