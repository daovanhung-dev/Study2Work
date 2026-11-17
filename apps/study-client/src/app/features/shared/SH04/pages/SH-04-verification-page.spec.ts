import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { VerificationHandoffStore } from '../../verification-handoff';
import { VerificationApi } from '../data-access/SH-04-verification.service';
import { VerificationPage } from './SH-04-verification-page';

describe('SH-04 verification page', () => {
  it('dispatches once for a valid handoff and records the accepted HTTP result', async () => {
    const dispatch = vi.fn(() => of({ state: 'accepted' as const, httpStatus: 202 }));
    const take = vi.fn(() => ({ userId: 42, email: 'student@example.com' }));
    await TestBed.configureTestingModule({
      imports: [VerificationPage],
      providers: [
        { provide: VerificationHandoffStore, useValue: { take } },
        { provide: VerificationApi, useValue: { dispatch } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(VerificationPage);
    fixture.detectChanges();

    expect(take).toHaveBeenCalledOnce();
    expect(dispatch).toHaveBeenCalledWith({ user_id: 42, email: 'student@example.com' });
    expect(fixture.componentInstance.state()).toBe('accepted');
    expect(fixture.componentInstance.httpStatus()).toBe(202);
  });

  it('does not send email verification without a valid one-time handoff', async () => {
    const dispatch = vi.fn();
    await TestBed.configureTestingModule({
      imports: [VerificationPage],
      providers: [
        { provide: VerificationHandoffStore, useValue: { take: () => null } },
        { provide: VerificationApi, useValue: { dispatch } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(VerificationPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state()).toBe('missing');
    expect(dispatch).not.toHaveBeenCalled();
  });
});
