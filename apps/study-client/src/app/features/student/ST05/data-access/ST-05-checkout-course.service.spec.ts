import { HttpResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom, of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { St05CourseApi } from './ST-05-checkout-course.service';

describe('ST-05 API #16 adapter', () => {
  it('maps an explicit approved provider to one Order request and reads the created ID', async () => {
    const order = { id: 71, course_id: 12, user_id: 4, amount: '100.00', currency: 'VND',
      status: 'PENDING', created_at: '2026-11-18T00:00:00Z' };
    const requestResponse = vi.fn(() => of(new HttpResponse({
      status: 201,
      body: { success: true, businessCode: 'DESIGN_RESOURCE_CREATED', message: 'Order created.',
        data: order, meta: {}, traceId: 'trace-1' },
    })));
    TestBed.configureTestingModule({
      providers: [{ provide: StudyApiService, useValue: { requestResponse } }],
    });
    const service = TestBed.inject(St05CourseApi);

    expect(await firstValueFrom(service.createOrder(12, ' approved-provider '))).toEqual(order);
    expect(requestResponse).toHaveBeenCalledWith(STUDY_SERVER_APIS.API_016, {
      body: { course_id: 12, payment_provider: 'approved-provider' },
    });
  });
});
