import { Component, OnInit } from '@angular/core';
import { ShopService } from '../../services/shop';
import { InventoryItem } from '../../interfaces/models';
@Component({
  selector: 'app-inventory',
  imports: [],
  templateUrl: './inventory.html',
  styleUrl: './inventory.css',
})
export class Inventory implements OnInit {
  inventoryItems: InventoryItem[] = [];
  errorMessage = '';

  constructor(private shopService: ShopService) {}

  ngOnInit(){
    this.shopService.getInventory().subscribe({
      next: (data:InventoryItem[]) => {
        this.inventoryItems = data;
      },
      error: () => {
        this.errorMessage = 'Inventory loading error';
      }
    })
  }
}
