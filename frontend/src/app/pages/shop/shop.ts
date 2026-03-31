import { Component, OnInit } from '@angular/core';
import { ShopService } from '../../services/shop';
@Component({
  selector: 'app-shop',
  imports: [],
  templateUrl: './shop.html',
  styleUrl: './shop.css',
})
export class Shop implements OnInit{
  skins: any[] = [];

  constructor(private shopService: ShopService) {}

  ngOnInit() {
    this.shopService.getSkins().subscribe({
      next: (data:any) => {
        this.skins = data;
      },
      error: () => {
        console.log('Skins loading error');
      }
    });
  }

  addToCart(skinId: number) {
    this.shopService.addToCart(skinId).subscribe({
      next: () => {
        alert('Skin has been added to the cart!');
      },
      error: () => {
        console.log('The error of adding to the cart');
      }
    });
  }
}
