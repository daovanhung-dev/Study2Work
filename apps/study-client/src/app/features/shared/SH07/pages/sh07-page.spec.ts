import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { SH07OperationService } from '../data-access/sh07-operation.service';
import { SH07Page } from './sh07-page';

const operationId = 'b46e19e7-4ef2-4a4f-9ed2-83783e68fb01';

describe('SH07Page', () => {
  it('loads a notification operation and offers only explicit manual refresh', async () => {
    const service = { getOperation: vi.fn(() => of(operationEnvelope())) };
    const fixture = await createPage(service, operationId);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(service.getOperation).toHaveBeenCalledTimes(1);
    expect(root.textContent).toContain('Đã tiếp nhận · đang chờ xử lý');
    expect(root.textContent).toContain('chưa xác nhận thông báo đã được gửi');
    expect(root.textContent).not.toContain('owner_id');
    expect(root.querySelector('.sh07-refresh')?.textContent).toContain('Làm mới trạng thái');

    root.querySelector<HTMLButtonElement>('.sh07-refresh')!.click();
    fixture.detectChanges();
    expect(service.getOperation).toHaveBeenCalledTimes(2);
  });

  it('does not call API #18 when the route ID is not a UUID', async () => {
    const service = { getOperation: vi.fn(() => of(operationEnvelope())) };
    const fixture = await createPage(service, 'not-a-uuid');
    fixture.detectChanges();

    expect(service.getOperation).not.toHaveBeenCalled();
    expect((fixture.nativeElement as HTMLElement).querySelector('[role="alert"]')?.textContent)
      .toContain('không hợp lệ');
  });

  it('keeps owner-bound not-found responses private and understandable', async () => {
    const service = {
      getOperation: vi.fn(() => throwError(() => new HttpErrorResponse({ status: 404 }))),
    };
    const fixture = await createPage(service, operationId);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[role="alert"]')?.textContent)
      .toContain('không thuộc tài khoản hiện tại');
    expect(root.textContent).not.toContain('DESIGN_RESOURCE_NOT_FOUND');
  });
});

async function createPage(
  service: { getOperation: ReturnType<typeof vi.fn> },
  id: string,
) {
  await TestBed.configureTestingModule({
    imports: [SH07Page],
    providers: [
      provideRouter([]),
      { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ operationId: id }) } } },
      { provide: SH07OperationService, useValue: service },
    ],
  }).compileComponents();
  return TestBed.createComponent(SH07Page);
}

function operationEnvelope(): ApiEnvelope<unknown> {
  return {
    success: true,
    businessCode: 'DESIGN_OPERATION_RETRIEVED',
    message: 'Operation retrieved.',
    data: {
      id: operationId,
      kind: 'NOTIFICATION_DISPATCH',
      status: 'QUEUED',
      owner_id: 42,
      submitted_at: '2026-11-20T10:00:00Z',
      updated_at: '2026-11-20T10:00:00Z',
    },
    meta: {},
    traceId: 'trace-test',
  };
}
