import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GangService } from '../../services/gang';
import { ProfileService } from '../../services/profile';
import { ShopService } from '../../services/shop';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Gang, GangMember, GangMessage, GangJoinRequest, GangVaultRental, InventoryItem } from '../../interfaces/models';

type ActiveTab = 'members' | 'vault' | 'chat' | 'requests';

@Component({
  selector: 'app-gang-room',
  imports: [FormsModule, DatePipe],
  templateUrl: './gang-room.html',
  styleUrl: './gang-room.css',
})
export class GangRoom implements OnInit, OnDestroy {
  gangId!: number;
  gang: Gang | null = null;
  members: GangMember[] = [];
  messages: GangMessage[] = [];
  joinRequests: GangJoinRequest[] = [];
  vaultItems: GangVaultRental[] = [];
  myInventory: InventoryItem[] = [];
  showDepositPanel = false;

  activeTab: ActiveTab = 'members';
  isLoading = true;
  error: string | null = null;
  actionMessage: string | null = null;

  // Chat
  newMessage = '';
  chatLoading = false;
  private chatInterval: any;

  // Current user role (1=User, 2=Admin, 3=Owner)
  myRole = 0;
  myUserId: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private gangService: GangService,
    private cdr: ChangeDetectorRef,
    private profileService: ProfileService,
    private shopService: ShopService,
  ) {}

  ngOnInit() {
    this.gangId = Number(this.route.snapshot.paramMap.get('id'));
    this.profileService.loadProfile();
    this.loadGang();
    this.loadMembers();
    this.loadRequests();
  }

  ngOnDestroy() {
    clearInterval(this.chatInterval);
  }

  loadGang() {
    this.gangService.getGangs().subscribe({
      next: (gangs) => {
        this.gang = gangs.find(g => g.id === this.gangId) || null;
        if (!this.gang) {
          this.error = 'Gang not found';
        }

        if(!this.gang?.is_member) {
          this.activeTab = 'members';
        }

        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Failed to load gang';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadMembers() {
    this.gangService.getMembers(this.gangId).subscribe({
      next: (data) => {
        this.members = data;
        this.profileService.profile$.subscribe(profile => {
          if (profile) {
            const me = data.find(m => m.username === profile.username);
            this.myRole = me?.role ?? 0;
            this.cdr.detectChanges();
          }
        });
        this.cdr.detectChanges();
      },
      error: () => {}
    });
  }

  loadRequests() {
    this.gangService.getJoinRequests(this.gangId).subscribe({
      next: (data) => {
        this.joinRequests = data;
        this.cdr.detectChanges();
      },
      error: () => {}
    });
  }

  loadVault() {
    this.gangService.getVault(this.gangId).subscribe({
      next: (data) => {
        this.vaultItems = data;
        this.cdr.detectChanges();
      },
      error: () => {}
    });
  }

  loadChat() {
    this.gangService.getChatHistory(this.gangId).subscribe({
      next: (data) => {
        this.messages = data;
        this.cdr.detectChanges();
      },
      error: () => {}
    });
  }

  loadMyInventory() {
    this.shopService.getInventory().subscribe({
      next: (data) => {
        this.myInventory = data.filter(item => item.status === 'in_inventory');
        this.cdr.detectChanges();
      },
      error: () => {}
    });
  }

  depositItem(itemId: number) {
    this.gangService.depositItem(this.gangId, itemId).subscribe({
      next: (res) => {
        this.actionMessage = res.detail || '✓ Item deposited!';
        this.showDepositPanel = false;
        this.loadVault();
        this.loadMyInventory();
        this.loadGang();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to deposit';
        this.cdr.detectChanges();
      }
    });
  }

  setTab(tab: ActiveTab) {
    this.activeTab = tab;
    this.actionMessage = null;

    if(tab != 'members' && !this.gang?.is_member) return;

    if (tab === 'requests') this.loadRequests();
    if (tab === 'vault') {
      this.loadVault();
      this.loadMyInventory();
    }
    if (tab === 'chat') {
      this.loadChat();
      this.chatInterval = setInterval(() => this.loadChat(), 5000);
    } else {
      clearInterval(this.chatInterval);
    }
  }

  apply() {
    this.gangService.applyToGang(this.gangId).subscribe({
      next: () => {
        this.actionMessage = '✓ Request sent!';
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to send request';
        this.cdr.detectChanges();
      }
    });
  }

  declineRequest(requestId: number) {
    this.gangService.declineRequest(this.gangId, requestId).subscribe({
      next: (res) => {
        this.actionMessage = res.detail;
        this.loadRequests();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to decline';
        this.cdr.detectChanges();
      }
    });
  }

  leave() {
    this.gangService.leaveGang(this.gangId).subscribe({
      next: () => {
        this.router.navigate(['/gangs']);
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to leave gang';
        this.cdr.detectChanges();
      }
    });
  }

  acceptRequest(requestId: number) {
    this.gangService.acceptRequest(this.gangId, requestId).subscribe({
      next: () => {
        this.loadRequests();
        this.loadMembers();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to accept request';
        this.cdr.detectChanges();
      }
    });
  }

  rentItem(itemId: number) {
    this.gangService.rentItem(this.gangId, itemId).subscribe({
      next: () => {
        this.actionMessage = '✓ Item rented!';
        this.loadVault();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to rent item';
        this.cdr.detectChanges();
      }
    });
  }

  returnItem(itemId: number) {
    this.gangService.returnItem(this.gangId, itemId).subscribe({
      next: () => {
        this.actionMessage = '✓ Item returned!';
        this.loadVault();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to return item';
        this.cdr.detectChanges();
      }
    });
  }

  sendMessage() {
    if (!this.newMessage.trim()) return;
    this.chatLoading = true;
    this.gangService.sendMessage(this.gangId, this.newMessage.trim()).subscribe({
      next: () => {
        this.newMessage = '';
        this.chatLoading = false;
        this.loadChat();
      },
      error: () => {
        this.chatLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  goBack() {
    this.router.navigate(['/gangs']);
  }

  promoteMember(userId: number) {
    this.gangService.promoteMember(this.gangId, userId).subscribe({
      next: (res) => {
        this.actionMessage = res.detail;
        this.loadMembers();
        this.loadGang();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to promote member';
        this.cdr.detectChanges();
      }
    });
  }

  demoteMember(userId: number) {
    this.gangService.demoteMember(this.gangId, userId).subscribe({
      next: (res) => {
        this.actionMessage = res.detail;
        this.loadMembers();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to demote member';
        this.cdr.detectChanges();
      }
    });
  }

  kickMember(userId: number) {
    this.gangService.kickMember(this.gangId, userId).subscribe({
      next: (res) => {
        this.actionMessage = res.detail;
        this.loadMembers();
        this.loadGang();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionMessage = err?.error?.detail || 'Failed to kick';
        this.cdr.detectChanges();
      }
    });
  }
}