import { Component, OnInit } from '@angular/core';
import { ShopService } from '../../services/shop';
@Component({
  selector: 'app-inventory',
  imports: [],
  templateUrl: './inventory.html',
  styleUrl: './inventory.css',
})
export class Inventory implements OnInit {
  inventoryItems: any[] = [];

  constructor(private shopService: ShopService) {}

  ngOnInit(){
    this.shopService.getInventory().subscribe({
      next: (data:any) => {
        this.inventoryItems = data;
      },
      error: () => {
        console.log('Inventory loading error');
      }
    })
  }
}
