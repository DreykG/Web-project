import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { InventoryItem, Cart, CartResponse } from '../interfaces/models';

@Injectable({
  providedIn: 'root',
})
export class ShopService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getSkins(categoryId?: number) {
    const params = categoryId ? `?category=${categoryId}` : '';
    return this.http.get<InventoryItem[]>(`${this.apiUrl}/shop/items/${params}`);
  }

  getCategories() {
    return this.http.get<any[]>(`${this.apiUrl}/shop/categories/`);
  }

  getCartItems() {
    return this.http.get<CartResponse>(`${this.apiUrl}/shop/cart/`);
  }

  getInventory(){
    return this.http.get<InventoryItem[]>(`${this.apiUrl}/shop/items/my_items/`);
  }

  addToCart(skinId: number){
    return this.http.post(`${this.apiUrl}/shop/cart/add/${skinId}`, {});
  }

  buyCart(ids: number[]){
    return this.http.post(`${this.apiUrl}/shop/cart/checkout`, {ids: ids});
  }

  removeFromCart(itemId: number){
    return this.http.post(`${this.apiUrl}/shop/cart/remove`, {ids: [itemId]});
  }

  saleItem(items: {id: number, price: number}[]){
    return this.http.post(`${this.apiUrl}/shop/items/sale`, {items});
  }

  getMySales(){
    return this.http.get<InventoryItem[]>(`${this.apiUrl}/shop/items/my_sales/`);
  }

  cancelSale(ids: number[]){
    return this.http.post(`${this.apiUrl}/shop/items/cancel_sale`, {ids});
  }
}
