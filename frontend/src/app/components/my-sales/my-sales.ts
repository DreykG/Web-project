import { Component, OnInit } from '@angular/core';
import { InventoryItem } from '../../interfaces/models';
import { ShopService } from '../../services/shop';

@Component({
  selector: 'app-my-sales',
  imports: [],
  templateUrl: './my-sales.html',
  styleUrl: './my-sales.css',
})
export class MySales implements OnInit {
  sales: InventoryItem[] = [];
  errorMessage = '';

  constructor(private shopService: ShopService) {}

  ngOnInit() {
    this.loadSales();
  }

  loadSales() {
    this.shopService.getMySales().subscribe({
      next: (data) => this.sales = data,
      error: () => this.errorMessage = 'Ошибка загрузки продаж'
    });
  }

  cancelSale(itemId: number) {
    this.shopService.cancelSale([itemId]).subscribe({
      next: () => {
        alert('Продажа отменена');
        this.loadSales(); // обновить список
      },
      error: () => this.errorMessage = 'Ошибка отмены'
    });
  }
}
