import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';

import { ST10Page } from './st10-page';

describe('ST10Page', () => {
  it('keeps the protected lesson locked until the server can verify Student access', async () => {
    await TestBed.configureTestingModule({
      imports: [ST10Page],
      providers: [provideRouter([])],
    }).compileComponents();
    const fixture = TestBed.createComponent(ST10Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-10"]')).not.toBeNull();
    expect(root.textContent).toContain('CHƯA GỬI YÊU CẦU');
    expect(root.textContent).toContain('client chưa gửi request vì chưa có Student Bearer token');
    expect(root.querySelector('video')).toBeNull();
    expect(root.querySelector('button[disabled]')?.textContent).toContain('đang khóa');
  });
});
