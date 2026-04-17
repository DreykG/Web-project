import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ShopService } from '../../services/shop';
import { FormsModule } from '@angular/forms';
import { InventoryItem } from '../../interfaces/models';
@Component({
  selector: 'app-shop',
  imports: [FormsModule],
  templateUrl: './shop.html',
  styleUrl: './shop.css',
})
export class Shop implements OnInit{
  skins: InventoryItem[] = [];
  sortedSkins: InventoryItem[] = [];
  searchText = '';
  sortBy = 'default';
  errorMessage: string | null = null;

  constructor(private shopService: ShopService, private cdr: ChangeDetectorRef) {}

ngOnInit() {
  this.shopService.getSkins().subscribe({
    next: (data: InventoryItem[]) => {
      this.skins = data;
      this.sortedSkins = [...data]; 
      this.cdr.detectChanges();
    },
    error: (err) => {
      this.errorMessage = 'Failed to load skins';
      this.cdr.detectChanges();

      setTimeout(() => {
        this.errorMessage = null;
        this.cdr.detectChanges();
      }, 3000);
    }
  });
}

  addToCart(skinId: number) {
    this.shopService.addToCart(skinId).subscribe({
      next: () => {
        alert('Skin has been added to the cart!');
      },
      error: () => {
        this.errorMessage = 'Failed to load cart';

        setTimeout(() => {
        this.errorMessage = null;
        this.cdr.detectChanges();
      }, 3000);
      }
    });
  }

  sortSkins() {

    let result = [...this.skins];

    if (this.searchText.trim()) {
      const search = this.searchText.toLowerCase();
      result = result.filter(skin => 
        skin.skin_name?.toLowerCase().includes(search)
      );
    }

    if(this.sortBy === 'price_asc') {
      result.sort((a, b) => a.price - b.price);
    } else if(this.sortBy === 'price_desc') {
      result.sort((a, b) => b.price - a.price);
    } else if(this.sortBy === 'date_asc') {
      result.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
    } else if(this.sortBy === 'date_desc') {
      result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    }

  this.sortedSkins = result;
  };
}
