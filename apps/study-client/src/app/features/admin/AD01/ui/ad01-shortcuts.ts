import { Component } from '@angular/core';

import { AD01Icon } from './ad01-icon';

@Component({
  imports: [AD01Icon],
  selector: 'study-ad01-shortcuts',
  styleUrl: './ad01-shortcuts.css',
  templateUrl: './ad01-shortcuts.html',
})
export class AD01Shortcuts {
  readonly shortcuts = [
    {
      title: 'Quản lý người dùng',
      description: 'Hồ sơ và trạng thái người dùng',
      icon: 'users',
    },
    {
      title: 'Quản lý khóa học',
      description: 'Chương trình và nội dung học',
      icon: 'book',
    },
    {
      title: 'Hàng đợi kiểm duyệt',
      description: 'Bài nộp và học liệu cần xem xét',
      icon: 'checklist',
    },
  ] as const;
}
