export interface Skin {
    id: number;
    name: string;
    weapon: string;
    rarity: string;
    base_price: number;
    url: string;
}

export interface InventoryItem {
    id: number;
    user: number;
    skin: string;
    price: number;
    status: string;
    obtained_type: string;
    wear: string;
    purchase_price: number;
    sale_price: number;
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
    inventory_item: number;
    added_at: string;
}

export interface Weapon {
    id: number;
    category: number;
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