import { Routes } from '@angular/router';
import {Login} from "./pages/login/login";
import {Shop} from "./pages/shop/shop";
import {Cart} from "./pages/cart/cart";
import {Inventory} from "./pages/inventory/inventory"; 

export const routes: Routes = [
    {path: '', redirectTo: 'shop', pathMatch: 'full'},
    {path: 'login', component: Login},
    {path: 'shop', component: Shop},
    {path: 'cart', component: Cart},
    {path: 'inventory', component: Inventory},
];
