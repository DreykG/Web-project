import { Component, OnInit } from '@angular/core';
import { ShopService } from '../../services/shop';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-shop',
  imports: [FormsModule],
  templateUrl: './shop.html',
  styleUrl: './shop.css',
})
export class Shop implements OnInit{
  skins: any[] = [];
  filteredSkins: any[] = [];
  searchText = '';

  constructor(private shopService: ShopService) {}

  ngOnInit() {
    this.shopService.getSkins().subscribe({
      next: (data:any) => {
        this.skins = data;
        this.filteredSkins = data;
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

  filterSkins() {
    this.filteredSkins = this.skins.filter(skin => skin.name.toLowerCase().includes(this.searchText.toLocaleLowerCase()))
  };
}
