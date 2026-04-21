import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ShopService } from '../../services/shop';
import { ProfileService } from '../../services/profile';
import { InventoryItem, UserProfile } from '../../interfaces/models';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-inventory',
  imports: [FormsModule, CommonModule],
  templateUrl: './inventory.html',
  styleUrl: './inventory.css',
})
export class Inventory implements OnInit {
  profile: UserProfile | null = null;
  inventoryItems: InventoryItem[] = [];
  mySales: InventoryItem[] = [];
  salePrice: { [id: number]: number } = {};
  activeTab: 'inventory' | 'sales' = 'inventory';
  errorMessage = '';
  successMessage = '';

  constructor(private shopService: ShopService, private cdr: ChangeDetectorRef, private profileService: ProfileService) {}

  ngOnInit(){
    this.profileService.getProfile().subscribe({
      next: (data: UserProfile) => {
        this.profile = data;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Profile loading error';
        this.cdr.detectChanges();
      }
    });

    this.shopService.getInventory().subscribe({
      next: (data:InventoryItem[]) => {
        this.inventoryItems = data.filter(item => item.status !== 'on_sale');
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Inventory loading error';
        this.cdr.detectChanges();
      }
    });

  this.shopService.getMySales().subscribe({
    next: (data: InventoryItem[]) => {
      this.mySales = data;
      this.cdr.detectChanges();
    },
    error: () => {
      this.errorMessage = 'Sales loading error';
      this.cdr.detectChanges();
    }
  });
}

  logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }

  putOnSale(item: InventoryItem) {
    const price = this.salePrice[item.id];
    if (!price || price <= 0) {
      this.errorMessage = 'Invalid price';
      this.cdr.detectChanges();
      return;
    }
    this.shopService.saleItem([{ id: item.id, price }]).subscribe({
      next: () => {
        this.successMessage = `✓ ${item.skin_name} выставлен на продажу!`;
        setTimeout(() => { this.successMessage = ''; this.cdr.detectChanges(); }, 3000);
        this.shopService.getInventory().subscribe(data => {
          this.inventoryItems = data.filter(i => i.status !== 'on_sale');
          this.cdr.detectChanges();
        });
        this.shopService.getMySales().subscribe(data => {
          this.mySales = data;
          this.cdr.detectChanges();
        });
      },
      error: () => {
        this.errorMessage = 'Ошибка при выставлении на продажу';
        this.cdr.detectChanges();
      }
    });
  }

  cancelSale(itemId: number) {
    this.shopService.cancelSale([itemId]).subscribe({
      next: () => {
        this.successMessage = '✓ Продажа отменена';
        setTimeout(() => { this.successMessage = ''; this.cdr.detectChanges(); }, 3000);
        this.shopService.getInventory().subscribe(data => {
          this.inventoryItems = data.filter(i => i.status !== 'for_sale');
          this.cdr.detectChanges();
        });
        this.shopService.getMySales().subscribe(data => {
          this.mySales = data;
          this.cdr.detectChanges();
        });
      },
      error: () => {
        this.errorMessage = 'Ошибка при отмене продажи';
        this.cdr.detectChanges();
      }
    });
  }
}
