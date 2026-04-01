import { Routes } from '@angular/router';
import { Login } from "./pages/login/login";
import { Shop } from "./pages/shop/shop";
import { Cart } from "./pages/cart/cart";
import { Inventory } from "./pages/inventory/inventory";
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
    {path: '', redirectTo: 'shop', pathMatch: 'full'},
    {path: 'login', component: Login},
    {path: 'shop', component: Shop, canActivate: [authGuard]},
    {path: 'cart', component: Cart, canActivate: [authGuard]},
    {path: 'inventory', component: Inventory, canActivate: [authGuard]},
];
