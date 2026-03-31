import { Component, OnInit } from '@angular/core';
import { ShopService } from '../../services/shop';
@Component({
  selector: 'app-cart',
  imports: [],
  templateUrl: './cart.html',
  styleUrl: './cart.css',
})
export class Cart implements OnInit{
  cartItems: any[] = [];

  constructor(private shopService: ShopService) {}

  ngOnInit() {
    this.shopService.getCartItems().subscribe({
      next: (data:any) => {
        this.cartItems = data;
      },
      error: () => {
        console.log('Cart Items loading error');
      }
    });
  }

  removeFromCart(itemId: number) {
    this.shopService.removeFromCart(itemId).subscribe({
      next: (data:any) => {
        this.cartItems = this.cartItems.filter(item => item.id !== itemId);
      },
      error: () => {
        console.log('Item remove error');
        
      }
    });
  }

  buyCart() {
    this.shopService.buyCart().subscribe({
      next: () => {
        console.log('Items have been successfully purchased');
      },
      error: () => {
        console.log('Purchase error');
      }
    });
  }

}
