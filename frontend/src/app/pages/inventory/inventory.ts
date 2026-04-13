import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ShopService } from '../../services/shop';
import { ProfileService } from '../../services/profile';
import { InventoryItem, UserProfile } from '../../interfaces/models';
@Component({
  selector: 'app-inventory',
  imports: [],
  templateUrl: './inventory.html',
  styleUrl: './inventory.css',
})
export class Inventory implements OnInit {
  profile: UserProfile | null = null;
  inventoryItems: InventoryItem[] = [];
  errorMessage = '';

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
        this.inventoryItems = data;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Inventory loading error';
      }
    })
  }
}
