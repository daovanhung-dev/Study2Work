import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { StudentApiService } from '../../../../core/http/student-api.service';
import { ST18SubmissionService } from './st18-submission.service';

describe('ST18SubmissionService', () => {
  let request: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    request = vi.fn().mockReturnValue(of({ success: true, data: {} }));

    await TestBed.configureTestingModule({
      providers: [
        ST18SubmissionService,
        { provide: StudentApiService, useValue: { request } },
      ],
    }).compileComponents();
  });

  afterEach(() => TestBed.resetTestingModule());

  it('maps the route assignment ID to API #33', () => {
    TestBed.inject(ST18SubmissionService).assignment('42').subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_033, {
      pathParams: { assignment_id: '42' },
    });
  });

  it('maps a selected submission file to API #34 multipart fields', () => {
    const file = new File(['submission'], 'submission.txt', { type: 'text/plain' });
    TestBed.inject(ST18SubmissionService).upload(file, 9).subscribe();

    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0]?.[0]).toBe(STUDY_SERVER_APIS.API_034);
    const options = request.mock.calls[0]?.[1] as { body: FormData };
    expect([...options.body.keys()]).toEqual(['file', 'purpose', 'course_id']);
    expect(options.body.get('file')).toMatchObject({ name: 'submission.txt', type: 'text/plain' });
    expect(options.body.get('purpose')).toBe('SUBMISSION');
    expect(options.body.get('course_id')).toBe('9');
  });

  it('maps the assignment route ID and selected upload reference to API #35', () => {
    TestBed.inject(ST18SubmissionService).submit('42', 'My submission', 77).subscribe();

    expect(request).toHaveBeenCalledExactlyOnceWith(STUDY_SERVER_APIS.API_035, {
      pathParams: { assignment_id: '42' },
      body: { content: 'My submission', upload_id: 77 },
    });
  });
});
