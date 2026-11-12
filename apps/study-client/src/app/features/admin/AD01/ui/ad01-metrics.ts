import { Component } from '@angular/core';

import { AD01Icon } from './ad01-icon';

@Component({
  imports: [AD01Icon],
  selector: 'study-ad01-metrics',
  styleUrl: './ad01-metrics.css',
  templateUrl: './ad01-metrics.html',
})
export class AD01Metrics {
  readonly metrics = [
    {
      title: 'Người dùng hệ thống',
      description: 'Chỉ số chưa được định nghĩa trong contract.',
      icon: 'users',
    },
    {
      title: 'Chương trình học',
      description: 'Chưa có mapping chỉ số được xác nhận.',
      icon: 'book',
    },
    {
      title: 'Kiểm định chất lượng',
      description: 'Nguồn dữ liệu chưa được kết nối.',
      icon: 'checklist',
    },
    {
      title: 'Hạ tầng trực tuyến',
      description: 'Chưa có nguồn trạng thái dịch vụ.',
      icon: 'server',
    },
  ] as const;
}
