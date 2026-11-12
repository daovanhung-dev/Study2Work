import { Component } from '@angular/core';

import { AD01Icon } from './ad01-icon';

@Component({
  imports: [AD01Icon],
  selector: 'study-ad01-header',
  styleUrl: './ad01-header.css',
  templateUrl: './ad01-header.html',
})
export class AD01Header {
  readonly navigation = [
    { icon: 'dashboard', label: 'Tổng quan', current: true },
    { icon: 'users', label: 'Người dùng', current: false },
    { icon: 'book', label: 'Khóa học & nội dung', current: false },
    { icon: 'checklist', label: 'Kiểm duyệt', current: false },
    { icon: 'chart', label: 'Báo cáo', current: false },
  ] as const;
}
