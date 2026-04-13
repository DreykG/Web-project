import { NumberValueAccessor } from "@angular/forms";

export interface Weapon {
    id: number;
    category: Category;
    name: string;
}

export interface Category {
    id: number;
    name: string;
}

export interface Rarity {
    id: number;
    name: string;
}

export interface Wear {
    id: number;
    name: string;
}

export interface Skin {
    id: number;
    name: string;
    weapon: Weapon;
    rarity: Rarity;
    base_price: number;
    url: string;
}

export interface InventoryItem {
    id: number;
    user: number;
    user_username: string;
    skin: number;
    skin_name: string;
    price: number;
    rarity: string;
    wear: number;
    wear_name: string;
    url: string;
    status: string;
    created_at: string;
}

export interface Cart {
    id: number;
    user: number;
    created_at: string;
    updated_at: string;
}

export interface CartItem {
    id: number;
    cart: number;
    inventory_item: InventoryItem;
    added_at: string;
}

export interface CartResponse {
    cart_id: number;
    items: InventoryItem[];
    total_items_count: number;
    total_price: number;
}

export interface UserProfile {
    id: number;
    username: string;
    balance: number;
    avatar: string | null;
    cases_opened_count: number;
    total_drop_value: number;
    inventory_value: number;
    date_joined: string;
}

export interface TradeOfferItem {
    id: number;
    inventory_item: number;
    inventory_item_details: InventoryItem;
}

export interface TradeResponseItem {
    id: number;
    inventory_item: number;
    inventory_item_details: InventoryItem;
}

export interface TradeResponse {
    id: number;
    responder: number;
    responder_username: string;
    status: 'pending' | 'accepted' | 'rejected';
    response_value: number;
    items: TradeResponseItem[];
    responded_at: string;
}

export interface TradeOffer {
    id: number;
    creator: number;
    creator_username: string;
    title: string;
    status: 'open' | 'closed' | 'cancelled';
    offer_value: number;
    items: TradeOfferItem[];
    responses_count: number;
    responses: TradeResponse[];
    created_at: string;
}