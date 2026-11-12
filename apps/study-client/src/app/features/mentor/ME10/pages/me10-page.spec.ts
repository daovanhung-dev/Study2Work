import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { Me10GradingService } from '../data-access/me10-grading.service';
import { ME10Page } from './me10-page';

describe('ME10Page', () => {
  const sampleDetailEnvelope = {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'OK',
    data: {
      id: 9001,
      assignment_id: 301,
      user_id: 7001,
      content: 'Giải pháp kiến trúc microservices của học viên.',
      files: [
        {
          id: 44,
          name: 'report.pdf',
          url: 'https://cdn.example.com/report.pdf',
          content_type: 'application/pdf',
          size_bytes: 2048,
          status: 'READY',
        },
      ],
      status: 'SUBMITTED',
      submitted_at: '2026-11-12T08:00:00Z',
      score: null,
      feedback: null,
    },
    meta: {},
    traceId: 'trace-me10-detail',
  };

  function setupTest(submissionId = '9001') {
    const gradedEnvelope = {
      ...sampleDetailEnvelope,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      data: { ...sampleDetailEnvelope.data, status: 'GRADED', score: '85.00' },
    };

    const feedbackEnvelope = {
      ...sampleDetailEnvelope,
      businessCode: 'DESIGN_RESOURCE_UPDATED',
      data: { ...sampleDetailEnvelope.data, feedback: 'Bài làm tốt, trình bày rõ ràng.' },
    };

    const serviceStub = {
      getSubmissionDetail: vi.fn().mockReturnValue(of(sampleDetailEnvelope)),
      saveGrade: vi.fn().mockReturnValue(of(gradedEnvelope)),
      saveFeedback: vi.fn().mockReturnValue(of(feedbackEnvelope)),
    };

    TestBed.configureTestingModule({
      imports: [ME10Page],
      providers: [
        provideRouter([]),
        { provide: Me10GradingService, useValue: serviceStub },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ submissionId }),
              queryParamMap: convertToParamMap({}),
            },
          },
        },
      ],
    });

    return { serviceStub };
  }

  it('loads submission detail (#55) and renders content + file attachment', () => {
    const { serviceStub } = setupTest('9001');
    const fixture = TestBed.createComponent(ME10Page);
    fixture.detectChanges();

    expect(serviceStub.getSubmissionDetail).toHaveBeenCalledWith(9001);
    expect(fixture.componentInstance.screenState()).toBe('ready');

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Giải pháp kiến trúc microservices của học viên.');
    expect(text).toContain('report.pdf');
  });

  it('saves integer score via API #56 independently while preserving unsaved feedback draft', () => {
    const { serviceStub } = setupTest('9001');
    const fixture = TestBed.createComponent(ME10Page);
    fixture.detectChanges();

    const comp = fixture.componentInstance;
    comp.onScoreInput('85');
    comp.onFeedbackInput('Bản nháp nhận xét chưa lưu');
    comp.submitGrade();

    expect(serviceStub.saveGrade).toHaveBeenCalledWith(9001, {
      score: 85,
      rubric_items: '[]',
    });
    expect(comp.gradeStatus()).toBe('saved');
    expect(comp.feedbackDraft()).toBe('Bản nháp nhận xét chưa lưu');
    expect(comp.feedbackStatus()).toBe('dirty');
    expect(serviceStub.getSubmissionDetail).toHaveBeenCalledTimes(2);
  });

  it('saves feedback via API #57 independently and keeps combined button disabled', () => {
    const { serviceStub } = setupTest('9001');
    const fixture = TestBed.createComponent(ME10Page);
    fixture.detectChanges();

    const comp = fixture.componentInstance;
    comp.onFeedbackInput('Bài làm tốt, trình bày rõ ràng.');
    comp.submitFeedback();

    expect(serviceStub.saveFeedback).toHaveBeenCalledWith(9001, {
      feedback_text: 'Bài làm tốt, trình bày rõ ràng.',
      attachments: '[]',
    });
    expect(comp.feedbackStatus()).toBe('saved');

    const combinedBtn = (fixture.nativeElement as HTMLElement).querySelector(
      '#btn-combined-disabled',
    ) as HTMLButtonElement | null;
    expect(combinedBtn).not.toBeNull();
    expect(combinedBtn?.disabled).toBe(true);
  });
});
