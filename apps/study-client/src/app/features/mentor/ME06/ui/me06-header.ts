import { Component, Input } from '@angular/core';

@Component({
  selector: 'study-me06-header',
  styleUrl: './me06-header.css',
  templateUrl: './me06-header.html',
})
export class Me06Header {
  @Input() courseId: number | null = null;

  readonly navigation = [
    { label: 'Tổng quan', current: false },
    { label: 'Khóa học phụ trách', current: true },
    { label: 'Chấm bài', current: false },
    { label: 'Hộp thư hỗ trợ', current: false },
    { label: 'Thông báo', current: false },
  ] as const;
}
