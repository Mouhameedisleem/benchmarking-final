import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AppNotification {
  id: string;
  message: string;
  type: string;
  timestamp: string;
  read: boolean;
}

@Injectable({ providedIn: 'root' })
export class NotificationService implements OnDestroy {

  private readonly _notifs = new BehaviorSubject<AppNotification[]>([]);
  readonly notifications$ = this._notifs.asObservable();

  private abortCtrl?: AbortController;
  private reconnectTimer?: ReturnType<typeof setTimeout>;

  get notifications(): AppNotification[] { return this._notifs.value; }
  get unreadCount(): number { return this._notifs.value.filter(n => !n.read).length; }

  connect(): void {
    const token = localStorage.getItem('token');
    if (!token) return;
    this.disconnect();
    this.stream(token);
  }

  disconnect(): void {
    clearTimeout(this.reconnectTimer);
    this.abortCtrl?.abort();
  }

  markAllRead(): void {
    this._notifs.next(this._notifs.value.map(n => ({ ...n, read: true })));
  }

  clear(): void { this._notifs.next([]); }

  ngOnDestroy(): void { this.disconnect(); }

  // ── fetch()-based SSE — supports Authorization header unlike EventSource ───

  private async stream(token: string): Promise<void> {
    this.abortCtrl = new AbortController();
    try {
      const resp = await fetch(`${environment.apiUrl}/notifications/stream`, {
        headers: { Authorization: `Bearer ${token}` },
        signal: this.abortCtrl.signal
      });
      if (!resp.ok || !resp.body) { this.scheduleReconnect(token); return; }

      const reader  = resp.body.getReader();
      const decoder = new TextDecoder();
      let   buffer  = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // SSE events are separated by double newlines
        const events = buffer.split('\n\n');
        buffer = events.pop() ?? '';

        for (const event of events) {
          const dataLine = event.split('\n').find(l => l.startsWith('data:'));
          if (!dataLine) continue;
          try {
            const parsed = JSON.parse(dataLine.slice(5).trim()) as AppNotification;
            if (parsed.type && parsed.type !== 'connected') {
              this.push(parsed);
            }
          } catch { /* ignore malformed frames */ }
        }
      }
    } catch (err: any) {
      if (err?.name !== 'AbortError') this.scheduleReconnect(token);
    }
  }

  private push(notif: AppNotification): void {
    const current = this._notifs.value;
    if (current.some(n => n.id === notif.id)) return; // deduplicate
    this._notifs.next([{ ...notif, read: false }, ...current].slice(0, 30));
  }

  private scheduleReconnect(token: string): void {
    this.reconnectTimer = setTimeout(() => this.stream(token), 5000);
  }
}
