import { Routes } from '@angular/router';
import { Login } from "./pages/login/login";
import { Shop } from "./pages/shop/shop";
import { Cart } from "./pages/cart/cart";
import { Register } from "./pages/register/register";
import { Inventory } from "./pages/inventory/inventory";
import { Trades } from './pages/trades/trades';
import { TradeRoom } from './components/trade-room/trade-room';
import { Cases } from './pages/case/case';
import { CaseOpen } from './components/case-open/case-open';
import { Gangs } from './pages/gangs/gangs';
import { GangRoom } from './components/gang-room/gang-room';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
    {path: '', redirectTo: 'shop', pathMatch: 'full'},
    {path: 'login', component: Login},
    {path: 'shop', component: Shop, canActivate: [authGuard]},
    {path: 'cart', component: Cart, canActivate: [authGuard]},
    {path: 'inventory', component: Inventory, canActivate: [authGuard]},
    {path: 'trades', component: Trades, canActivate: [authGuard]},
    {path: 'trade-room', component: TradeRoom, canActivate: [authGuard]},
    {path: 'trades/:id', component: TradeRoom, canActivate: [authGuard]},
    {path: 'register', component: Register},
    {path: 'cases', component: Cases, canActivate: [authGuard]},
    {path: 'cases/:id', component: CaseOpen, canActivate: [authGuard]},
    {path: 'gangs', component: Gangs, canActivate: [authGuard]},
    {path: 'gangs/:id', component: GangRoom, canActivate: [authGuard]}
];
