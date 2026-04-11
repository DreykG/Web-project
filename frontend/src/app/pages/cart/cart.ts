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
  errorMessage = '';

  constructor(private shopService: ShopService) {}

  ngOnInit() {
    this.shopService.getCartItems().subscribe({
      next: (data:any) => {
        this.cartItems = data.items;
      },
      error: () => {
        this.errorMessage ='Cart Items loading error';
      }
    });
  }

  removeFromCart(itemId: number) {
    this.shopService.removeFromCart(itemId).subscribe({
      next: (data:any) => {
        this.cartItems = this.cartItems.filter(item => item.id !== itemId);
      },
      error: () => {
        this.errorMessage = 'Item remove error';
        
      }
    });
  }

  buyCart() {
    const ids = this.cartItems.map(item => item.id);
    this.shopService.buyCart(ids).subscribe({
      next: () => {
        this.cartItems = [];
        alert('Purchase successeful!');
      },
      error: () => {
        this.errorMessage = 'Purchase error';
      }
    });
  }

}
