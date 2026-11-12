import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me12ThreadService } from '../data-access/me12-thread.service';
import { ME12Page } from './me12-page';

describe('ME12Page', () => {
  const sampleDetailEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      id: 701,
      course_id: 101,
      student: { id: 3001, full_name: 'Nguyễn Văn A', avatar_url: null },
      status: 'OPEN',
      messages: [
        {
          id: 1,
          author: { id: 3001, full_name: 'Nguyễn Văn A' },
          content: 'Em cần giải thích thêm về phần Transaction.',
          attachments: [],
          created_at: '2026-11-12T09:00:00Z',
        },
      ],
      created_at: '2026-11-12T09:00:00Z',
      resolved_at: null,
    },
    meta: {},
    traceId: 'trace-me12-detail',
  };

  function setupTest(requestId = '701') {
    const repliedEnvelope = {
      ...sampleDetailEnvelope,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      data: {
        ...sampleDetailEnvelope.data,
        messages: [
          ...sampleDetailEnvelope.data.messages,
          {
            id: 2,
            author: { id: 99, full_name: 'Mentor' },
            content: 'Em xem lại slide 14 nhé.',
            attachments: [],
            created_at: '2026-11-12T09:05:00Z',
          },
        ],
      },
    };

    const resolvedEnvelope = {
      ...sampleDetailEnvelope,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      data: {
        ...sampleDetailEnvelope.data,
        status: 'RESOLVED',
        resolved_at: '2026-11-12T09:10:00Z',
      },
    };

    const serviceStub = {
      getSupportRequestDetail: vi.fn().mockReturnValue(of(sampleDetailEnvelope)),
      sendReply: vi.fn().mockReturnValue(of(repliedEnvelope)),
      resolveRequest: vi.fn().mockReturnValue(of(resolvedEnvelope)),
    };

    TestBed.configureTestingModule({
      imports: [ME12Page],
      providers: [
        provideRouter([]),
        { provide: Me12ThreadService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ requestId }),
              queryParamMap: convertToParamMap({}),
            },
          },
        },
      ],
    });

    return { serviceStub };
  }

  it('loads support request detail (#59) and renders conversation messages', () => {
    const { serviceStub } = setupTest('701');
    const fixture = TestBed.createComponent(ME12Page);
    fixture.detectChanges();

    expect(serviceStub.getSupportRequestDetail).toHaveBeenCalledWith(701);
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Em cần giải thích thêm về phần Transaction.');
    expect(text).toContain('Nguyễn Văn A');
  });

  it('sends reply via API #60 with attachment_refs="[]" and reloads #59', () => {
    const { serviceStub } = setupTest('701');
    const fixture = TestBed.createComponent(ME12Page);
    fixture.detectChanges();

    const comp = fixture.componentInstance;
    comp.onReplyDraftChange('Em xem lại slide 14 nhé.');
    comp.submitReply();

    expect(serviceStub.sendReply).toHaveBeenCalledWith(701, {
      message: 'Em xem lại slide 14 nhé.',
      attachment_refs: '[]',
    });
    expect(comp.replyStatus()).toBe('saved');
    expect(serviceStub.getSupportRequestDetail).toHaveBeenCalledTimes(2);
  });

  it('resolves support request via API #61 after confirmation checkbox is checked', () => {
    const { serviceStub } = setupTest('701');
    const fixture = TestBed.createComponent(ME12Page);
    fixture.detectChanges();

    const comp = fixture.componentInstance;
    comp.onConfirmResolveChange(true);
    comp.submitResolve();

    expect(serviceStub.resolveRequest).toHaveBeenCalledWith(701);
    expect(comp.resolveStatus()).toBe('saved');
    expect(comp.requestDetail()?.status).toBe('RESOLVED');
  });
});
