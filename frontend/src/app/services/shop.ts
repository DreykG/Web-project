import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ShopService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getSkins() {
    return this.http.get(`${this.apiUrl}/shop/items/`);
  }

  getCartItems() {
    return this.http.get(`${this.apiUrl}/shop/cart/`);
  }

  getInventory(){
    return this.http.get(`${this.apiUrl}/shop/items/my_items/`);
  }

  addToCart(skinId: number){
    return this.http.post(`${this.apiUrl}/shop/cart/add/${skinId}/`, {});
  }

  buyCart(ids: number[]){
    return this.http.post(`${this.apiUrl}/shop/cart/checkout/`, {ids: ids});
  }

  removeFromCart(itemId: number){
    return this.http.post(`${this.apiUrl}/shop/cart/remove/`, {ids: [itemId]});
  }
}
