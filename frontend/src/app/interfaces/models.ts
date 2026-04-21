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
    is_private: boolean;
    password?: string | null;
}

export interface Case {
  id: number;
  name: string;
  price: string;        // DecimalField → строка в JSON
  img_url: string | null;
  is_active: boolean;
  created_at: string;   // ISO datetime
}

export interface CaseItem {
  url: any;
  id: number;
  case: number;         // FK → id кейса
  skin: number;         // FK → id скина
  skin_name: string;
  wear: number;         // FK → id wear
  wear_name: string;
  drop_chance: string;  // DecimalField → строка
  created_at: string;
}

export interface CaseOpeningDrop {
  id: number;
  user: number;
  user_username: string;
  skin: number;
  skin_name: string;
  price: string;
  rarity: string;
  wear: number;
  wear_name: string;
  url: string;
  status: string;
  created_at: string;
}
 
export interface CaseOpening {
  item_id: number;
  skin_name: string;
  sell_price: number;
  drop: CaseOpeningDrop;
}

export interface LiveDrop {
  id: number;
  username: string;
  skin_name: string;
  skin_image: string;
  case_name: string;
  rarity: string;
  opened_at: string;
}

export interface ItemActionRequest {
  item_id: number;
}

export interface Gang {
  id: number;
  name: string;
  description: string;
  owner_username: string;
  members_count: number;
  is_member: boolean;
  treasury: number;
}

export interface GangMember {
  id: number;
  user_id: number;
  username: string;
  role: number;
  role_name: string;
  joined_at: string;
}

export interface GangMessage {
  id: number;
  user: number;
  username: string;
  text: string;
  formatted_display: string;
  created_at: string;
}

export interface GangJoinRequest {
  id: number;
  gang: number;
  gang_name: string;
  user: number;
  username: string;
  message: string;
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
}

export interface GangVaultRental {
  id: number;
  user: number;
  item: number;
  item_details: {
    name: string;
    image: string | null;
    rarity: string | null;
  };
  deposit_amount: string;
  status: 'active' | 'returned' | 'lost';
  status_display: string;
  created_at: string;
  returned_at: string | null;
}