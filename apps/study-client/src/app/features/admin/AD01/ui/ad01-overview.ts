import { Component } from '@angular/core';

import { AD01Icon } from './ad01-icon';

@Component({
  imports: [AD01Icon],
  selector: 'study-ad01-overview',
  styleUrl: './ad01-overview.css',
  templateUrl: './ad01-overview.html',
})
export class AD01Overview {
  readonly services = [
    { title: 'Cơ sở dữ liệu', icon: 'database' },
    { title: 'Dịch vụ xác thực', icon: 'shield' },
    { title: 'Hàng đợi tác vụ', icon: 'layers' },
  ] as const;
}
