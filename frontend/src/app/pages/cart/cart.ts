import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ShopService } from '../../services/shop';
import { CartResponse, InventoryItem } from '../../interfaces/models';
import { ProfileService } from '../../services/profile';
@Component({
  selector: 'app-cart',
  imports: [],
  templateUrl: './cart.html',
  styleUrl: './cart.css',
})
export class Cart implements OnInit{
  cartItems: InventoryItem[] = [];
  errorMessage = '';

  constructor(private shopService: ShopService, private cdr: ChangeDetectorRef, private profileService: ProfileService) {}

  ngOnInit() {
    this.shopService.getCartItems().subscribe({
      next: (data:CartResponse) => {
        this.cartItems = data.items;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage ='Cart Items loading error';
      }
    });
  }

  removeFromCart(itemId: number) {
    this.shopService.removeFromCart(itemId).subscribe({
      next: () => {
        this.cartItems = this.cartItems.filter(item => item.id !== itemId);
        this.cdr.detectChanges();
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
        //alert('Purchase successeful!');

        this.profileService.loadProfile();
        this.shopService.getCartItems().subscribe({
          next: (data: CartResponse) => {
            console.log('Cart after purchase:', data);
            this.cartItems = data.items;
            this.cdr.detectChanges();
          }
        });
      },
      error: (err) => {
        console.log('Purchase error:', err);
        this.errorMessage = 'Purchase error';
        this.cdr.detectChanges();
      }
    });

  }

    totalSum() {
      return this.cartItems.reduce((sum, item) => sum + Number(item.price), 0);
    }

}
