import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GangService } from '../../services/gang';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Gang, GangMember, GangMessage, GangJoinRequest, GangVaultRental } from '../../interfaces/models';

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
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.gangId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadGang();
    this.loadMembers();
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

  setTab(tab: ActiveTab) {
    this.activeTab = tab;
    this.actionMessage = null;

    if (tab === 'requests') this.loadRequests();
    if (tab === 'vault') this.loadVault();
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

  acceptRequest(userId: number) {
    this.gangService.acceptRequest(this.gangId, userId).subscribe({
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
}